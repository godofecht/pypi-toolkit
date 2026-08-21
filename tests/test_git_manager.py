from pypi_toolkit.git_manager import GitManager


def test_init_repository_initializes_before_configuring(monkeypatch):
    manager = GitManager(git_user="Ada", git_email="ada@example.com")
    calls = []

    monkeypatch.setattr("pypi_toolkit.git_manager.os.path.isdir", lambda path: False)
    monkeypatch.setattr(manager, "run_command", lambda command: calls.append(command))

    manager.init_repository()

    assert calls == [
        ["git", "init"],
        ["git", "config", "user.name", "Ada"],
        ["git", "config", "user.email", "ada@example.com"],
        ["git", "add", "--all"],
        ["git", "commit", "-m", "Initial commit"],
    ]


def test_existing_repository_is_left_alone(monkeypatch):
    manager = GitManager(git_user="Ada", git_email="ada@example.com")
    calls = []

    monkeypatch.setattr("pypi_toolkit.git_manager.os.path.isdir", lambda path: True)
    monkeypatch.setattr(manager, "run_command", lambda command: calls.append(command))

    manager.init_repository()

    assert calls == []
