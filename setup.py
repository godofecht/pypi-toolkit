# setup.py

from setuptools import setup, find_packages
import os

# Read the README file for the long description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read the version from the package
version = {}
with open(os.path.join("pypi_toolkit", "__init__.py")) as fp:
    exec(fp.read(), version)

setup(
    name="pypi-toolkit",
    version=version['__version__'],
    author="Your Name",
    author_email="your.email@example.com",
    description="A toolkit for building, testing, and uploading Python packages to PyPI",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/pypi-toolkit",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'twine',
        'pytest',
    ],
    entry_points={
        'console_scripts': [
            'pypi-toolkit=pypi_toolkit.build:main',
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
