import argparse
import glob
import logging
import os
import subprocess
import sys
from collections.abc import Mapping, Sequence
from typing import Optional

from pypi_toolkit.git_manager import GitManager

if os.path.isfile(".env"):
    from dotenv import load_dotenv

    load_dotenv()


def run_command(
    command: Sequence[str],
    *,
    env: Optional[Mapping[str, str]] = None,
) -> None:
    """Run a command and raise on failure."""
    logging.info("Running command: %s", " ".join(command))
    subprocess.run(command, check=True, text=True, env=env)


def build_package() -> None:
    """Build source and wheel distributions."""
    run_command([sys.executable, "-m", "build"])


def run_tests() -> None:
    """Run the project's pytest suite."""
    run_command([sys.executable, "-m", "pytest"])


def upload_to_pypi() -> None:
    """Upload built distributions to PyPI with Twine."""
    username = os.getenv("TWINE_USERNAME") or os.getenv("PYPI_USERNAME")
    password = os.getenv("TWINE_PASSWORD") or os.getenv("PYPI_PASSWORD")

    if not username or not password:
        raise RuntimeError(
            "PyPI credentials are missing. Set TWINE_USERNAME/TWINE_PASSWORD "
            "or PYPI_USERNAME/PYPI_PASSWORD."
        )

    artifacts = sorted(glob.glob("dist/*"))
    if not artifacts:
        raise FileNotFoundError("No distributions found in dist/. Run 'pypi-toolkit build' first.")

    env = os.environ.copy()
    env["TWINE_USERNAME"] = username
    env["TWINE_PASSWORD"] = password
    run_command([sys.executable, "-m", "twine", "upload", *artifacts], env=env)


def create_package_with_cookiecutter() -> None:
    """Create a package from the standard Cookiecutter PyPackage template."""
    template_url = "https://github.com/audreyfeldroy/cookiecutter-pypackage.git"
    logging.info("Creating a package from %s", template_url)
    from cookiecutter.main import cookiecutter

    cookiecutter(template_url)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="pypi-toolkit",
        description="Build, test, publish, scaffold, and initialize Python packages.",
    )
    parser.add_argument(
        "action",
        choices=["build", "test", "upload", "all", "init_git", "create_package"],
    )
    return parser


def main(argv: Optional[Sequence[str]] = None) -> None:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    args = build_parser().parse_args(argv)

    if args.action == "init_git":
        GitManager().init_repository()
        return

    if args.action == "create_package":
        create_package_with_cookiecutter()
        return

    if args.action == "build":
        build_package()
        return

    if args.action == "test":
        run_tests()
        return

    if args.action == "upload":
        upload_to_pypi()
        return

    run_tests()
    build_package()
    upload_to_pypi()
