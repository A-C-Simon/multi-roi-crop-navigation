# Validation and limits

## Distribution scope

Version 0.1.0 packages the existing detector and navigation implementation for
inspection and reproducible setup. The runtime algorithms, simulator nodes,
worlds, and launch behavior are preserved from the source snapshot. This is
not an audit-fix release.

## Automated checks

The existing suite has eight synthetic checks covering missing plants,
persistent shifts, width changes, straight and slanted corridors, drawing
coverage, and short heading excursions. Run it with:

```bash
python -m pip install -e '.[dev]'
python -m pytest
```

The CI configuration runs the tests and command help on Python 3.10, 3.11,
and 3.12. It also generates example inputs, runs the image and video commands,
and builds a wheel and source archive. CI does not launch Gazebo or assess
field accuracy.

Use `python scripts/verify_snapshot.py` to compare preserved source and asset
files with the recorded SHA-256 checksums. New packaging and documentation
files are outside that source snapshot.

## Evidence limits

Historical image results used visual inspection without labeled ground truth.
Their angles describe estimated geometry; they are not accuracy scores. Their
runtimes came from the original local setup and are not portable benchmarks.
The generated examples only verify that the tools can be installed and run.

Known limits include sparse or missing rows, vegetation bridges, strongly
curved corridors, competing neighboring furrows, stale geometry, and differences
between command-line and library configurations. Detection and navigation have
unresolved correctness issues. A valid-looking overlay does not establish a
safe path, and loss of evidence does not guarantee a stop command.

## Simulation scope

The simulator uses a different configuration from the default video CLI.
Historical lane-following results are described in the original project; they
have not been re-established by packaging this repository. Gazebo is not run
in CI. Neither synthetic tests nor simulation validate a physical rover.

## Reporting a problem

Include the command, Python version, dependency versions, image dimensions,
and a small input you are allowed to share. Attach the CSV header and relevant
rows, plus a composite image if it helps explain the failure. Use the
[issue tracker](https://github.com/A-C-Simon/multi-roi-crop-navigation/issues).
