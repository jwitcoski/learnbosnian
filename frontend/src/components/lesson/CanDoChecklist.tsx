import { useState } from "react";
import type { CanDoCheck } from "../../types/chapter";
import { PrimaryButton } from "./styles";

type Props = { items: CanDoCheck[] };

export default function CanDoChecklist({ items }: Props) {
  const [done, setDone] = useState<Record<string, boolean>>({});

  if (!items?.length) return null;

  const allDone = items.every((i) => done[i.id]);

  return (
    <div>
      <h2>Can-do check</h2>
      <p style={{ color: "var(--color-muted)", marginTop: 0 }}>
        Honest self-check. Mark each when you can do it without peeking.
      </p>
      <ul style={{ listStyle: "none", padding: 0 }}>
        {items.map((item) => (
          <li key={item.id} style={{ marginBottom: "0.75rem" }}>
            <label style={{ display: "flex", gap: "0.65rem", cursor: "pointer" }}>
              <input
                type="checkbox"
                checked={Boolean(done[item.id])}
                onChange={() =>
                  setDone((m) => ({ ...m, [item.id]: !m[item.id] }))
                }
                style={{ width: "auto", marginTop: 4 }}
              />
              <span>
                <strong>
                  {item.kind === "listen"
                    ? "Listen"
                    : item.kind === "write"
                    ? "Write"
                    : "Speak"}
                  :
                </strong>{" "}
                {item.prompt}
              </span>
            </label>
          </li>
        ))}
      </ul>
      {allDone ? (
        <p style={{ fontWeight: 700, color: "var(--color-sage)" }}>
          Nice. You marked every can-do for this lesson.
        </p>
      ) : (
        <PrimaryButton
          type="button"
          onClick={() => {
            const next: Record<string, boolean> = {};
            items.forEach((i) => {
              next[i.id] = true;
            });
            setDone(next);
          }}
        >
          Mark all done
        </PrimaryButton>
      )}
    </div>
  );
}
