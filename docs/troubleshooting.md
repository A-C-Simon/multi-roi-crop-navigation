# Troubleshooting

## Command not found

Activate the environment where the project was installed:

```bash
source .venv/bin/activate
python -m pip show multi-roi-crop-navigation
```

From a checkout, `python test_multi_roi.py --help` also runs the detector.

## No images are processed

Supply `--input` explicitly. The historical default refers to a photo directory
outside this repository. Confirm that your folder contains readable image
files, or quote a supported glob. The sample generator provides a quick check:

```bash
python examples/generate_sample.py
multiroi-detect --input examples/data --results_dir outputs/check
```

The existing scripts can print an input error without returning a failing
process exit status. Check their log, the output count, and the CSV contents.

## OpenCV import fails with a missing library

On Ubuntu, install `libgl1` and `libglib2.0-0`. Use a clean virtual environment
if several OpenCV distributions are installed. The standard and headless
packages both expose `cv2` and should not be mixed.

## Preview fails on a server

Omit `--show`. File processing does not need a display. A GUI preview requires
a valid display session and the corresponding OpenCV GUI libraries.

## MP4 is missing or empty

Video codec availability depends on the OpenCV build. Check that the input
opens and contains frames. Keep the console log and verify the output with a
video player or by reopening it with OpenCV. A CSV alone does not prove that
a video was encoded successfully.

## The overlay is plausible but the path is wrong

Inspect the binary mask, two-sided evidence, and accepted points together.
Sparse crops, merged weeds, and competing furrows can produce incorrect
geometry. A fitted line is not proof of a detected corridor. Save the composite
and CSV for the same frame when reporting the issue.

## Simulation cannot find Python modules

Follow the separate environment instructions in [simulation](simulation.md).
The launch scripts use system Python, which cannot automatically see packages
installed only into the offline virtual environment. Check imports with system
`python3` in the same shell used to launch ROS.

## Simulation cannot find models or source files

Set `MULTIROI_DIR` to the root of this checkout before building or launching.
The repository must include `run_mr_navigation.py` at that root and the plant
models under `tests/agribot/agribot_gazebo/models`.

## Another Gazebo server is running

The wrapper refuses to start when `gzserver` is already active. Stop the
previous simulation through its launch terminal, then retry. Avoid starting
multiple rigs that publish on the same ROS topics.

## Reproducing an installation problem

Record `python --version`, `python -m pip freeze`, the exact command, and the
complete error text. Avoid sharing credentials or unrelated environment files.

## Pytest imports ROS packages in the offline environment

A sourced ROS shell can add packages through `PYTHONPATH`, even when a virtual
environment is active. Use a fresh terminal for offline work. To run the check
without the inherited path on Linux:

```bash
env -u PYTHONPATH python -m pytest
```
