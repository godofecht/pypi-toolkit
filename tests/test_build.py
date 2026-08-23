import os
import sys

import pytest

from pypi_toolkit import build


def test_build_package_uses_current_python(monkeypatch):
    calls = []
    monkeypatch.setattr(
        build, "run_command", lambda command, **kwargs: calls.append((command, kwargs))
    )

    build.build_package()

    assert calls == [([sys.executable, "-m", "build"], {})]


def test_run_tests_uses_current_python(monkeypatch):
    calls = []
    monkeypatch.setattr(
        build, "run_command", lambda command, **kwargs: calls.append((command, kwargs))
    )

    build.run_tests()

    assert calls == [([sys.executable, "-m", "pytest"], {})]


def test_upload_requires_credentials(monkeypatch):
    for key in ("TWINE_USERNAME", "TWINE_PASSWORD", "PYPI_USERNAME", "PYPI_PASSWORD"):
        monkeypatch.delenv(key, raising=False)

    with pytest.raises(RuntimeError, match="PyPI credentials are missing"):
        build.upload_to_pypi()


def test_upload_passes_credentials_via_environment(monkeypatch, tmp_path):
    dist = tmp_path / "dist"
    dist.mkdir()
    artifact = dist / "example-1.0.0.tar.gz"
    artifact.write_text("artifact")
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("PYPI_USERNAME", "__token__")
    monkeypatch.setenv("PYPI_PASSWORD", "secret")

    calls = []
    monkeypatch.setattr(
        build, "run_command", lambda command, **kwargs: calls.append((command, kwargs))
    )

    build.upload_to_pypi()

    command, kwargs = calls[0]
    assert command == [
        sys.executable,
        "-m",
        "twine",
        "upload",
        os.fspath(artifact.relative_to(tmp_path)),
    ]
    assert kwargs["env"]["TWINE_USERNAME"] == "__token__"
    assert kwargs["env"]["TWINE_PASSWORD"] == "secret"
    assert "secret" not in command


def test_all_runs_test_build_upload_in_safe_order(monkeypatch):
    calls = []
    monkeypatch.setattr(build, "run_tests", lambda: calls.append("test"))
    monkeypatch.setattr(build, "build_package", lambda: calls.append("build"))
    monkeypatch.setattr(build, "upload_to_pypi", lambda: calls.append("upload"))

    build.main(["all"])

    assert calls == ["test", "build", "upload"]
