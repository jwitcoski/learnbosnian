export type VoiceProfile = {
  id: string;
  displayName: string;
  gender: "female" | "male";
  role?: "primary" | "backup";
  description?: string;
};

export type Clip = {
  id: string;
  book: number;
  day: number;
  type: "vocab" | "dialogue";
  index: number;
  bosnian: string;
  english: string;
  pronunciation?: string;
  preferredGender: "female" | "male" | "any";
  /** Exact voice talent who owns this clip (exclusive queue). */
  assignedVoiceId: string;
  speaker: string | null;
  s3Key: string;
  recorded: boolean;
  recording: {
    clipId: string;
    voiceId: string | null;
    contentType: string | null;
    updatedAt: string | null;
  } | null;
};

const TOKEN_KEY = "lb-recorder-token";
const VOICE_KEY = "lb-recorder-voice";

function apiBase() {
  const base = import.meta.env.VITE_AUDIO_API_URL || "";
  return base.replace(/\/$/, "");
}

export function getStoredToken() {
  return localStorage.getItem(TOKEN_KEY);
}

export function setStoredToken(token: string | null) {
  if (token) localStorage.setItem(TOKEN_KEY, token);
  else localStorage.removeItem(TOKEN_KEY);
}

export function getStoredVoiceId() {
  return localStorage.getItem(VOICE_KEY);
}

export function setStoredVoiceId(voiceId: string | null) {
  if (voiceId) localStorage.setItem(VOICE_KEY, voiceId);
  else localStorage.removeItem(VOICE_KEY);
}

async function api<T>(
  path: string,
  options: RequestInit = {},
  authed = true
): Promise<T> {
  const headers = new Headers(options.headers || {});
  if (!headers.has("Content-Type") && options.body) {
    headers.set("Content-Type", "application/json");
  }
  if (authed) {
    const token = getStoredToken();
    if (token) headers.set("Authorization", `Bearer ${token}`);
  }
  const res = await fetch(`${apiBase()}${path}`, { ...options, headers });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) {
    throw new Error(data.error || `Request failed (${res.status})`);
  }
  return data as T;
}

export function login(password: string) {
  return api<{ token: string }>("/audio/login", {
    method: "POST",
    body: JSON.stringify({ password }),
  }, false);
}

export function fetchClips(params: {
  day?: number;
  type?: string;
  gender?: string;
} = {}) {
  const q = new URLSearchParams();
  if (params.day != null) q.set("day", String(params.day));
  if (params.type) q.set("type", params.type);
  if (params.gender) q.set("gender", params.gender);
  const qs = q.toString();
  return api<{
    clips: Clip[];
    days: number[];
    total: number;
    recordedCount: number;
  }>(`/audio/clips${qs ? `?${qs}` : ""}`);
}

export function fetchVoices() {
  return api<{ voices: VoiceProfile[] }>("/audio/voices");
}

export async function uploadClip(opts: {
  clipId: string;
  voiceId: string;
  blob: Blob;
}) {
  const contentType = opts.blob.type || "audio/mp4";
  const signed = await api<{
    uploadUrl: string;
    s3Key: string;
    clipId: string;
  }>("/audio/upload-url", {
    method: "POST",
    body: JSON.stringify({
      clipId: opts.clipId,
      voiceId: opts.voiceId,
      contentType,
    }),
  });

  const put = await fetch(signed.uploadUrl, {
    method: "PUT",
    headers: { "Content-Type": contentType },
    body: opts.blob,
  });
  if (!put.ok) {
    throw new Error(`S3 upload failed (${put.status})`);
  }

  await api("/audio/complete", {
    method: "POST",
    body: JSON.stringify({
      clipId: opts.clipId,
      voiceId: opts.voiceId,
      contentType,
      s3Key: signed.s3Key,
    }),
  });

  return signed;
}

export function publicAudioUrl(s3Key: string) {
  const base = (import.meta.env.VITE_AUDIO_PUBLIC_BASE || "").replace(/\/$/, "");
  return `${base}/${s3Key.replace(/^\//, "")}`;
}

/** Pick best MediaRecorder MIME type for iPhone Safari + desktop. */
export function pickRecorderMimeType(): string | undefined {
  if (typeof MediaRecorder === "undefined") return undefined;
  const candidates = [
    "audio/mp4",
    "audio/mp4;codecs=mp4a.40.2",
    "audio/aac",
    "audio/webm;codecs=opus",
    "audio/webm",
  ];
  return candidates.find((t) => MediaRecorder.isTypeSupported(t));
}
