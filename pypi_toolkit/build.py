import os
import subprocess
import sys
import argparse
import logging
from dataclasses import dataclass
from dotenv import load_dotenv
from pypi_toolkit.git_manager import GitManager

# Load environment variables from .env file if available
if os.path.exists('.env'):
    load_dotenv()

def run_command(command: str) -> None:
    """Run shell commands and exit if they fail."""
    logging.info(f"Running command: {command}")
    result = subprocess.run(command, shell=True, text=True)
    if result.returncode != 0:
        logging.error(f"Command failed: {command}")
        sys.exit(result.returncode)

def install_twine() -> None:
    """Ensure that Twine is installed."""
    try:
        import twine
    except ImportError:
        logging.info("Twine not found. Installing twine...")
        run_command("pip install twine")

def build_package() -> None:
    """Build the Python package."""
    logging.info("Building the package...")
    run_command("python -m build")

def run_tests() -> None:
    """Run the test suite."""
    logging.info("Running tests...")
    run_command("pytest")

def upload_to_pypi() -> None:
    """Upload the built package to PyPI."""
    pypi_username = os.getenv('PYPI_USERNAME', '')
    pypi_password = os.getenv('PYPI_PASSWORD', '')

    if not pypi_username or not pypi_password:
        logging.error("PyPI credentials are missing. Please set PYPI_USERNAME and PYPI_PASSWORD as environment variables or in the .env file.")
        sys.exit(1)

    logging.info(f"Uploading the package to PyPI as {pypi_username}...")
    run_command(f"twine upload dist/* -u {pypi_username} -p {pypi_password}")

def install_cookiecutter() -> None:
    """Ensure that Cookiecutter is installed."""
    try:
        import cookiecutter
    except ImportError:
        logging.info("Cookiecutter not found. Installing cookiecutter...")
        run_command("pip install cookiecutter")

def create_package_with_cookiecutter() -> None:
    """Create a new Python package using cookiecutter."""
    install_cookiecutter()
    template_url = "https://github.com/audreyr/cookiecutter-pypackage.git"
    logging.info(f"Creating a new Python package with cookiecutter from template: {template_url}")
    run_command(f"cookiecutter {template_url}")

def main() -> None:
    """Main entry point for argument parsing and command execution."""
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

    parser = argparse.ArgumentParser(
        description="A toolkit for building, testing, uploading Python packages to PyPI, and initializing a Git repository."
    )
    
    parser.add_argument(
        "action",
        choices=["build", "test", "upload", "all", "init_git", "create_package"],
        help=(
            "Choose the action to perform:\n"
            "  build          Build the Python package.\n"
            "  test           Run the test suite.\n"
            "  upload         Upload the built package to PyPI.\n"
            "  all            Build, test, and upload the package to PyPI.\n"
            "  init_git       Initialize a Git repository.\n"
            "  create_package Create a new Python package using cookiecutter."
        )
    )
    
    args = parser.parse_args()

    git_manager = GitManager()

    # Execute the action based on the argument passed
    if args.action == "init_git":
        git_manager.init_repository()

    if args.action == "create_package":
        create_package_with_cookiecutter()

    if args.action in ["build", "all"]:
        build_package()

    if args.action in ["test", "all"]:
        run_tests()

    if args.action in ["upload", "all"]:
        # Run tests before upload in the 'all' case to ensure upload happens only after successful tests
        if args.action == "all":
            logging.info("All tests passed. Proceeding with upload...")
        install_twine()
        upload_to_pypi()

    logging.info("Process completed successfully.")

if __name__ == "__main__":
    main()
