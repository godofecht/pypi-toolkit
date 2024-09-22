# PyPI Toolkit

```markdown
`pypi-toolkit` is a command-line tool designed to simplify the process of building, testing, and uploading Python packages to PyPI.

## Table of Contents

- [Motivation](#motivation)
- [Features](#features)
- [Checklist](#checklist)
    - [Current Features](#current-features)
    - [Upcoming Features](#upcoming-features)
- [Installation](#installation)
- [Usage](#usage)

## Motivation

Publishing Python packages to PyPI can be a repetitive and error-prone process. `pypi-toolkit` aims to streamline this workflow by providing a single tool that handles building, testing, and uploading your packages, ensuring consistency and reducing the likelihood of mistakes. With `pypi-toolkit`, it becomes much easier to quickly build, test, and upload your PyPI package.

## Features

- **Build**: Creates source and wheel distributions.
- **Test**: Runs your test suite using `pytest`.
- **Upload**: Uploads your package to PyPI using `twine`.
- **All**: Performs build, test, and upload in sequence.

## Checklist

### Current Features

- [x] Build source and wheel distributions
- [x] Run tests using `pytest`
- [x] Upload packages to PyPI using `twine`
- [x] Perform build, test, and upload in sequence

### Upcoming Features

- [ ] Automated version bumping
- [ ] Integration with CI/CD pipelines
- [ ] Enhanced logging and error reporting
- [ ] Support for additional testing frameworks

## Installation

You can install `pypi-toolkit` using `pip`:

```bash
pip install pypi-toolkit
```

## Usage

After installing `pypi-toolkit`, you can use the following commands:

- To build your package:
  ```bash
  pypi-toolkit build
  ```

- To test your package:
  ```bash
  pypi-toolkit test
  ```

- To upload your package to PyPI:
  ```bash
  pypi-toolkit upload
  ```

- To perform build, test, and upload in sequence:
  ```bash
  pypi-toolkit all
  ```
```
