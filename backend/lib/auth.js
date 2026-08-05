"use strict";

const crypto = require("crypto");

const TOKEN_TTL_SECONDS = 60 * 60 * 12; // 12 hours

function corsHeaders(origin) {
  return {
    "Access-Control-Allow-Origin": origin || "*",
    "Access-Control-Allow-Headers": "Content-Type,Authorization",
    "Access-Control-Allow-Methods": "GET,POST,OPTIONS",
    "Access-Control-Allow-Credentials": "true",
  };
}

function json(statusCode, body, origin) {
  return {
    statusCode,
    headers: {
      ...corsHeaders(origin),
      "Content-Type": "application/json",
    },
    body: JSON.stringify(body),
  };
}

function timingSafeEqualString(a, b) {
  const aa = Buffer.from(String(a || ""));
  const bb = Buffer.from(String(b || ""));
  if (aa.length !== bb.length) {
    crypto.timingSafeEqual(aa, aa);
    return false;
  }
  return crypto.timingSafeEqual(aa, bb);
}

function signToken(payload, secret) {
  const body = Buffer.from(JSON.stringify(payload)).toString("base64url");
  const sig = crypto
    .createHmac("sha256", secret)
    .update(body)
    .digest("base64url");
  return `${body}.${sig}`;
}

function verifyToken(token, secret) {
  if (!token || !secret) return null;
  const [body, sig] = String(token).split(".");
  if (!body || !sig) return null;
  const expected = crypto
    .createHmac("sha256", secret)
    .update(body)
    .digest("base64url");
  if (!timingSafeEqualString(sig, expected)) return null;
  let payload;
  try {
    payload = JSON.parse(Buffer.from(body, "base64url").toString("utf8"));
  } catch {
    return null;
  }
  if (!payload?.exp || Date.now() / 1000 > payload.exp) return null;
  return payload;
}

function issueToken(secret) {
  const now = Math.floor(Date.now() / 1000);
  return signToken({ role: "recorder", iat: now, exp: now + TOKEN_TTL_SECONDS }, secret);
}

function getBearerToken(event) {
  const header =
    event.headers?.authorization ||
    event.headers?.Authorization ||
    "";
  const match = String(header).match(/^Bearer\s+(.+)$/i);
  return match ? match[1].trim() : null;
}

function requireAuth(event, secret) {
  return verifyToken(getBearerToken(event), secret);
}

module.exports = {
  TOKEN_TTL_SECONDS,
  corsHeaders,
  json,
  timingSafeEqualString,
  issueToken,
  verifyToken,
  requireAuth,
};
