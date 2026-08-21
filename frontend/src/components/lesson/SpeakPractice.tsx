import { useCallback, useEffect, useRef, useState } from "react";
import { pickRecorderMimeType } from "./recorderMime";
import { PrimaryButton } from "./styles";
import {
  requestSpeakCheckUpload,
  runSpeakCheck,
  SpeakCheckResult,
} from "../../lib/speakCheckApi";

export type SpeakPracticeProps = {
  day: number;
  lineIndex: number;
  bosnian: string;
  english: string;
  vocabulary?: string[];
  aiEnabled?: boolean;
  attemptsLeft: number;
  onAiAttempt: () => void;
};

export default function SpeakPractice({
  day,
  lineIndex,
  bosnian,
  english,
  vocabulary = [],
  aiEnabled = true,
  attemptsLeft,
  onAiAttempt,
}: SpeakPracticeProps) {
  const [recording, setRecording] = useState(false);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const [blob, setBlob] = useState<Blob | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);
  const [feedback, setFeedback] = useState<SpeakCheckResult | null>(null);

  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const chunksRef = useRef<BlobPart[]>([]);
  const streamRef = useRef<MediaStream | null>(null);
  const previewRef = useRef<string | null>(null);

  const cleanup = useCallback(() => {
    streamRef.current?.getTracks().forEach((t) => t.stop());
    streamRef.current = null;
  }, []);

  useEffect(
    () => () => {
      cleanup();
      if (previewRef.current) URL.revokeObjectURL(previewRef.current);
    },
    [cleanup]
  );

  const start = async () => {
    setError(null);
    setFeedback(null);
    if (previewRef.current) {
      URL.revokeObjectURL(previewRef.current);
      previewRef.current = null;
    }
    setPreviewUrl(null);
    setBlob(null);
    try {
      if (!navigator.mediaDevices?.getUserMedia) {
        throw new Error(
          "This browser can’t use your microphone. Try Chrome or Safari, or check site permissions."
        );
      }
      const stream = await navigator.mediaDevices.getUserMedia({
        audio: {
          echoCancellation: true,
          noiseSuppression: true,
          autoGainControl: true,
        },
      });
      streamRef.current = stream;
      const mimeType = pickRecorderMimeType();
      const recorder = mimeType
        ? new MediaRecorder(stream, { mimeType })
        : new MediaRecorder(stream);
      mediaRecorderRef.current = recorder;
      chunksRef.current = [];
      recorder.ondataavailable = (e) => {
        if (e.data.size > 0) chunksRef.current.push(e.data);
      };
      recorder.onstop = () => {
        cleanup();
        const type = recorder.mimeType || "audio/webm";
        const b = new Blob(chunksRef.current, { type });
        const url = URL.createObjectURL(b);
        previewRef.current = url;
        setBlob(b);
        setPreviewUrl(url);
        setRecording(false);
      };
      recorder.start();
      setRecording(true);
      window.setTimeout(() => {
        if (mediaRecorderRef.current?.state === "recording") {
          mediaRecorderRef.current.stop();
        }
      }, 8000);
    } catch (err) {
      cleanup();
      setError(err instanceof Error ? err.message : "Could not record");
      setRecording(false);
    }
  };

  const stop = () => {
    if (mediaRecorderRef.current?.state === "recording") {
      mediaRecorderRef.current.stop();
    }
  };

  const checkWithAi = async () => {
    if (!blob || attemptsLeft <= 0 || !aiEnabled) return;
    setBusy(true);
    setError(null);
    setFeedback(null);
    try {
      onAiAttempt();
      const { uploadUrl, s3Key, contentType } = await requestSpeakCheckUpload(
        blob.type || "audio/webm"
      );
      const put = await fetch(uploadUrl, {
        method: "PUT",
        headers: { "Content-Type": contentType },
        body: blob,
      });
      if (!put.ok) throw new Error(`Upload failed (${put.status})`);
      const result = await runSpeakCheck({
        s3Key,
        day,
        lineIndex,
        target: bosnian,
        english,
        vocabulary,
      });
      setFeedback(result);
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : "Speak Check is unavailable right now. Listen to the teacher audio and compare by ear."
      );
    } finally {
      setBusy(false);
    }
  };

  return (
    <div style={{ marginTop: "0.65rem" }}>
      <div
        style={{
          display: "flex",
          flexWrap: "wrap",
          gap: "0.5rem",
        }}
      >
        {!recording ? (
          <PrimaryButton type="button" onClick={() => void start()}>
            Record yourself
          </PrimaryButton>
        ) : (
          <PrimaryButton type="button" onClick={stop}>
            Stop
          </PrimaryButton>
        )}
        {previewUrl && (
          <PrimaryButton
            type="button"
            onClick={() => {
              const a = new Audio(previewUrl);
              void a.play();
            }}
          >
            Play my take
          </PrimaryButton>
        )}
        {aiEnabled && blob && (
          <PrimaryButton
            type="button"
            onClick={() => void checkWithAi()}
            disabled={busy || attemptsLeft <= 0}
          >
            {busy
              ? "Checking…"
              : attemptsLeft > 0
              ? `Speak Check (${attemptsLeft} left)`
              : "Speak Check used up"}
          </PrimaryButton>
        )}
      </div>
      {recording && (
        <p style={{ fontSize: "0.9rem", color: "var(--color-muted)" }}>
          Recording (max 8 seconds)…
        </p>
      )}
      {error && (
        <p style={{ color: "var(--color-crimson)", fontWeight: 600 }}>{error}</p>
      )}
      {feedback && (
        <div style={{ marginTop: "0.75rem" }}>
          <p style={{ marginBottom: "0.35rem" }}>
            <strong>Heard:</strong> {feedback.heard || "(unclear)"}
          </p>
          <p style={{ marginBottom: "0.35rem" }}>
            <strong>Target:</strong> {feedback.target}
          </p>
          {feedback.fixes?.length > 0 && (
            <ul style={{ margin: "0.35rem 0" }}>
              {feedback.fixes.map((f) => (
                <li key={f}>{f}</li>
              ))}
            </ul>
          )}
          {feedback.encourage && (
            <p style={{ color: "var(--color-sage)", fontWeight: 600 }}>
              {feedback.encourage}
            </p>
          )}
        </div>
      )}
      {aiEnabled && !feedback && (
        <p
          style={{
            marginTop: "0.5rem",
            fontSize: "0.75rem",
            color: "var(--color-muted)",
          }}
        >
          Speak Check listens to your recording and sends back short tips.
        </p>
      )}
    </div>
  );
}
