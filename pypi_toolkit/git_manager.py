import logging
import os
import subprocess
from collections.abc import Sequence
from dataclasses import dataclass, field


@dataclass
class GitManager:
    git_user: str = field(default_factory=lambda: os.getenv("GIT_USER", ""))
    git_email: str = field(default_factory=lambda: os.getenv("GIT_EMAIL", ""))

    def run_command(self, command: Sequence[str]) -> None:
        logging.info("Running command: %s", " ".join(command))
        subprocess.run(command, check=True, text=True)

    def prompt_for_missing_details(self) -> None:
        if not self.git_user:
            self.git_user = input("Enter your Git username: ").strip()
        if not self.git_email:
            self.git_email = input("Enter your Git email: ").strip()

    def configure_git(self) -> None:
        self.run_command(["git", "config", "user.name", self.git_user])
        self.run_command(["git", "config", "user.email", self.git_email])

    def init_repository(self) -> None:
        if os.path.isdir(".git"):
            logging.info("Git repository already exists.")
            return

        logging.info("Initializing a new Git repository...")
        self.prompt_for_missing_details()
        self.run_command(["git", "init"])
        self.configure_git()
        self.run_command(["git", "add", "--all"])
        self.run_command(["git", "commit", "-m", "Initial commit"])
