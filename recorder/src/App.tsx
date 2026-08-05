import { useCallback, useEffect, useMemo, useState } from "react";
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

type Screen = "login" | "home" | "day";

function formatTime(seconds: number) {
  const m = Math.floor(seconds / 60);
  const s = seconds % 60;
  return `${m}:${String(s).padStart(2, "0")}`;
}

export default function App() {
  const [screen, setScreen] = useState<Screen>(() =>
    getStoredToken() ? "home" : "login"
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

  const recorder = useRecorder();
  const voice = voices.find((v) => v.id === voiceId) || null;

  const refreshMeta = useCallback(async () => {
    const [voiceRes, clipRes] = await Promise.all([
      fetchVoices(),
      fetchClips(),
    ]);
    setVoices(voiceRes.voices);
    setDays(clipRes.days);
    setRecordedCount(clipRes.recordedCount);
    setTotal(clipRes.total);
    if (!voiceId && voiceRes.voices[0]) {
      setVoiceId(voiceRes.voices[0].id);
      setStoredVoiceId(voiceRes.voices[0].id);
    }
  }, [voiceId]);

  const resetRecorder = recorder.reset;

  const loadDay = useCallback(async (d: number) => {
    setLoadError(null);
    setBusy(true);
    try {
      const res = await fetchClips({ day: d });
      setClips(res.clips);
      setDay(d);
      setScreen("day");
      setActiveClipId(null);
      resetRecorder();
    } catch (err) {
      setLoadError(err instanceof Error ? err.message : "Failed to load clips");
    } finally {
      setBusy(false);
    }
  }, [resetRecorder]);

  useEffect(() => {
    if (screen === "login") return;
    refreshMeta().catch((err) => {
      setLoadError(err instanceof Error ? err.message : "Session expired");
      setStoredToken(null);
      setScreen("login");
    });
  }, [screen, refreshMeta]);

  const onLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoginError(null);
    setBusy(true);
    try {
      const res = await login(password);
      setStoredToken(res.token);
      setPassword("");
      setScreen("home");
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

  const onUpload = async () => {
    if (!activeClip || !voice || !recorder.blob) return;
    setStatusMsg(null);
    setBusy(true);
    try {
      await uploadClip({
        clipId: activeClip.id,
        voiceId: voice.id,
        blob: recorder.blob,
      });
      setStatusMsg("Uploaded — thanks!");
      recorder.reset();
      await loadDay(activeClip.day);
      await refreshMeta();
    } catch (err) {
      setStatusMsg(err instanceof Error ? err.message : "Upload failed");
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
            setVoiceId(e.target.value);
            setStoredVoiceId(e.target.value);
          }}
        >
          {voices.map((v) => (
            <option key={v.id} value={v.id}>
              {v.displayName} ({v.gender})
            </option>
          ))}
        </select>
        <p className="meta">
          {recordedCount}/{total} clips uploaded · 2 female + 2 male voices
        </p>
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
              disabled={busy}
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
                recorder.reset();
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
                    recorder.reset();
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

          {recorder.previewUrl && (
            <audio className="player" controls src={recorder.previewUrl} />
          )}

          {recorder.error && <p className="error">{recorder.error}</p>}
          {statusMsg && <p className="status">{statusMsg}</p>}

          <div className="actions">
            {recorder.state === "idle" && (
              <button
                type="button"
                className="primary"
                onClick={recorder.start}
                disabled={busy}
              >
                Hold mic · Start
              </button>
            )}
            {recorder.state === "recording" && (
              <button type="button" className="danger" onClick={recorder.stop}>
                Stop
              </button>
            )}
            {recorder.state === "preview" && (
              <>
                <button
                  type="button"
                  className="primary"
                  onClick={onUpload}
                  disabled={busy || !voice}
                >
                  {busy ? "Uploading…" : "Upload to S3"}
                </button>
                <button
                  type="button"
                  className="ghost"
                  onClick={recorder.reset}
                  disabled={busy}
                >
                  Re-record
                </button>
              </>
            )}
          </div>
        </section>
      )}
    </div>
  );
}
