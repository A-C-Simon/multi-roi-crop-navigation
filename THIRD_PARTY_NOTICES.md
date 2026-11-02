# Third-party notices

## Original project

The detector and navigation source were copied from
[A-C-Simon/Crop_row_detection](https://github.com/A-C-Simon/Crop_row_detection),
under `LinReg/MultiROI`. The exact source revision and file checksums are in
[docs/source-snapshot.json](docs/source-snapshot.json). No root license was
specified there. This repository does not assign a new open-source license to
that code.

## Simulation package

The existing `mrsim` package declares MIT in its package metadata. That applies
to the package in `tests/sim_ros2/src/mrsim`, subject to the separate plant-model
license below. Its license text is included beside `package.xml`.

## Plant models

The `big_plant` and `small_plant` models under
`tests/agribot/agribot_gazebo/models` come from
[PRBonn/agribot](https://github.com/PRBonn/agribot), revision
`3e477363b3427c7928f43efc97224f23c5b3e4ea`.
They are distributed under the BSD 2-Clause license. The original copyright
notice and license are retained in [tests/agribot/LICENSE.md](tests/agribot/LICENSE.md).
Only those models are included, rather than the full reference repository.

## Research reference

Zhou Y, Yang Y, Zhang B L, Wen X, Yue X, Chen L Q. Autonomous detection of crop
rows based on adaptive multi-ROI in maize fields. *International Journal of
Agricultural and Biological Engineering*, 2021, 14(4), 217-225.
[DOI: 10.25165/j.ijabe.20211404.6315](https://doi.org/10.25165/j.ijabe.20211404.6315).

The article PDF and the original photograph collection are not bundled. The
example images in this repository are generated geometric scenes.

## Python dependencies

NumPy, OpenCV, SciPy, and scikit-learn are installed separately. Their respective
licenses apply to those packages. They are not vendored in this repository.
