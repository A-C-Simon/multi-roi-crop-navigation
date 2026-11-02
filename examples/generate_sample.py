"""Generate small geometric crop scenes for trying the command-line tools."""
from pathlib import Path
import argparse
import math
import cv2
import numpy as np


def scene(phase=0.0):
    h, w = 480, 640
    rng = np.random.default_rng(42)
    image = np.full((h, w, 3), (62, 81, 112), dtype=np.uint8)
    noise = rng.integers(-8, 9, (h, w, 1), dtype=np.int16)
    image = np.clip(image.astype(np.int16) + noise, 0, 255).astype(np.uint8)
    shift = 6.0 * math.sin(phase)
    for base in (40, 225, 415, 600):
        for y in range(0, h, 20):
            def center(yy):
                t = yy / (h - 1)
                return 320 + (base - 320) * (0.35 + 0.65 * t) + shift
            half = 3 + 8 * y / h
            y2 = min(h - 1, y + 18)
            pts = np.array([[center(y)-half,y], [center(y)+half,y],
                            [center(y2)+half,y2], [center(y2)-half,y2]], np.int32)
            cv2.fillPoly(image, [pts], (35, 156 + (y // 20 % 3) * 14, 42))
    for x, y in ((70, 280), (530, 370), (85, 410)):
        cv2.circle(image, (x, y), 5, (30, 135, 42), -1)
    return image


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=Path('examples/data'))
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    for name, phase in [('straight', 0.0), ('offset', math.pi / 2)]:
        path = args.output / f'{name}.png'
        if not cv2.imwrite(str(path), scene(phase)):
            raise RuntimeError(f'Could not write {path}')
    path = args.output / 'corridor.mp4'
    writer = cv2.VideoWriter(str(path), cv2.VideoWriter_fourcc(*'mp4v'), 20, (640,480))
    if not writer.isOpened():
        raise RuntimeError('MP4 writer unavailable; the PNG examples were still generated')
    try:
        for i in range(40):
            writer.write(scene(i / 39 * 2 * math.pi))
    finally:
        writer.release()
    print(f'Wrote two PNG images and a 40-frame MP4 to {args.output.resolve()}')


if __name__ == '__main__':
    main()
