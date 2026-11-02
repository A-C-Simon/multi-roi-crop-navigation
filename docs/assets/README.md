# Field example

The README preview uses `photo_7_2026-08-18_17-17-57.png` from the original
project's `Photos` directory. The input is included at
[`examples/field/photo_7_2026-08-18_17-17-57.png`](../../examples/field/photo_7_2026-08-18_17-17-57.png),
without resizing, retouching, or changes to the detector.

[Original repository image](https://github.com/A-C-Simon/Crop_row_detection/blob/e0d5b105826a63875bc0a51c95e61ab818480b8d/Photos/photo_7_2026-08-18_17-17-57.png).

Run this from the repository root after installation:

```bash
multiroi-detect --input examples/field --results_dir outputs/field-example
```

The resulting `photo_7_2026-08-18_17-17-57.png` is the four-panel composite
shown in the README. `detector-preview.png` is a copy of that output.
It is a single demonstration result, not an accuracy benchmark.

Input SHA-256: `fed0df94b402cebc388a303602a7c3840fcd6d5b4eabbb4c8e9af43613ca990f`.

## Navigation recording

`navigation-demo.mp4` is the supplied screencast, copied without re-encoding.
It shows the simulated rover alongside the live MultiROI overlay. The file is
H.264 video at 964 by 340 pixels, with a duration of 62.52 seconds.

`navigation-demo.gif` is an eight-second extract beginning at four seconds,
rendered at 10 frames per second for the README. The complete recording is
available through the linked MP4.
