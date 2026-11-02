# Installation

## Requirements

The offline tools need Python 3.10 to 3.12, pip, and a virtual environment.
Linux with Python 3.10 is the reference platform. Python 3.11 and 3.12 are
included in the CI configuration; other operating systems have not been
validated here. No GPU, model weights, ROS installation, or field dataset is
required for the offline examples.

On Ubuntu, install the Python environment tools and OpenCV runtime libraries:

```bash
sudo apt update
sudo apt install python3-venv python3-pip libgl1 libglib2.0-0
```

## Install from a checkout

Start in a fresh terminal without ROS sourced. An inherited ROS `PYTHONPATH`
can expose unrelated packages and pytest plugins inside a virtual environment.

```bash
git clone https://github.com/A-C-Simon/multi-roi-crop-navigation.git
cd multi-roi-crop-navigation
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install .
```

For a source checkout you plan to edit, use this instead of the last command:

```bash
python -m pip install -e '.[dev]'
```

The package installs three commands:

| Command | Purpose |
| --- | --- |
| `multiroi-detect` | Extended detector for image folders or globs |
| `multiroi-nav` | Navigation analysis for images, video, or a camera |
| `multiroi-reference` | Preserved reference detector |

The commands work outside the repository. Examples, historical CSV files, and
the simulator workspace are accessed from a checkout or source archive.

## Reference dependency versions

The core runtime used for the snapshot checks is recorded in
[`constraints-tested.txt`](../constraints-tested.txt). To select those versions:

```bash
python -m pip install -c constraints-tested.txt '.[dev]'
```

The constraints cover the four direct runtime dependencies. They are not a full
lock of every transitive package. The declared dependency ranges retain NumPy
1.x compatibility for the preserved implementation.

## Verify the installation

```bash
multiroi-detect --help
multiroi-nav --help
python examples/generate_sample.py
multiroi-detect --input examples/data --results_dir outputs/install-check
```

Expect two processed images and `detection_data.csv` in
`outputs/install-check`. For the automated checks, install the `dev` extra and
run `python -m pytest` from the repository root.

## Display and video support

The default package is `opencv-python`, which supports `--show` on a machine
with a working display. Omit `--show` for file processing on a server. Avoid
installing both the standard and headless OpenCV distributions into the same
environment, since they provide the same `cv2` module.

For the separate ROS environment, follow [simulation](simulation.md). Do not
reuse the offline virtual environment for ROS launch commands.
