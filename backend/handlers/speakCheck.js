"use strict";

/**
 * Learner speak-check: S3 upload → Amazon Transcribe bs-BA → Bedrock Amazon Nova.
 * Public endpoints (rate-limited). All-AWS stack for credit billing.
 */

const AWS = require("aws-sdk");
const crypto = require("crypto");
const https = require("https");
const { json } = require("../lib/auth");

const s3 = new AWS.S3({ signatureVersion: "v4" });
const transcribe = new AWS.TranscribeService();
const bedrock = new AWS.BedrockRuntime({
  region: process.env.AWS_REGION || process.env.BEDROCK_REGION || "us-east-1",
});
const dynamodb = new AWS.DynamoDB.DocumentClient();

const MAX_ATTEMPTS_PER_HOUR = 20;
const NOVA_MODEL = process.env.NOVA_MODEL_ID || "amazon.nova-lite-v1:0";

function requestOrigin(event) {
  return event.headers?.origin || event.headers?.Origin || "*";
}

function clientKey(event) {
  const ip =
    event.requestContext?.http?.sourceIp ||
    event.requestContext?.identity?.sourceIp ||
    event.headers?.["x-forwarded-for"]?.split(",")[0]?.trim() ||
    "unknown";
  return crypto.createHash("sha256").update(ip).digest("hex").slice(0, 24);
}

function sleep(ms) {
  return new Promise((r) => setTimeout(r, ms));
}

function fetchJson(url) {
  return new Promise((resolve, reject) => {
    https
      .get(url, (res) => {
        let data = "";
        res.on("data", (c) => {
          data += c;
        });
        res.on("end", () => {
          try {
            resolve(JSON.parse(data));
          } catch (err) {
            reject(err);
          }
        });
      })
      .on("error", reject);
  });
}

async function rateLimit(key) {
  const table = process.env.DYNAMODB_TABLE;
  if (!table) return true;
  const hour = new Date().toISOString().slice(0, 13);
  const pk = `SPEAK_RL#${key}`;
  const sk = `HOUR#${hour}`;
  try {
    const existing = await dynamodb
      .get({ TableName: table, Key: { pk, sk } })
      .promise();
    const count = existing.Item?.count || 0;
    if (count >= MAX_ATTEMPTS_PER_HOUR) return false;
    await dynamodb
      .put({
        TableName: table,
        Item: {
          pk,
          sk,
          count: count + 1,
          updatedAt: new Date().toISOString(),
        },
      })
      .promise();
    return true;
  } catch (err) {
    console.warn("rateLimit error", err);
    return true;
  }
}

async function waitForTranscript(jobName) {
  for (let i = 0; i < 40; i += 1) {
    const res = await transcribe
      .getTranscriptionJob({ TranscriptionJobName: jobName })
      .promise();
    const job = res.TranscriptionJob;
    const status = job.TranscriptionJobStatus;
    if (status === "COMPLETED") {
      const uri = job.Transcript.TranscriptFileUri;
      const data = await fetchJson(uri);
      const text =
        data?.results?.transcripts?.[0]?.transcript?.trim() || "";
      const confItems = data?.results?.items || [];
      const confs = confItems
        .map((it) => Number(it.alternatives?.[0]?.confidence))
        .filter((n) => !Number.isNaN(n));
      const confidence = confs.length
        ? confs.reduce((a, b) => a + b, 0) / confs.length
        : 0;
      return { text, confidence };
    }
    if (status === "FAILED") {
      throw new Error(job.FailureReason || "Transcription failed");
    }
    await sleep(1500);
  }
  throw new Error("Transcription timed out");
}

function parseNovaJson(raw) {
  const text = String(raw || "").trim();
  const start = text.indexOf("{");
  const end = text.lastIndexOf("}");
  if (start >= 0 && end > start) {
    try {
      return JSON.parse(text.slice(start, end + 1));
    } catch {
      /* fall through */
    }
  }
  return {
    verdict: "retry",
    heard: "",
    target: "",
    fixes: ["Could not parse coach feedback. Compare with the teacher audio."],
    encourage: "Try once more.",
  };
}

async function coachWithNova({ target, english, heard, confidence, vocabulary }) {
  const system = `You are a friendly Bosnian (Latin script) pronunciation and phrase coach for A1 learners.
Compare what ASR heard to the target line. Give short, kind, actionable fixes in English.
Never invent phonetic details you cannot know. If ASR is empty or very low confidence, verdict=unclear.
Reply with JSON only: {"verdict":"pass"|"retry"|"unclear","heard":"...","target":"...","fixes":["..."],"encourage":"..."}
Max 3 fixes. Keep each fix under 120 characters.`;

  const user = JSON.stringify({
    target,
    english,
    asrHeard: heard,
    asrConfidence: confidence,
    lessonVocabulary: (vocabulary || []).slice(0, 30),
  });

  const body = {
    schemaVersion: "messages-v1",
    system: [{ text: system }],
    messages: [
      {
        role: "user",
        content: [{ text: user }],
      },
    ],
    inferenceConfig: {
      maxTokens: 400,
      temperature: 0.2,
    },
  };

  const res = await bedrock
    .invokeModel({
      modelId: NOVA_MODEL,
      contentType: "application/json",
      accept: "application/json",
      body: JSON.stringify(body),
    })
    .promise();

  const payload = JSON.parse(Buffer.from(res.body).toString("utf8"));
  const raw =
    payload?.output?.message?.content?.map((c) => c.text).join("") ||
    payload?.content?.[0]?.text ||
    payload?.outputText ||
    JSON.stringify(payload);

  const parsed = parseNovaJson(raw);
  parsed.heard = parsed.heard || heard || "";
  parsed.target = parsed.target || target;
  parsed.fixes = Array.isArray(parsed.fixes) ? parsed.fixes.slice(0, 3) : [];
  return parsed;
}

async function deleteQuietly(key) {
  try {
    await s3
      .deleteObject({ Bucket: process.env.AUDIO_BUCKET, Key: key })
      .promise();
  } catch (err) {
    console.warn("deleteQuietly", err.message);
  }
}

function mediaFormatForKey(s3Key) {
  if (s3Key.endsWith(".mp4") || s3Key.endsWith(".m4a")) return "mp4";
  if (s3Key.endsWith(".ogg") || s3Key.endsWith(".oga")) return "ogg";
  if (s3Key.endsWith(".wav")) return "wav";
  if (s3Key.endsWith(".mp3")) return "mp3";
  if (s3Key.endsWith(".flac")) return "flac";
  if (s3Key.endsWith(".webm")) return "webm";
  return undefined;
}

module.exports.handleSpeakCheck = async function handleSpeakCheck(event, key) {
  const origin = requestOrigin(event);
  const bucket = process.env.AUDIO_BUCKET;
  if (!bucket) {
    return json(500, { error: "AUDIO_BUCKET not configured" }, origin);
  }

  const rlKey = clientKey(event);
  const allowed = await rateLimit(rlKey);
  if (!allowed) {
    return json(
      429,
      { error: "Too many speak checks. Try again later." },
      origin
    );
  }

  if (key === "POST /speak-check/upload-url") {
    const body = JSON.parse(event.body || "{}");
    let contentType = body.contentType || "audio/webm";
    if (!String(contentType).startsWith("audio/")) {
      return json(400, { error: "contentType must be audio/*" }, origin);
    }
    const id = crypto.randomBytes(12).toString("hex");
    const ext = contentType.includes("mp4")
      ? "mp4"
      : contentType.includes("ogg")
      ? "ogg"
      : contentType.includes("wav")
      ? "wav"
      : "webm";
    const s3Key = `learner-takes/${new Date()
      .toISOString()
      .slice(0, 10)}/${id}.${ext}`;
    const uploadUrl = await s3.getSignedUrlPromise("putObject", {
      Bucket: bucket,
      Key: s3Key,
      ContentType: contentType,
      Expires: 60 * 5,
    });
    return json(
      200,
      { uploadUrl, s3Key, contentType, expiresInSeconds: 300 },
      origin
    );
  }

  if (key === "POST /speak-check") {
    const body = JSON.parse(event.body || "{}");
    const { s3Key, target, english, vocabulary, day, lineIndex } = body;
    if (!s3Key || !target) {
      return json(400, { error: "s3Key and target are required" }, origin);
    }
    if (!String(s3Key).startsWith("learner-takes/")) {
      return json(400, { error: "Invalid s3Key" }, origin);
    }

    const jobName = `lb-speak-${Date.now()}-${crypto
      .randomBytes(4)
      .toString("hex")}`;
    const mediaUri = `s3://${bucket}/${s3Key}`;
    const format = mediaFormatForKey(s3Key);

    const startParams = {
      TranscriptionJobName: jobName,
      LanguageCode: "bs-BA",
      Media: { MediaFileUri: mediaUri },
    };
    if (format) startParams.MediaFormat = format;

    try {
      await transcribe.startTranscriptionJob(startParams).promise();
    } catch (err) {
      await deleteQuietly(s3Key);
      throw err;
    }

    let transcript;
    try {
      transcript = await waitForTranscript(jobName);
    } catch (err) {
      await deleteQuietly(s3Key);
      throw err;
    }

    let feedback;
    try {
      if (!transcript.text || transcript.confidence < 0.15) {
        feedback = {
          verdict: "unclear",
          heard: transcript.text || "",
          target,
          fixes: [
            "Could not hear clearly. Move closer to the mic and try again.",
          ],
          encourage: "Play the teacher line, then record once more.",
        };
      } else {
        feedback = await coachWithNova({
          target,
          english: english || "",
          heard: transcript.text,
          confidence: transcript.confidence,
          vocabulary: Array.isArray(vocabulary) ? vocabulary : [],
        });
      }
    } finally {
      await deleteQuietly(s3Key);
    }

    return json(
      200,
      {
        ...feedback,
        day: day ?? null,
        lineIndex: lineIndex ?? null,
      },
      origin
    );
  }

  return null;
};
