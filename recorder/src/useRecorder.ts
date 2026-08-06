import { useCallback, useEffect, useRef, useState } from "react";
import { pickRecorderMimeType } from "./api";

export type RecorderState = "idle" | "recording" | "preview";

export function useRecorder() {
  const [state, setState] = useState<RecorderState>("idle");
  const [error, setError] = useState<string | null>(null);
  const [blob, setBlob] = useState<Blob | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const [seconds, setSeconds] = useState(0);

  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const chunksRef = useRef<BlobPart[]>([]);
  const streamRef = useRef<MediaStream | null>(null);
  const timerRef = useRef<number | null>(null);
  const previewUrlRef = useRef<string | null>(null);

  const cleanupStream = useCallback(() => {
    streamRef.current?.getTracks().forEach((t) => t.stop());
    streamRef.current = null;
  }, []);

  const reset = useCallback(() => {
    if (mediaRecorderRef.current?.state === "recording") {
      mediaRecorderRef.current.stop();
    }
    if (timerRef.current) window.clearInterval(timerRef.current);
    timerRef.current = null;
    cleanupStream();
    if (previewUrlRef.current) {
      URL.revokeObjectURL(previewUrlRef.current);
      previewUrlRef.current = null;
    }
    setPreviewUrl(null);
    setBlob(null);
    setSeconds(0);
    setError(null);
    setState("idle");
  }, [cleanupStream]);

  useEffect(() => () => reset(), [reset]);

  const start = useCallback(async () => {
    setError(null);
    if (previewUrlRef.current) {
      URL.revokeObjectURL(previewUrlRef.current);
      previewUrlRef.current = null;
    }
    setPreviewUrl(null);
    setBlob(null);

    try {
      if (!navigator.mediaDevices?.getUserMedia) {
        throw new Error("Microphone access is not available in this browser.");
      }
      if (typeof MediaRecorder === "undefined") {
        throw new Error(
          "Recording is not supported here. On iPhone use Safari (iOS 14.3+)."
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
        const type = recorder.mimeType || mimeType || "audio/mp4";
        const next = new Blob(chunksRef.current, { type });
        const url = URL.createObjectURL(next);
        previewUrlRef.current = url;
        setBlob(next);
        setPreviewUrl(url);
        setState("preview");
        cleanupStream();
        if (timerRef.current) window.clearInterval(timerRef.current);
        timerRef.current = null;
      };

      recorder.start(250);
      setState("recording");
      setSeconds(0);
      timerRef.current = window.setInterval(() => {
        setSeconds((s) => s + 1);
      }, 1000);
    } catch (err) {
      cleanupStream();
      setState("idle");
      setError(err instanceof Error ? err.message : "Could not start recording");
    }
  }, [cleanupStream]);

  const stop = useCallback(() => {
    const recorder = mediaRecorderRef.current;
    if (recorder && recorder.state === "recording") {
      recorder.stop();
    }
  }, []);

  return {
    state,
    error,
    blob,
    previewUrl,
    seconds,
    start,
    stop,
    reset,
  };
}
