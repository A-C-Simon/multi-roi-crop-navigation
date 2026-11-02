# Outputs

## Detection command

`multiroi-detect` writes one composite PNG per readable image and
`detection_data.csv` in the selected results directory. The composite contains
four panels:

| Position | Contents |
| --- | --- |
| Top left | Excess green and Otsu binary segmentation |
| Top right | Kept and removed vegetation pixels |
| Bottom left | Mask, strip regions, selected points, and fitted geometry |
| Bottom right | Geometry over the original image |

Green points are assigned to the navigation fit. Red points are rejected or
suppressed. White regions show the strip corridor. The light blue path is the
navigation fit; darker blue lines describe the flanking rows. Fallback points
can also enter the fit, so color alone does not establish measured evidence.

The detector CSV includes filename, pass-one and final navigation angles,
point count, detection-line count, weed pressure, post-scrub removal statistics,
and processing time. With post-scrubbing disabled, the two angle fields match.
The angle is measured in degrees from vertical; it is not a ground-truth error.

## Navigation command

Folder mode writes `*_nav.png`, `*_composite.png`, `*_combined.png`, and
`nav_commands.csv`.
Video mode writes `<input-name>_nav.mp4` and `<input-name>_nav.csv`.
`--composite-only` changes the video output to `<input-name>_composite.mp4`
and suppresses the separate folder navigation image.

CSV schemas differ between folder, video, and simulator modes. Read the
header before combining files. Common quantities are:

| Quantity | Unit or interpretation |
| --- | --- |
| Linear command, `v` | metres per second |
| Angular command, `w` | radians per second |
| Lateral image error | pixels relative to image centre |
| Heading | degrees in CSV diagnostics; radians in controller features |
| Corridor width | pixels, not physical row spacing |
| Confidence | implementation score in `[0, 1]`, not a calibrated probability |
| Two-sided strips | detector evidence count |
| Status | filter or map decision label |

Navigation overlays show the filtered red path, raw geometry, and optional
lookahead regions. These are diagnostic drawings. They do not establish
clearance from crops or obstacles.

## Simulator

The simulator writes `nav_run.csv` and periodic overlay frames in its log
directory. With the ToF guard enabled, it also writes `tof_guard.csv`.
Cross-track measurements are in metres and use the simulated lane geometry.
They are distinct from the image-space lateral error.

## Keeping runs separate

Use a new output directory per experiment. Reusing a directory can overwrite
files with the same names and leave older files from a different input set.
Generated outputs are ignored by Git under `outputs/`.
