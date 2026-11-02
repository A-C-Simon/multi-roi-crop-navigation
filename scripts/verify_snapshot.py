"""Verify preserved source and asset files against their import checksums."""
from pathlib import Path
import hashlib
import json
import sys


def main():
    root = Path(__file__).resolve().parents[1]
    record = json.loads((root / 'docs/source-snapshot.json').read_text())
    mismatches = []
    for name, expected in record['sha256'].items():
        path = root / name
        if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != expected:
            mismatches.append(name)
    if mismatches:
        print('Snapshot differences:', *mismatches, sep='\n  ')
        return 1
    print(f"Verified {len(record['sha256'])} unchanged source and asset files")
    return 0


if __name__ == '__main__':
    sys.exit(main())
