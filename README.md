# Workshop_OpenSD2026
Repository containing the materials for the OpenSD2026 Workshop in Belgium, providing a hands-on introduction to Python programming for structural dynamics.  Workshop page: https://www.vub.be/en/event/opensd-summer-school-belgium

## Repository layout
- `src/` Python source package for workshop
- `notebooks/` folder that contains the workshops 
- `notebooks/01_introduction/01_introduction.ipynb`
- `notebooks/02_python_fundamentals/02_python_fundamentals.ipynb`
- `notebooks/02_python_fundamentals/02_python_fundamentals.ipynb`
- `notebooks/03_structural_dynamics/03_structural_dynamics.ipynb`
- `notebooks/04_project_work/04_project_work.ipynb`

## Working on the workshop 
There are two main ways to work with the workshop materials:

GitHub Codespaces
Recommended during the workshop. It provides a ready-to-use development environment directly in the browser.
Local installation
Clone the repository and run the workshop on your own computer.

## Dependency management with uv

This repository uses [uv](https://docs.astral.sh/uv/) to manage Python dependencies.

```bash
uv sync
uv run jupyter lab
```
