# PyPI Toolkit

`pypi-toolkit` is a small command-line toolkit for the routine mechanics around publishing Python packages: run tests, build distributions, upload them with Twine, scaffold a package, or initialise Git.

## Install

```bash
pip install pypi-toolkit
```

For development:

```bash
python -m pip install -e '.[dev]'
```

## Commands

```bash
pypi-toolkit test
pypi-toolkit build
pypi-toolkit upload
pypi-toolkit all
pypi-toolkit create_package
pypi-toolkit init_git
```

`all` deliberately runs tests before building and uploading. Uploads read standard Twine credentials from `TWINE_USERNAME` and `TWINE_PASSWORD`; the legacy `PYPI_USERNAME` and `PYPI_PASSWORD` names are also accepted.

A token-based setup looks like this:

```bash
export TWINE_USERNAME=__token__
export TWINE_PASSWORD='pypi-...'
pypi-toolkit all
```

Credentials are passed to Twine through the environment rather than command-line arguments.

## Development

Run the same checks used by GitHub Actions:

```bash
python -m pytest
ruff check .
python -m build
python -m twine check dist/*
```

CI runs on pull requests and pushes to `main`. Publishing is intentionally separate from CI and only runs for GitHub releases, preventing ordinary documentation or code commits from attempting to republish the same package version.

## License

MIT
