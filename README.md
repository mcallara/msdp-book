# Modern Software Development Practices

A Jupyter Book containing comprehensive material on modern software development practices.

## Project Structure

- `ch1/` - Chapter 1 content
- `ch2/` - Chapter 2 content
- `ch3/` - Chapter 3 content (includes `portfolio.ipynb`)
- `ch4/` - Chapter 4 content
- `ch5/` - Chapter 5 content
- `test_money/` - Test files for the Money class implementation
- `images/` - Image assets
- `_config.yml` - Jupyter Book configuration
- `_toc.yml` - Jupyter Book table of contents
- `intro.md` - Introduction page
- `references.bib` - Bibliography

## Prerequisites

- Python 3.9 or higher
- [uv](https://github.com/astral-sh/uv) package manager

## Getting Started

### 1. Install uv (if not already installed)

```bash
# On macOS with Homebrew
brew install uv

# Or download from https://github.com/astral-sh/uv
```

### 2. Sync Dependencies

```bash
uv sync
```

This will:
- Create a virtual environment in `.venv/`
- Install all project dependencies listed in `pyproject.toml`
- Lock dependency versions in `uv.lock`

### 3. Build the Book

```bash
uv run jupyter-book build .
```

The built book will be available at `_build/html/index.html`

### 4. View the Book

Open the generated HTML in your browser:

```bash
open _build/html/index.html
```

## Development

### Running Python Scripts

```bash
uv run python <script.py>
```

### Running Tests

```bash
uv run pytest
```

### Using Jupyter Notebooks

```bash
uv run jupyter notebook
```

## Dependencies

Key dependencies managed by uv:

- `jupyter-book` - Build system for the book
- `matplotlib` - Data visualization
- `numpy` - Numerical computing
- `pytest` - Testing framework
- `ipytest` - Testing in notebooks
- `sphinxcontrib-mermaid` - Mermaid diagram support
- `bash-kernel` - Bash kernel for Jupyter
- `ghp-import` - GitHub Pages deployment

See `pyproject.toml` for the complete list of dependencies.

## License

Copyright © 2025 Matias Callara
