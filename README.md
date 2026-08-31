[![OpenSD2026 - Belgium](assets/OpenSD_bannerlogo.jpg)](https://www.vub.be/en/event/opensd-summer-school-belgium)

# Workshop_OpenSD2026

Repository containing the materials for the OpenSD2026 Workshop in Belgium, providing a hands-on introduction to Python programming for structural dynamics.

Workshop page: https://www.vub.be/en/event/opensd-summer-school-belgium

## Repository layout

- `notebooks/` workshop notebooks and exercises:
  - `WS0_Introduction/`
  - `WS1_An_intro_to_python/`
  - `WS2_Signal_processing_for_SHM/`
  - `WS3_Intro_to_pyFatigue/`
  - `WS4_AI_for_SHM/`
- `assets/` images and workshop assets

## Working on the workshop

There are two main ways to use the workshop materials:

- **GitHub Codespaces** (recommended during the workshop): ready-to-use development environment in the browser.
- **Local installation**: clone the repository and run everything on your own machine.

## Dependency management with uv

This repository uses [uv](https://docs.astral.sh/uv/) to manage Python dependencies:

```bash
uv sync
uv run jupyter lab
```

## Testing with pytest

Tests are located in `notebooks/WS1_An_intro_to_python/012_test_driven_dev/tests`. Run them with:

```bash
uv run pytest
```

## License

Copyright © 2026 OpenSD2026 contributors. All rights reserved. The materials in this repository are provided for educational use only and may not be copied, redistributed, or modified without prior permission. See [LICENSE](LICENSE).
