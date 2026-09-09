#!/usr/bin/env python3
"""Faithful grid low-poly pass from a source photo (no invented content)."""
from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw


def polygonize(
    source: Path,
    dest: Path,
    *,
    max_edge: int = 1400,
    cols: int = 56,
    rows: int = 42,
) -> None:
    im = Image.open(source).convert("RGB")
    im.thumbnail((max_edge, max_edge), Image.Resampling.LANCZOS)
    arr = np.asarray(im)
    h, w = arr.shape[:2]
    out = Image.new("RGB", (w, h), (255, 255, 255))
    draw = ImageDraw.Draw(out)

    def cell_color(x0: int, y0: int, x1: int, y1: int) -> tuple[int, int, int]:
        patch = arr[y0:y1, x0:x1]
        if patch.size == 0:
            return (0, 0, 0)
        mean = patch.reshape(-1, 3).mean(axis=0).astype(np.uint8)
        return int(mean[0]), int(mean[1]), int(mean[2])

    for gy in range(rows):
        for gx in range(cols):
            x0 = gx * w // cols
            x1 = (gx + 1) * w // cols
            y0 = gy * h // rows
            y1 = (gy + 1) * h // rows
            color = cell_color(x0, y0, x1, y1)
            cx = (x0 + x1) // 2
            cy = (y0 + y1) // 2
            if (gx + gy) % 2 == 0:
                draw.polygon([(x0, y0), (x1, y0), (cx, cy)], fill=color)
                draw.polygon([(x1, y0), (x1, y1), (cx, cy)], fill=color)
                draw.polygon([(x1, y1), (x0, y1), (cx, cy)], fill=color)
                draw.polygon([(x0, y1), (x0, y0), (cx, cy)], fill=color)
            else:
                draw.polygon([(x0, y0), (x1, y0), (x1, y1)], fill=color)
                draw.polygon([(x0, y0), (x1, y1), (x0, y1)], fill=color)

    dest.parent.mkdir(parents=True, exist_ok=True)
    out.save(dest, format="PNG", optimize=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source")
    parser.add_argument("dest")
    parser.add_argument("--cols", type=int, default=56)
    parser.add_argument("--rows", type=int, default=42)
    args = parser.parse_args()
    polygonize(
        Path(args.source),
        Path(args.dest),
        cols=args.cols,
        rows=args.rows,
    )
    print(f"wrote {args.dest}")


if __name__ == "__main__":
    main()
