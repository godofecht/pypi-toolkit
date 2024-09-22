import argparse
import logging
import subprocess
import sys

def run_command(command):
    logging.info(f"Running command: {command}")
    result = subprocess.run(command, shell=True)
    if result.returncode != 0:
        logging.error(f"Command failed: {command}")
        sys.exit(result.returncode)

def install_twine():
    try:
        import twine
    except ImportError:
        logging.info("Twine not found. Installing twine...")
        run_command("pip install twine")

def build_package():
    logging.info("Building the package...")
    run_command("python setup.py sdist bdist_wheel")

def run_tests():
    logging.info("Running tests...")
    run_command("pytest")

def upload_to_pypi():
    logging.info("Uploading the package to PyPI...")
    run_command("twine upload dist/*")

def main():
    # Set up logging
    logging.basicConfig(level=logging.INFO)

    # Set up argument parser with help messages
    parser = argparse.ArgumentParser(
        description="pypi-toolkit: A utility to build, test, and upload Python packages to PyPI",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument(
        "action",
        choices=["build", "test", "upload", "all"],
        help="Action to perform: \n"
             "'build' - Build the Python package.\n"
             "'test' - Run tests using pytest.\n"
             "'upload' - Upload the package to PyPI.\n"
             "'all' - Run all the above actions in sequence."
    )

    # Parse the arguments
    args = parser.parse_args()

    # Perform actions based on the provided arguments
    if args.action in ["build", "all"]:
        build_package()

    if args.action in ["test", "all"]:
        run_tests()

    if args.action in ["upload", "all"]:
        install_twine()
        upload_to_pypi()

    logging.info("Process completed successfully.")

if __name__ == "__main__":
    main()
