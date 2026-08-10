import { useMemo, useRef, useState } from "react";
import type { AuthenticListen } from "../../types/chapter";
import { clipAudioUrl } from "../../lib/audioClips";
import { PrimaryButton } from "./styles";

type Props = { block: AuthenticListen };

function youtubeEmbed(url?: string): string | null {
  if (!url) return null;
  try {
    const u = new URL(url);
    if (u.hostname.includes("youtu.be")) {
      const id = u.pathname.replace("/", "");
      return id ? `https://www.youtube.com/embed/${id}?rel=0` : null;
    }
    if (u.hostname.includes("youtube.com")) {
      const id = u.searchParams.get("v");
      if (id) return `https://www.youtube.com/embed/${id}?rel=0`;
      const parts = u.pathname.split("/");
      const embedIdx = parts.indexOf("embed");
      if (embedIdx >= 0 && parts[embedIdx + 1]) {
        return `https://www.youtube.com/embed/${parts[embedIdx + 1]}?rel=0`;
      }
    }
  } catch {
    return null;
  }
  return null;
}

export default function AuthenticListenPanel({ block }: Props) {
  const audioRef = useRef<HTMLAudioElement | null>(null);
  const [heard, setHeard] = useState(false);
  const [playing, setPlaying] = useState(false);
  const [loop, setLoop] = useState(true);
  const [rate, setRate] = useState(1);
  const [choice, setChoice] = useState<number | null>(null);
  const [checked, setChecked] = useState(false);
  const [revealed, setRevealed] = useState(false);
  const [heardWords, setHeardWords] = useState<Record<string, boolean>>({});

  const embed = useMemo(
    () => youtubeEmbed(block.source.embedUrl),
    [block.source.embedUrl]
  );
  const hostedUrl = block.source.clipId
    ? clipAudioUrl(block.source.clipId)
    : null;

  const markHeard = () => setHeard(true);

  const toggleHosted = async () => {
    if (!hostedUrl) return;
    if (!audioRef.current) {
      audioRef.current = new Audio(hostedUrl);
      audioRef.current.loop = loop;
      audioRef.current.playbackRate = rate;
      audioRef.current.addEventListener("ended", () => setPlaying(false));
      audioRef.current.addEventListener("play", markHeard);
    }
    const audio = audioRef.current;
    audio.loop = loop;
    audio.playbackRate = rate;
    if (!audio.paused) {
      audio.pause();
      setPlaying(false);
      return;
    }
    try {
      await audio.play();
      setPlaying(true);
      markHeard();
    } catch {
      setPlaying(false);
    }
  };

  const gist = block.listenTask.gistQuestion;
  const correct = checked && choice === gist.correctIndex;

  return (
    <div>
      <p style={{ color: "var(--color-muted)", marginTop: 0 }}>{block.hook}</p>
      <p style={{ fontSize: "0.9rem", color: "var(--color-muted)" }}>
        <strong>{block.kind === "song" ? "Song" : "Speaker"}</strong>
        {" · "}
        {block.source.artistOrSpeaker}
        {block.source.regionOrScene ? ` · ${block.source.regionOrScene}` : ""}
        {block.durationHint ? ` · focus ~${block.durationHint}` : ""}
      </p>

      {embed && (
        <div
          style={{
            position: "relative",
            paddingBottom: "56.25%",
            height: 0,
            marginBottom: "1rem",
            borderRadius: 8,
            overflow: "hidden",
            background: "#111",
          }}
        >
          <iframe
            title={block.source.title}
            src={embed}
            style={{
              position: "absolute",
              top: 0,
              left: 0,
              width: "100%",
              height: "100%",
              border: 0,
            }}
            allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
            allowFullScreen
            onLoad={markHeard}
          />
        </div>
      )}

      {hostedUrl && (
        <div style={{ marginBottom: "1rem", display: "flex", gap: "0.5rem", flexWrap: "wrap" }}>
          <PrimaryButton type="button" onClick={() => void toggleHosted()}>
            {playing ? "Pause clip" : "Play clip"}
          </PrimaryButton>
          <PrimaryButton
            type="button"
            onClick={() => {
              setLoop((v) => {
                if (audioRef.current) audioRef.current.loop = !v;
                return !v;
              });
            }}
          >
            Loop: {loop ? "on" : "off"}
          </PrimaryButton>
          {block.kind === "speaker" && (
            <PrimaryButton
              type="button"
              onClick={() => {
                const next = rate === 1 ? 0.75 : 1;
                setRate(next);
                if (audioRef.current) audioRef.current.playbackRate = next;
              }}
            >
              Speed: {rate === 1 ? "1×" : "0.75×"}
            </PrimaryButton>
          )}
        </div>
      )}

      {!embed && !hostedUrl && (
        <div style={{ marginBottom: "1rem" }}>
          <p style={{ color: "var(--color-muted)" }}>
            Open the source link, listen for about a minute, then return for the
            gist task.
          </p>
          <PrimaryButton type="button" onClick={markHeard}>
            I listened. Unlock gist
          </PrimaryButton>
        </div>
      )}

      <p>
        <a href={block.source.pageUrl} target="_blank" rel="noreferrer">
          {block.source.title}
        </a>
        {" · "}
        <span style={{ color: "var(--color-muted)", fontSize: "0.9rem" }}>
          {block.source.credit} ({block.source.license})
        </span>
      </p>

      <p style={{ fontWeight: 600 }}>{block.listenTask.prompt}</p>
      {!heard && (
        <p style={{ color: "var(--color-muted)", fontSize: "0.95rem" }}>
          Start the clip above first. The gist question unlocks after you begin
          listening.
        </p>
      )}

      {heard && (
        <div style={{ marginTop: "0.75rem" }}>
          <p>
            <strong>{gist.prompt}</strong>
          </p>
          {gist.options.map((opt, i) => (
            <label
              key={opt}
              style={{ display: "block", marginBottom: "0.35rem", cursor: "pointer" }}
            >
              <input
                type="radio"
                name="authentic-gist"
                checked={choice === i}
                onChange={() => {
                  setChoice(i);
                  setChecked(false);
                }}
                style={{ width: "auto", marginRight: "0.5rem" }}
              />
              {opt}
            </label>
          ))}
          <PrimaryButton
            type="button"
            disabled={choice === null}
            onClick={() => {
              setChecked(true);
              setRevealed(true);
            }}
          >
            Check gist
          </PrimaryButton>
          {checked && (
            <p
              style={{
                fontWeight: 700,
                color: correct ? "var(--color-sage)" : "var(--color-crimson)",
              }}
            >
              {correct ? "Correct" : `Not quite. Aim for: ${gist.options[gist.correctIndex]}`}
            </p>
          )}
        </div>
      )}

      {block.listenTask.targetWords && block.listenTask.targetWords.length > 0 && heard && (
        <div style={{ marginTop: "1rem" }}>
          <p style={{ fontWeight: 600 }}>Tap words you catch</p>
          <div style={{ display: "flex", flexWrap: "wrap", gap: "0.5rem" }}>
            {block.listenTask.targetWords.map((w) => (
              <button
                key={w}
                type="button"
                onClick={() =>
                  setHeardWords((m) => ({ ...m, [w]: !m[w] }))
                }
                style={{
                  padding: "0.35rem 0.7rem",
                  borderRadius: 6,
                  border: "1px solid var(--color-border, #ccc)",
                  background: heardWords[w]
                    ? "rgba(132, 146, 116, 0.25)"
                    : "transparent",
                  cursor: "pointer",
                }}
              >
                {w}
              </button>
            ))}
          </div>
        </div>
      )}

      {block.listenTask.noticePrompt && heard && (
        <p style={{ color: "var(--color-muted)", marginTop: "1rem" }}>
          Notice: {block.listenTask.noticePrompt}
        </p>
      )}

      {revealed && (
        <div style={{ marginTop: "1.25rem" }}>
          <h3>Key lines</h3>
          {block.reveal.keyLines.map((line) => (
            <p key={line.bosnian} style={{ marginBottom: "0.5rem" }}>
              <strong>{line.bosnian}</strong>
              <br />
              <span style={{ color: "var(--color-muted)" }}>{line.english}</span>
            </p>
          ))}
          <p>{block.reveal.teacherNote}</p>
        </div>
      )}

      {heard && !revealed && (
        <PrimaryButton
          type="button"
          onClick={() => setRevealed(true)}
          style={{ marginTop: "0.75rem" }}
        >
          Reveal key lines
        </PrimaryButton>
      )}
    </div>
  );
}
