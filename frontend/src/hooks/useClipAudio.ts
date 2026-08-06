import { useCallback, useEffect, useRef, useState } from "react";
import { clipAudioUrl } from "../lib/audioClips";

/**
 * Play a voice-over clip from the public audio CDN.
 * Missing clips fail quietly (no toast) so unpublished audio is fine.
 */
export function useClipAudio() {
  const audioRef = useRef<HTMLAudioElement | null>(null);
  const [playingId, setPlayingId] = useState<string | null>(null);
  const [missing, setMissing] = useState<Record<string, true>>({});

  useEffect(() => {
    const audio = new Audio();
    audio.preload = "none";
    audioRef.current = audio;

    const onEnded = () => setPlayingId(null);
    const onPause = () => {
      if (audio.ended || audio.paused) setPlayingId(null);
    };
    audio.addEventListener("ended", onEnded);
    audio.addEventListener("pause", onPause);
    return () => {
      audio.pause();
      audio.removeEventListener("ended", onEnded);
      audio.removeEventListener("pause", onPause);
      audioRef.current = null;
    };
  }, []);

  const playClip = useCallback(
    (clipId: string) => {
      const audio = audioRef.current;
      if (!audio || missing[clipId]) return;

      if (playingId === clipId && !audio.paused) {
        audio.pause();
        setPlayingId(null);
        return;
      }

      const url = clipAudioUrl(clipId);
      audio.pause();
      audio.src = url;
      setPlayingId(clipId);
      void audio.play().catch(() => {
        setMissing((m) => ({ ...m, [clipId]: true }));
        setPlayingId(null);
      });
    },
    [missing, playingId]
  );

  return { playClip, playingId, missing };
}
