# pypi_toolkit/build.py

import os
import subprocess
import sys
import argparse
import logging

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
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
    
    parser = argparse.ArgumentParser(
        description="A toolkit for building, testing, and uploading Python packages to PyPI."
    )
    
    parser.add_argument(
        "action",
        choices=["build", "test", "upload", "all"],
        help="Choose the action to perform: build, test, upload, or all."
    )
    
    args = parser.parse_args()

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
