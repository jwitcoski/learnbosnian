import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import {
  Clip,
  VoiceProfile,
  fetchClips,
  fetchVoices,
  getStoredToken,
  getStoredVoiceId,
  login,
  publicAudioUrl,
  setStoredToken,
  setStoredVoiceId,
  uploadClip,
} from "./api";
import { useRecorder } from "./useRecorder";
import {
  decodeAudioBlob,
  formatClipTime,
  trimBlobToWav,
} from "./trimAudio";

type Screen = "login" | "voice" | "home" | "day";

function formatTime(seconds: number) {
  const m = Math.floor(seconds / 60);
  const s = seconds % 60;
  return `${m}:${String(s).padStart(2, "0")}`;
}

export default function App() {
  const [screen, setScreen] = useState<Screen>(() =>
    getStoredToken() ? (getStoredVoiceId() ? "home" : "voice") : "login"
  );
  const [password, setPassword] = useState("");
  const [loginError, setLoginError] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);

  const [voices, setVoices] = useState<VoiceProfile[]>([]);
  const [voiceId, setVoiceId] = useState<string | null>(() => getStoredVoiceId());
  const [days, setDays] = useState<number[]>([]);
  const [recordedCount, setRecordedCount] = useState(0);
  const [total, setTotal] = useState(0);
  const [day, setDay] = useState<number | null>(null);
  const [clips, setClips] = useState<Clip[]>([]);
  const [filter, setFilter] = useState<"all" | "mine" | "missing">("mine");
  const [activeClipId, setActiveClipId] = useState<string | null>(null);
  const [statusMsg, setStatusMsg] = useState<string | null>(null);
  const [loadError, setLoadError] = useState<string | null>(null);

  const [duration, setDuration] = useState(0);
  const [trimStart, setTrimStart] = useState(0);
  const [trimEnd, setTrimEnd] = useState(0);
  const [trimmedUrl, setTrimmedUrl] = useState<string | null>(null);
  const [trimError, setTrimError] = useState<string | null>(null);
  const [confirmAccept, setConfirmAccept] = useState(false);

  const trimmedUrlRef = useRef<string | null>(null);
  const previewAudioRef = useRef<HTMLAudioElement | null>(null);

  const recorder = useRecorder();
  const resetRecorder = recorder.reset;
  const voice = voices.find((v) => v.id === voiceId) || null;

  const clearTrimmedUrl = useCallback(() => {
    if (trimmedUrlRef.current) {
      URL.revokeObjectURL(trimmedUrlRef.current);
      trimmedUrlRef.current = null;
    }
    setTrimmedUrl(null);
  }, []);

  const resetTake = useCallback(() => {
    clearTrimmedUrl();
    setDuration(0);
    setTrimStart(0);
    setTrimEnd(0);
    setTrimError(null);
    setConfirmAccept(false);
    resetRecorder();
  }, [clearTrimmedUrl, resetRecorder]);

  const refreshMeta = useCallback(async () => {
    const [voiceRes, clipRes] = await Promise.all([
      fetchVoices(),
      fetchClips(),
    ]);
    setVoices(voiceRes.voices);
    setDays(clipRes.days);
    setRecordedCount(clipRes.recordedCount);
    setTotal(clipRes.total);
  }, []);

  const loadDay = useCallback(
    async (d: number) => {
      setLoadError(null);
      setBusy(true);
      try {
        const res = await fetchClips({ day: d });
        setClips(res.clips);
        setDay(d);
        setScreen("day");
        setActiveClipId(null);
        resetTake();
      } catch (err) {
        setLoadError(err instanceof Error ? err.message : "Failed to load clips");
      } finally {
        setBusy(false);
      }
    },
    [resetTake]
  );

  useEffect(() => {
    if (screen === "login") return;
    refreshMeta().catch((err) => {
      setLoadError(err instanceof Error ? err.message : "Session expired");
      setStoredToken(null);
      setScreen("login");
    });
  }, [screen, refreshMeta]);

  // When a new recording lands in preview, measure duration and reset trim.
  useEffect(() => {
    if (recorder.state !== "preview" || !recorder.blob) return;
    let cancelled = false;
    clearTrimmedUrl();
    setConfirmAccept(false);
    setTrimError(null);
    decodeAudioBlob(recorder.blob)
      .then((buf) => {
        if (cancelled) return;
        const d = buf.duration;
        setDuration(d);
        setTrimStart(0);
        setTrimEnd(d);
      })
      .catch((err) => {
        if (cancelled) return;
        setTrimError(
          err instanceof Error
            ? err.message
            : "Could not decode recording for trimming"
        );
        // Fall back: allow full take without trim metadata
        setDuration(0);
        setTrimStart(0);
        setTrimEnd(0);
      });
    return () => {
      cancelled = true;
    };
  }, [recorder.state, recorder.blob, clearTrimmedUrl]);

  // Rebuild trimmed preview when handles move.
  useEffect(() => {
    if (recorder.state !== "preview" || !recorder.blob || duration <= 0) return;
    let cancelled = false;
    const handle = window.setTimeout(() => {
      trimBlobToWav(recorder.blob!, {
        startSec: trimStart,
        endSec: trimEnd,
      })
        .then(({ blob }) => {
          if (cancelled) return;
          if (trimmedUrlRef.current) URL.revokeObjectURL(trimmedUrlRef.current);
          const url = URL.createObjectURL(blob);
          trimmedUrlRef.current = url;
          setTrimmedUrl(url);
          setTrimError(null);
        })
        .catch((err) => {
          if (cancelled) return;
          setTrimError(
            err instanceof Error ? err.message : "Could not trim recording"
          );
        });
    }, 180);
    return () => {
      cancelled = true;
      window.clearTimeout(handle);
    };
  }, [recorder.state, recorder.blob, duration, trimStart, trimEnd]);

  useEffect(() => () => clearTrimmedUrl(), [clearTrimmedUrl]);

  const onLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoginError(null);
    setBusy(true);
    try {
      const res = await login(password);
      setStoredToken(res.token);
      setPassword("");
      setScreen(getStoredVoiceId() ? "home" : "voice");
    } catch (err) {
      setLoginError(err instanceof Error ? err.message : "Login failed");
    } finally {
      setBusy(false);
    }
  };

  const logout = () => {
    setStoredToken(null);
    setScreen("login");
    setClips([]);
    setDay(null);
    resetTake();
  };

  const pickVoice = (id: string) => {
    setVoiceId(id);
    setStoredVoiceId(id);
    setScreen("home");
  };

  const visibleClips = useMemo(() => {
    return clips.filter((c) => {
      if (filter === "missing") return !c.recorded;
      if (filter === "mine" && voice) {
        const genderOk =
          c.preferredGender === "any" || c.preferredGender === voice.gender;
        return genderOk && !c.recorded;
      }
      return true;
    });
  }, [clips, filter, voice]);

  const activeClip = clips.find((c) => c.id === activeClipId) || null;

  const playTrimmed = () => {
    const el = previewAudioRef.current;
    if (!el) return;
    el.currentTime = 0;
    void el.play();
  };

  const onAcceptUpload = async () => {
    if (!activeClip || !voice || !recorder.blob) return;
    setStatusMsg(null);
    setBusy(true);
    try {
      let blob = recorder.blob;
      if (duration > 0 && (trimStart > 0.01 || trimEnd < duration - 0.01)) {
        const trimmed = await trimBlobToWav(recorder.blob, {
          startSec: trimStart,
          endSec: trimEnd,
        });
        blob = trimmed.blob;
      } else if (duration > 0) {
        // Normalize accepted takes to WAV when we could decode them
        const trimmed = await trimBlobToWav(recorder.blob, {
          startSec: 0,
          endSec: duration,
        });
        blob = trimmed.blob;
      }
      await uploadClip({
        clipId: activeClip.id,
        voiceId: voice.id,
        blob,
      });
      setStatusMsg("Accepted & uploaded to S3 — thanks!");
      setConfirmAccept(false);
      resetTake();
      await loadDay(activeClip.day);
      await refreshMeta();
    } catch (err) {
      setStatusMsg(err instanceof Error ? err.message : "Upload failed");
      setConfirmAccept(false);
    } finally {
      setBusy(false);
    }
  };

  if (screen === "login") {
    return (
      <div className="shell">
        <header className="top">
          <p className="eyebrow">Private</p>
          <h1>Voice Recorder</h1>
          <p className="lede">
            Record Bosnian vocab and dialogue takes for Learn Bosnian. iPhone:
            use Safari and allow the microphone.
          </p>
        </header>
        <form className="card" onSubmit={onLogin}>
          <label htmlFor="password">Shared password</label>
          <input
            id="password"
            type="password"
            autoComplete="current-password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
          {loginError && <p className="error">{loginError}</p>}
          <button type="submit" className="primary" disabled={busy}>
            {busy ? "Checking…" : "Enter studio"}
          </button>
        </form>
      </div>
    );
  }

  if (screen === "voice") {
    return (
      <div className="shell">
        <header className="top">
          <p className="eyebrow">Step 1</p>
          <h1>Which voice are you recording?</h1>
          <p className="lede">
            Female 1 covers all vocabulary. Male 1 covers male dialogue. Female 2
            and Male 2 are extras when a second take is needed.
          </p>
        </header>
        <div className="voice-grid">
          {voices.map((v) => (
            <button
              key={v.id}
              type="button"
              className="voice-card"
              onClick={() => pickVoice(v.id)}
            >
              <span className="voice-name">{v.displayName}</span>
              <span className="voice-meta">
                {v.gender}
                {v.role === "backup" ? " · backup" : " · primary"}
              </span>
              {v.description && <span className="voice-desc">{v.description}</span>}
            </button>
          ))}
        </div>
        <button type="button" className="ghost" onClick={logout}>
          Log out
        </button>
      </div>
    );
  }

  return (
    <div className="shell">
      <header className="top row">
        <div>
          <p className="eyebrow">Learn Bosnian</p>
          <h1>Voice studio</h1>
        </div>
        <button type="button" className="ghost" onClick={logout}>
          Log out
        </button>
      </header>

      <section className="card">
        <label htmlFor="voice">Recording as</label>
        <select
          id="voice"
          value={voiceId || ""}
          onChange={(e) => {
            if (!e.target.value) {
              setVoiceId(null);
              setStoredVoiceId(null);
              setScreen("voice");
              return;
            }
            setVoiceId(e.target.value);
            setStoredVoiceId(e.target.value);
          }}
        >
          <option value="">Choose a voice…</option>
          {voices.map((v) => (
            <option key={v.id} value={v.id}>
              {v.displayName}
            </option>
          ))}
        </select>
        {voice?.description && <p className="meta">{voice.description}</p>}
        <p className="meta">
          {recordedCount}/{total} clips uploaded · Female 1 = vocab · Male 1 =
          male parts · F2/M2 if needed
        </p>
        <button
          type="button"
          className="ghost linkish"
          onClick={() => setScreen("voice")}
        >
          Change voice role
        </button>
      </section>

      {loadError && <p className="error banner">{loadError}</p>}

      {screen === "home" && (
        <section className="day-grid">
          {days.map((d) => (
            <button
              key={d}
              type="button"
              className="day-tile"
              onClick={() => loadDay(d)}
              disabled={busy || !voice}
            >
              <span className="daynum">Lesson {d}</span>
              <span className="hint">Open script</span>
            </button>
          ))}
        </section>
      )}

      {screen === "day" && day != null && (
        <>
          <div className="row toolbar">
            <button
              type="button"
              className="ghost"
              onClick={() => {
                setScreen("home");
                setDay(null);
                setActiveClipId(null);
                resetTake();
              }}
            >
              ← Lessons
            </button>
            <h2>Lesson {day}</h2>
          </div>

          <div className="filters">
            {(
              [
                ["mine", "My missing"],
                ["missing", "All missing"],
                ["all", "All clips"],
              ] as const
            ).map(([id, label]) => (
              <button
                key={id}
                type="button"
                className={filter === id ? "chip on" : "chip"}
                onClick={() => setFilter(id)}
              >
                {label}
              </button>
            ))}
          </div>

          <ul className="clip-list">
            {visibleClips.map((c) => (
              <li key={c.id}>
                <button
                  type="button"
                  className={
                    activeClipId === c.id ? "clip-card active" : "clip-card"
                  }
                  onClick={() => {
                    setActiveClipId(c.id);
                    setStatusMsg(null);
                    resetTake();
                  }}
                >
                  <div className="clip-top">
                    <span className="tag">{c.type}</span>
                    {c.recorded ? (
                      <span className="ok">Recorded</span>
                    ) : (
                      <span className="todo">Needed</span>
                    )}
                  </div>
                  {c.speaker && (
                    <div className="speaker">
                      {c.speaker}
                      {c.preferredGender !== "any" && (
                        <span> · prefer {c.preferredGender}</span>
                      )}
                    </div>
                  )}
                  {!c.speaker && c.type === "vocab" && (
                    <div className="speaker">Vocab · Female 1</div>
                  )}
                  <div className="bs">{c.bosnian}</div>
                  <div className="en">{c.english}</div>
                </button>
              </li>
            ))}
            {visibleClips.length === 0 && (
              <li className="meta empty">Nothing in this filter.</li>
            )}
          </ul>
        </>
      )}

      {activeClip && (
        <section className="recorder card sticky">
          <p className="eyebrow">Now recording</p>
          <h3>{activeClip.bosnian}</h3>
          <p className="en">{activeClip.english}</p>
          {activeClip.pronunciation && (
            <p className="pron">{activeClip.pronunciation}</p>
          )}

          {activeClip.recorded && activeClip.s3Key && (
            <audio
              className="player"
              controls
              preload="none"
              src={publicAudioUrl(activeClip.s3Key)}
            />
          )}

          {recorder.state === "recording" && (
            <p className="rec-live">Recording… {formatTime(recorder.seconds)}</p>
          )}

          {recorder.state === "preview" && (
            <div className="trim-panel">
              <p className="meta trim-label">
                Clip beginning &amp; end
                {duration > 0 && (
                  <>
                    {" "}
                    · keep {formatClipTime(Math.max(0, trimEnd - trimStart))} of{" "}
                    {formatClipTime(duration)}
                  </>
                )}
              </p>

              {duration > 0 && (
                <>
                  <label htmlFor="trim-start">
                    Start {formatClipTime(trimStart)}
                  </label>
                  <input
                    id="trim-start"
                    type="range"
                    min={0}
                    max={Math.max(0, duration - 0.05)}
                    step={0.05}
                    value={trimStart}
                    onChange={(e) => {
                      const next = Number(e.target.value);
                      setTrimStart(Math.min(next, trimEnd - 0.05));
                      setConfirmAccept(false);
                    }}
                  />
                  <label htmlFor="trim-end">
                    End {formatClipTime(trimEnd)}
                  </label>
                  <input
                    id="trim-end"
                    type="range"
                    min={0.05}
                    max={duration}
                    step={0.05}
                    value={trimEnd}
                    onChange={(e) => {
                      const next = Number(e.target.value);
                      setTrimEnd(Math.max(next, trimStart + 0.05));
                      setConfirmAccept(false);
                    }}
                  />
                </>
              )}

              {(trimmedUrl || recorder.previewUrl) && (
                <audio
                  ref={previewAudioRef}
                  className="player"
                  controls
                  src={trimmedUrl || recorder.previewUrl || undefined}
                />
              )}

              {trimError && <p className="error">{trimError}</p>}
            </div>
          )}

          {recorder.error && <p className="error">{recorder.error}</p>}
          {statusMsg && <p className="status">{statusMsg}</p>}

          <div className="actions">
            {recorder.state === "idle" && (
              <button
                type="button"
                className="primary"
                onClick={recorder.start}
                disabled={busy || !voice}
              >
                Record
              </button>
            )}
            {recorder.state === "recording" && (
              <button type="button" className="danger" onClick={recorder.stop}>
                Stop
              </button>
            )}
            {recorder.state === "preview" && !confirmAccept && (
              <>
                <button
                  type="button"
                  className="primary"
                  onClick={playTrimmed}
                  disabled={!trimmedUrl && !recorder.previewUrl}
                >
                  Play back
                </button>
                <button
                  type="button"
                  className="primary accept"
                  onClick={() => setConfirmAccept(true)}
                  disabled={busy || !voice}
                >
                  Accept this take?
                </button>
                <button
                  type="button"
                  className="ghost"
                  onClick={resetTake}
                  disabled={busy}
                >
                  Re-record
                </button>
              </>
            )}
            {recorder.state === "preview" && confirmAccept && (
              <>
                <p className="confirm-copy">
                  Accept this clipped take and upload it to S3 for the lesson
                  site?
                </p>
                <button
                  type="button"
                  className="primary accept"
                  onClick={onAcceptUpload}
                  disabled={busy || !voice}
                >
                  {busy ? "Uploading…" : "Yes — upload to S3"}
                </button>
                <button
                  type="button"
                  className="ghost"
                  onClick={() => setConfirmAccept(false)}
                  disabled={busy}
                >
                  Not yet
                </button>
              </>
            )}
          </div>
        </section>
      )}
    </div>
  );
}
