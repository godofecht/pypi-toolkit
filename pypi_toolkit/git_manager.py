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