import { useCallback, useEffect, useRef, useState } from "react";
import { clipAudioUrl } from "../lib/audioClips";

export type ClipPlayOptions = {
  loop?: boolean;
  rate?: number;
};

/**
 * Play a voice-over clip from the public audio CDN.
 * Missing clips fail quietly (no toast) so unpublished audio is fine.
 * Supports optional loop and playbackRate for listen tasks / shadowing.
 */
export function useClipAudio() {
  const audioRef = useRef<HTMLAudioElement | null>(null);
  const [playingId, setPlayingId] = useState<string | null>(null);
  const [missing, setMissing] = useState<Record<string, true>>({});
  const [rate, setRate] = useState(1);
  const [loop, setLoop] = useState(false);

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
    (clipId: string, opts?: ClipPlayOptions) => {
      const audio = audioRef.current;
      if (!audio || missing[clipId]) return;

      if (playingId === clipId && !audio.paused) {
        audio.pause();
        setPlayingId(null);
        return;
      }

      const nextRate = opts?.rate ?? rate;
      const nextLoop = opts?.loop ?? loop;
      const url = clipAudioUrl(clipId);
      audio.pause();
      audio.src = url;
      audio.playbackRate = nextRate;
      audio.loop = nextLoop;
      setPlayingId(clipId);
      void audio.play().catch(() => {
        setMissing((m) => ({ ...m, [clipId]: true }));
        setPlayingId(null);
      });
    },
    [missing, playingId, rate, loop]
  );

  const setPlaybackRate = useCallback((next: number) => {
    setRate(next);
    if (audioRef.current) audioRef.current.playbackRate = next;
  }, []);

  const setLooping = useCallback((next: boolean) => {
    setLoop(next);
    if (audioRef.current) audioRef.current.loop = next;
  }, []);

  return {
    playClip,
    playingId,
    missing,
    rate,
    loop,
    setPlaybackRate,
    setLooping,
  };
}
