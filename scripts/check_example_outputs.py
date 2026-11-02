"""Check that the documented example commands produced readable artifacts."""
from pathlib import Path
import csv
import cv2


def main():
    images = sorted(Path('outputs/detection').glob('*.png'))
    if len(images) != 2 or any(cv2.imread(str(p)) is None for p in images):
        raise RuntimeError('Expected two readable detection composites')
    for name, expected in [('outputs/detection/detection_data.csv',2),
                           ('outputs/video/corridor_nav.csv',40)]:
        with open(name, newline='') as stream:
            rows = list(csv.DictReader(stream))
        if len(rows) != expected:
            raise RuntimeError(f'{name}: expected {expected} records, got {len(rows)}')
    cap = cv2.VideoCapture('outputs/video/corridor_nav.mp4')
    count = 0
    try:
        while True:
            ok, _ = cap.read()
            if not ok:
                break
            count += 1
    finally:
        cap.release()
    if count != 40:
        raise RuntimeError(f'Expected 40 readable video frames, got {count}')
    print('Verified two image composites, both CSV files, and a 40-frame video')


if __name__ == '__main__':
    main()
