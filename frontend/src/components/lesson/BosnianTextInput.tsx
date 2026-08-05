import { useRef } from "react";

const CHARS = ["č", "ć", "š", "ž", "đ", "Č", "Ć", "Š", "Ž", "Đ"];

type Props = {
  value: string;
  onChange: (next: string) => void;
  /** Optional id so multiple pads can coexist; unused for focus tracking via inputRef. */
  inputRef?: React.RefObject<HTMLInputElement | null>;
  placeholder?: string;
  style?: React.CSSProperties;
};

/**
 * Text input plus clickable Bosnian diacritic buttons for US/UK keyboards.
 */
export default function BosnianTextInput({
  value,
  onChange,
  placeholder,
  style,
}: Props) {
  const ref = useRef<HTMLInputElement>(null);

  const insert = (ch: string) => {
    const el = ref.current;
    if (!el) {
      onChange(value + ch);
      return;
    }
    const start = el.selectionStart ?? value.length;
    const end = el.selectionEnd ?? value.length;
    const next = value.slice(0, start) + ch + value.slice(end);
    onChange(next);
    requestAnimationFrame(() => {
      el.focus();
      const pos = start + ch.length;
      el.setSelectionRange(pos, pos);
    });
  };

  return (
    <div style={{ marginBottom: "0.35rem" }}>
      <input
        ref={ref}
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder={placeholder}
        style={{ width: "100%", ...style }}
        autoComplete="off"
        spellCheck={false}
      />
      <div
        style={{
          display: "flex",
          flexWrap: "wrap",
          gap: "0.35rem",
          marginTop: "0.4rem",
          alignItems: "center",
        }}
      >
        <span style={{ fontSize: "0.8rem", color: "var(--color-muted)" }}>
          Add accent:
        </span>
        {CHARS.map((ch) => (
          <button
            key={ch}
            type="button"
            onMouseDown={(e) => e.preventDefault()}
            onClick={() => insert(ch)}
            aria-label={`Insert ${ch}`}
            style={{
              minWidth: "2rem",
              padding: "0.25rem 0.45rem",
              border: "1px solid var(--color-brown)",
              background: "rgba(255,255,255,0.85)",
              color: "var(--color-brown)",
              fontWeight: 700,
              fontSize: "1rem",
              cursor: "pointer",
              fontFamily: "var(--font-body)",
            }}
          >
            {ch}
          </button>
        ))}
      </div>
    </div>
  );
}
