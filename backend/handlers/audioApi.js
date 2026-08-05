"use strict";

const AWS = require("aws-sdk");
const path = require("path");
const {
  corsHeaders,
  json,
  timingSafeEqualString,
  issueToken,
  requireAuth,
} = require("../lib/auth");

const s3 = new AWS.S3({ signatureVersion: "v4" });
const dynamodb = new AWS.DynamoDB.DocumentClient();

function loadCatalog() {
  // Packaged next to handler via sync-content → backend/data/clips.json
  // eslint-disable-next-line import/no-dynamic-require, global-require
  return require(path.join(__dirname, "..", "data", "clips.json"));
}

function requestOrigin(event) {
  return event.headers?.origin || event.headers?.Origin || "*";
}

function routeKey(event) {
  const method = (
    event.requestContext?.http?.method ||
    event.httpMethod ||
    "GET"
  ).toUpperCase();
  let p = event.rawPath || event.path || "/";
  // Strip stage prefix like /prod
  p = p.replace(/^\/prod/, "").replace(/^\/dev/, "") || "/";
  return `${method} ${p}`;
}

async function listRecordingStatus() {
  const table = process.env.DYNAMODB_TABLE;
  const result = await dynamodb
    .query({
      TableName: table,
      KeyConditionExpression: "pk = :pk",
      ExpressionAttributeValues: { ":pk": "AUDIO_CLIP" },
    })
    .promise();
  const byId = {};
  for (const item of result.Items || []) {
    byId[item.clipId] = {
      clipId: item.clipId,
      status: item.status || "recorded",
      voiceId: item.voiceId || null,
      contentType: item.contentType || null,
      s3Key: item.s3Key || null,
      updatedAt: item.updatedAt || null,
    };
  }
  return byId;
}

module.exports.handler = async (event) => {
  const origin = requestOrigin(event);
  const method = (
    event.requestContext?.http?.method ||
    event.httpMethod ||
    "GET"
  ).toUpperCase();

  if (method === "OPTIONS") {
    return { statusCode: 204, headers: corsHeaders(origin), body: "" };
  }

  const password = process.env.RECORDING_PASSWORD || "";
  const tokenSecret = process.env.AUDIO_TOKEN_SECRET || password;
  const bucket = process.env.AUDIO_BUCKET;
  const key = routeKey(event);

  try {
    if (key === "POST /audio/login") {
      const body = JSON.parse(event.body || "{}");
      if (!password || !timingSafeEqualString(body.password, password)) {
        return json(401, { error: "Invalid password" }, origin);
      }
      const token = issueToken(tokenSecret);
      return json(200, { token, expiresInHours: 12 }, origin);
    }

    const auth = requireAuth(event, tokenSecret);
    if (!auth && key !== "GET /audio/health") {
      return json(401, { error: "Unauthorized" }, origin);
    }

    if (key === "GET /audio/health") {
      return json(200, { ok: true }, origin);
    }

    if (key === "GET /audio/voices") {
      const catalog = loadCatalog();
      return json(200, { voices: catalog.voiceProfiles || [] }, origin);
    }

    if (key === "GET /audio/clips") {
      const catalog = loadCatalog();
      const status = await listRecordingStatus();
      const dayFilter = event.queryStringParameters?.day;
      const typeFilter = event.queryStringParameters?.type;
      const genderFilter = event.queryStringParameters?.gender;

      let clips = catalog.clips || [];
      if (dayFilter != null && dayFilter !== "") {
        const day = Number(dayFilter);
        clips = clips.filter((c) => c.day === day);
      }
      if (typeFilter) {
        clips = clips.filter((c) => c.type === typeFilter);
      }
      if (genderFilter && genderFilter !== "any") {
        clips = clips.filter(
          (c) =>
            c.preferredGender === "any" || c.preferredGender === genderFilter
        );
      }

      const enriched = clips.map((c) => ({
        ...c,
        recording: status[c.id] || null,
        recorded: Boolean(status[c.id]),
      }));

      const days = Array.from(new Set((catalog.clips || []).map((c) => c.day))).sort(
        (a, b) => a - b
      );

      return json(
        200,
        {
          generatedAt: catalog.generatedAt,
          total: catalog.total,
          days,
          recordedCount: Object.keys(status).length,
          clips: enriched,
        },
        origin
      );
    }

    if (key === "POST /audio/upload-url") {
      const body = JSON.parse(event.body || "{}");
      const { clipId, voiceId, contentType } = body;
      if (!clipId || !voiceId || !contentType) {
        return json(
          400,
          { error: "clipId, voiceId, and contentType are required" },
          origin
        );
      }
      if (!String(contentType).startsWith("audio/")) {
        return json(400, { error: "contentType must be audio/*" }, origin);
      }

      const catalog = loadCatalog();
      const clip = (catalog.clips || []).find((c) => c.id === clipId);
      if (!clip) {
        return json(404, { error: "Unknown clipId" }, origin);
      }

      const voiceOk = (catalog.voiceProfiles || []).some((v) => v.id === voiceId);
      if (!voiceOk) {
        return json(400, { error: "Unknown voiceId" }, origin);
      }

      const s3Key = clip.s3Key || `clips/${clipId}`;
      const uploadUrl = await s3.getSignedUrlPromise("putObject", {
        Bucket: bucket,
        Key: s3Key,
        ContentType: contentType,
        Expires: 60 * 5,
        Metadata: {
          clipid: clipId,
          voiceid: voiceId,
        },
      });

      return json(
        200,
        {
          uploadUrl,
          s3Key,
          clipId,
          expiresInSeconds: 300,
          publicPath: `/${s3Key}`,
        },
        origin
      );
    }

    if (key === "POST /audio/complete") {
      const body = JSON.parse(event.body || "{}");
      const { clipId, voiceId, contentType, s3Key } = body;
      if (!clipId || !voiceId || !s3Key) {
        return json(
          400,
          { error: "clipId, voiceId, and s3Key are required" },
          origin
        );
      }

      const catalog = loadCatalog();
      const clip = (catalog.clips || []).find((c) => c.id === clipId);
      if (!clip) {
        return json(404, { error: "Unknown clipId" }, origin);
      }

      const now = new Date().toISOString();
      await dynamodb
        .put({
          TableName: process.env.DYNAMODB_TABLE,
          Item: {
            pk: "AUDIO_CLIP",
            sk: `CLIP#${clipId}`,
            clipId,
            voiceId,
            contentType: contentType || "audio/mp4",
            s3Key,
            status: "recorded",
            book: clip.book,
            day: clip.day,
            type: clip.type,
            bosnian: clip.bosnian,
            updatedAt: now,
            gsi1pk: `DAY#${clip.day}`,
            gsi1sk: `CLIP#${clipId}`,
          },
        })
        .promise();

      return json(200, { ok: true, clipId, updatedAt: now }, origin);
    }

    return json(404, { error: `Not found: ${key}` }, origin);
  } catch (error) {
    console.error("audioApi error", error);
    return json(500, { error: "Internal server error" }, origin);
  }
};
