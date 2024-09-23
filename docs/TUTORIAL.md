=========================
`pypi-toolkit` Tutorial
=========================

This tutorial will guide you through how to install, use, and integrate `pypi-toolkit` into your Python package development workflow, including a section on using it alongside `cookiecutter` for even faster package creation.

---

Table of Contents
=================

1. `What is pypi-toolkit? <#what-is-pypi-toolkit>`_
2. `Installation <#installation>`_
3. `Basic Usage <#basic-usage>`_
4. `Detailed Commands <#detailed-commands>`_
   - `Create Package <#create-package>`_
   - `Build <#build>`_
   - `Test <#test>`_
   - `Upload <#upload>`_
   - `All <#all>`_
5. `Using pypi-toolkit with Cookiecutter <#using-pypi-toolkit-with-cookiecutter>`_

---

What is `pypi-toolkit`?
=======================

`pypi-toolkit` is a command-line utility designed to automate the process of building, testing, and uploading Python packages to PyPI. It simplifies the standard Python packaging workflow by allowing developers to perform these steps in a single or combined command, improving efficiency and reducing errors.

**Features**:
- **Create Package**: Scaffold a new Python package using `cookiecutter` templates.
- **Build**: Creates a source distribution and wheel for your Python package.
- **Test**: Runs unit tests using `pytest`.
- **Upload**: Uploads your package to PyPI (or TestPyPI).
- **All**: Runs all the above actions in sequence.

---

Installation
============

You can install `pypi-toolkit` either locally (for development purposes) or directly from PyPI once it's published.

Install Locally
---------------

If you want to install it for local development:

.. code-block:: bash

   pip install -e .

This allows you to modify the code and instantly see the changes.

Install from PyPI
-----------------

Once the package is uploaded to PyPI, install it using:

.. code-block:: bash

   pip install pypi-toolkit

---

Basic Usage
===========

After installing, you can use `pypi-toolkit` via the command line to handle your Python package lifecycle.

Example Command:

.. code-block:: bash

   pypi-toolkit <action>

Where `<action>` can be one of the following:
- `create_package`: Scaffold a new Python package using `cookiecutter`.
- `build`: Build the package.
- `test`: Run the tests using `pytest`.
- `upload`: Upload the package to PyPI.
- `all`: Perform all three actions in sequence (build, test, upload).

---

Detailed Commands
=================

Create Package
--------------

Creates a new Python package using a `cookiecutter` template. By default, it uses a popular Python package template from `cookiecutter`.

.. code-block:: bash

   pypi-toolkit create_package

This command will invoke `cookiecutter` with the default template URL:

.. code-block:: bash

   https://github.com/audreyr/cookiecutter-pypackage

Build
-----

Builds your Python package into source distributions and wheels, making it ready for distribution.

.. code-block:: bash

   pypi-toolkit build

This command will run the following under the hood:

.. code-block:: bash

   python setup.py sdist bdist_wheel

The output is stored in the `dist/` folder, which contains the `.tar.gz` and `.whl` files necessary for distribution.

Test
----

Runs unit tests using `pytest`. Ensure that your `tests/` directory is set up correctly before running this command.

.. code-block:: bash

   pypi-toolkit test

This command will automatically run:

.. code-block:: bash

   pytest

Upload
------

Uploads the built distribution files to PyPI. It will also check if `twine` is installed, and install it if necessary.

.. code-block:: bash

   pypi-toolkit upload

This command performs:

.. code-block:: bash

   twine upload dist/*

To upload to TestPyPI (for testing purposes), use the following command instead:

.. code-block:: bash

   pypi-toolkit upload --repository-url https://test.pypi.org/legacy/

All
---

Runs the entire pipeline: build, test, and upload in one go. This is useful for automating the full release process.

.. code-block:: bash

   pypi-toolkit all

This command will sequentially:
- Build the package
- Run the tests
- Upload the package to PyPI

---

Using `pypi-toolkit` with Cookiecutter
======================================

You can further accelerate your development workflow by combining `pypi-toolkit` with `cookiecutter`, a tool that helps generate project templates.

What is Cookiecutter?
---------------------

`cookiecutter` is a command-line utility that creates projects from templates. These templates can include everything you need for a basic Python package, including `setup.py`, `README.md`, and necessary directory structures.

Installation
------------

If you don’t have `cookiecutter` installed yet, you can install it via pip:

.. code-block:: bash

   pip install cookiecutter

Step 1: Choose a Python Package Template
----------------------------------------

You can use any `cookiecutter` Python package template. For instance, the popular `audreyr/cookiecutter-pypackage` template can be used to scaffold a Python package:

.. code-block:: bash

   cookiecutter https://github.com/audreyr/cookiecutter-pypackage

This will guide you through a series of prompts to set up your Python package project, generating files like `setup.py`, `tests/`, `README.md`, and others for you.

Step 2: Create a Package with `pypi-toolkit`
--------------------------------------------

Alternatively, you can use `pypi-toolkit` directly to create a Python package using `cookiecutter`.

.. code-block:: bash

   pypi-toolkit create_package

This will invoke `cookiecutter` using the default template URL and scaffold a Python package in just one step.

---

Automating the Workflow
=======================

To streamline the process even further, you can create a Makefile or bash script to automate the `cookiecutter` setup and `pypi-toolkit` commands in a single command.

Example Makefile:

.. code-block:: makefile

   setup:
   	pypi-toolkit create_package

   build:
   	pypi-toolkit build

   test:
   	pypi-toolkit test

   upload:
   	pypi-toolkit upload

With this setup, you could scaffold a new package, build it, test it, and upload it with just a few commands.
