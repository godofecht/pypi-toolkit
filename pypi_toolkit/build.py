import os
import subprocess
import sys
import argparse
import logging
from dataclasses import dataclass
from dotenv import load_dotenv

# Load environment variables from .env file if available
if os.path.exists('.env'):
    load_dotenv()

@dataclass
class GitManager:
    git_user: str = os.getenv('GIT_USER', '')
    git_email: str = os.getenv('GIT_EMAIL', '')

    def run_command(self, command: str) -> None:
        """Run shell commands and exit if they fail."""
        logging.info(f"Running command: {command}")
        result = subprocess.run(command, shell=True, text=True)
        if result.returncode != 0:
            logging.error(f"Command failed: {command}")
            sys.exit(result.returncode)

    def check_env_variables(self) -> None:
        """Check for required environment variables and log if not found."""
        if not self.git_user:
            logging.warning("Environment variable GIT_USER not found.")
        if not self.git_email:
            logging.warning("Environment variable GIT_EMAIL not found.")

    def prompt_for_missing_details(self) -> None:
        """Prompt user interactively for Git details if environment variables are missing."""
        if not self.git_user:
            self.git_user = input("Enter your Git username: ")
        if not self.git_email:
            self.git_email = input("Enter your Git email: ")

    def configure_git(self) -> None:
        """Configure git with user details."""
        self.run_command(f"git config user.name '{self.git_user}'")
        self.run_command(f"git config user.email '{self.git_email}'")

    def init_repository(self) -> None:
        """Initialize a git repository and commit initial files."""
        if not os.path.exists('.git'):
            logging.info("Initializing a new Git repository...")

            self.check_env_variables()
            self.prompt_for_missing_details()
            self.configure_git()

            # Initialize git, add files, and make the first commit
            self.run_command("git init")
            self.run_command("git add .")
            self.run_command("git commit -m 'Initial commit'")
        else:
            logging.info("Git repository already exists.")


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

def main() -> None:
    """Main entry point for argument parsing and command execution."""
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

    parser = argparse.ArgumentParser(
        description="A toolkit for building, testing, uploading Python packages to PyPI, and initializing a Git repository."
    )
    
    parser.add_argument(
        "action",
        choices=["build", "test", "upload", "all", "init_git"],
        help="Choose the action to perform: build, test, upload, all, or init_git."
    )
    
    args = parser.parse_args()

    git_manager = GitManager()

    # Execute the action based on the argument passed
    if args.action == "init_git":
        git_manager.init_repository()

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
