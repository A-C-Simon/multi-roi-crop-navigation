# Project origin

## Source

This is a standalone distribution of the MultiROI directory from
[A-C-Simon/Crop_row_detection](https://github.com/A-C-Simon/Crop_row_detection).
It starts a new Git history rather than importing the full research repository.
The original project remains the reference for earlier development history and
large result collections.

The import uses commit `e0d5b105826a63875bc0a51c95e61ab818480b8d`, subdirectory
`LinReg/MultiROI`, as available on 2026-11-02. The runtime source and selected
simulation assets are copied without algorithm changes. Exact checksums are
recorded in [source-snapshot.json](source-snapshot.json).

This distribution adds Python packaging, command entry points, installation
instructions, generated examples, a documentation set, and CI configuration.
Historical result CSV files and experiment notes are retained separately.
The paper PDF, original photo collection, full agribot checkout, local caches,
colcon build output, and generated navigation runs are excluded.

## Research reference

Zhou Y, Yang Y, Zhang B L, Wen X, Yue X, Chen L Q. Autonomous detection of crop
rows based on adaptive multi-ROI in maize fields. *International Journal of
Agricultural and Biological Engineering*, 2021; 14(4): 217-225.
[10.25165/j.ijabe.20211404.6315](https://doi.org/10.25165/j.ijabe.20211404.6315).

`multi_roi.py` is the preserved reference reimplementation. The extended
detector and navigation stack add component filtering, evidence selection,
TLS fitting, spline geometry, temporal filtering, and control. They should not
be described as an exact reproduction of the paper.

## Licensing

The source repository has no root license. This distribution does not supply a
new permission grant for that code. Separate terms apply to the simulation
package and bundled plant models. See [third-party notices](../THIRD_PARTY_NOTICES.md).
