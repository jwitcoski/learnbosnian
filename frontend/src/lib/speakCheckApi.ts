export type SpeakCheckResult = {
  verdict: "pass" | "retry" | "unclear";
  heard: string;
  target: string;
  fixes: string[];
  encourage?: string;
};

function apiBase() {
  return (
    process.env.REACT_APP_AUDIO_API_URL ||
    process.env.REACT_APP_SPEAK_API_URL ||
    ""
  ).replace(/\/$/, "");
}

export async function requestSpeakCheckUpload(contentType: string): Promise<{
  uploadUrl: string;
  s3Key: string;
  contentType: string;
}> {
  const base = apiBase();
  if (!base) {
    throw new Error(
      "Speak check API is not configured (REACT_APP_AUDIO_API_URL)."
    );
  }
  const res = await fetch(`${base}/speak-check/upload-url`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ contentType }),
  });
  if (!res.ok) {
    const body = await res.json().catch(() => ({}));
    throw new Error(body.error || `Upload URL failed (${res.status})`);
  }
  return res.json();
}

export async function runSpeakCheck(payload: {
  s3Key: string;
  day: number;
  lineIndex: number;
  target: string;
  english: string;
  vocabulary?: string[];
}): Promise<SpeakCheckResult> {
  const base = apiBase();
  if (!base) {
    throw new Error(
      "Speak check API is not configured (REACT_APP_AUDIO_API_URL)."
    );
  }
  const res = await fetch(`${base}/speak-check`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  if (!res.ok) {
    const body = await res.json().catch(() => ({}));
    throw new Error(body.error || `Speak check failed (${res.status})`);
  }
  return res.json();
}
