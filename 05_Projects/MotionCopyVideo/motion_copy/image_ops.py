"""Image helpers: reference boards, contact sheets and consistency metrics.

Images are read/written through numpy buffers (imdecode/imencode) because
cv2.imread/imwrite cannot open non-ASCII Windows paths.
"""

from __future__ import annotations

import math
from pathlib import Path

import cv2
import numpy as np

IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp", ".bmp"}


def list_images(folder: Path) -> list[Path]:
    if not folder.is_dir():
        return []
    return sorted(p for p in folder.iterdir() if p.suffix.lower() in IMAGE_EXTENSIONS)


def read_image(path: Path) -> np.ndarray:
    image = cv2.imdecode(np.fromfile(str(path), dtype=np.uint8), cv2.IMREAD_COLOR)
    if image is None:
        raise ValueError(f"Cannot read image: {path}")
    return image


def write_image(path: Path, image: np.ndarray) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    ok, buffer = cv2.imencode(path.suffix or ".png", image)
    if not ok:
        raise ValueError(f"Cannot encode image: {path}")
    buffer.tofile(str(path))


def fit_tile(image: np.ndarray, width: int, height: int, background: int = 255) -> np.ndarray:
    """Letterbox an image into a width x height tile without distorting it."""
    scale = min(width / image.shape[1], height / image.shape[0])
    resized = cv2.resize(
        image,
        (max(1, int(image.shape[1] * scale)), max(1, int(image.shape[0] * scale))),
        interpolation=cv2.INTER_AREA,
    )
    tile = np.full((height, width, 3), background, np.uint8)
    y = (height - resized.shape[0]) // 2
    x = (width - resized.shape[1]) // 2
    tile[y:y + resized.shape[0], x:x + resized.shape[1]] = resized
    return tile


def _label(tile: np.ndarray, text: str) -> None:
    cv2.rectangle(tile, (0, 0), (min(tile.shape[1], 22 + 13 * len(text)), 30), (0, 0, 0), -1)
    cv2.putText(tile, text, (6, 22), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1, cv2.LINE_AA)


def build_board(images: list[Path], tile: int = 640) -> np.ndarray:
    """Pack several reference photos into one numbered grid image.

    Flow accepts only a few ingredient images, so every category (outfit,
    accessories, bike...) becomes exactly one board image.
    """
    cols = math.ceil(math.sqrt(len(images)))
    rows = math.ceil(len(images) / cols)
    board = np.full((rows * tile, cols * tile, 3), 255, np.uint8)
    for index, path in enumerate(images):
        cell = fit_tile(read_image(path), tile, tile)
        if len(images) > 1:
            _label(cell, str(index + 1))
        r, c = divmod(index, cols)
        board[r * tile:(r + 1) * tile, c * tile:(c + 1) * tile] = cell
    return board


def contact_sheet(rows: list[tuple[str, list[np.ndarray]]], tile_w: int = 270, tile_h: int = 480) -> np.ndarray:
    """One image with a labelled row per entry; used for the human visual check."""
    cols = max(len(frames) for _, frames in rows)
    sheet = np.full((len(rows) * tile_h, cols * tile_w, 3), 40, np.uint8)
    for r, (label, frames) in enumerate(rows):
        for c, frame in enumerate(frames):
            cell = fit_tile(frame, tile_w, tile_h, background=40)
            if c == 0:
                _label(cell, label)
            sheet[r * tile_h:(r + 1) * tile_h, c * tile_w:(c + 1) * tile_w] = cell
    return sheet


def _center(image: np.ndarray, keep: float = 0.6) -> np.ndarray:
    h, w = image.shape[:2]
    dh, dw = int(h * (1 - keep) / 2), int(w * (1 - keep) / 2)
    return image[dh:h - dh, dw:w - dw]


def colour_signature(frames: list[np.ndarray]) -> np.ndarray:
    """Mean hue/saturation histogram of the frame centre, where the subject usually is."""
    hists = []
    for frame in frames:
        hsv = cv2.cvtColor(_center(frame), cv2.COLOR_BGR2HSV)
        hist = cv2.calcHist([hsv], [0, 1], None, [30, 32], [0, 180, 0, 256])
        hists.append(cv2.normalize(hist, None).flatten())
    return np.mean(hists, axis=0).astype(np.float32)


def signature_similarity(a: np.ndarray, b: np.ndarray) -> float:
    """Histogram correlation in [-1, 1]; 1 means identical colour distribution."""
    return float(cv2.compareHist(a, b, cv2.HISTCMP_CORREL))


def frame_difference(a: np.ndarray, b: np.ndarray) -> float:
    """Mean absolute grey-level difference in [0, 1] at a common small size."""
    size = (160, 284)
    ga = cv2.cvtColor(cv2.resize(a, size, interpolation=cv2.INTER_AREA), cv2.COLOR_BGR2GRAY)
    gb = cv2.cvtColor(cv2.resize(b, size, interpolation=cv2.INTER_AREA), cv2.COLOR_BGR2GRAY)
    return float(np.mean(cv2.absdiff(ga, gb))) / 255.0


def colour_stats(frames: list[np.ndarray]) -> tuple[np.ndarray, np.ndarray]:
    """Per-channel (B, G, R) mean and std over sampled frames."""
    pixels = np.concatenate([f.reshape(-1, 3).astype(np.float64) for f in frames])
    return pixels.mean(axis=0), pixels.std(axis=0) + 1e-6


def colour_match_lut(
    clip_stats: tuple[np.ndarray, np.ndarray],
    anchor_stats: tuple[np.ndarray, np.ndarray],
    max_gain: float = 1.25,
) -> str:
    """ffmpeg lutrgb filter mapping a clip's colour statistics onto the anchor clip.

    One fixed transform per clip (not per frame), so it cannot introduce flicker.
    """
    (c_mean, c_std), (a_mean, a_std) = clip_stats, anchor_stats
    parts = []
    for name, index in (("r", 2), ("g", 1), ("b", 0)):
        gain = float(np.clip(a_std[index] / c_std[index], 1 / max_gain, max_gain))
        offset = float(a_mean[index] - c_mean[index] * gain)
        parts.append(f"{name}='clip(val*{gain:.4f}+({offset:.2f}),0,255)'")
    return "lutrgb=" + ":".join(parts)
