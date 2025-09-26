import os

# constants
COMMIT_TYPES_ALLOWED = ["feat", "fix", "chore", "docs", "test", "refactor"]

MESSAGES = {
    "commit_type": "Commit type (" + ", ".join(COMMIT_TYPES_ALLOWED) + "): ",
    "commit_message": "Commit message (no quotes): ",
    "confirm": "Press Enter to commit or Ctrl+C to cancel...",
}


# error exceptions
class CommitTypeError(Exception):
    def __init__(self):
        self.message1 = "Commit type is not allowed."
        self.message2 = "Allowed: " + ", ".join(COMMIT_TYPES_ALLOWED)
        super().__init__(f"{self.message1}\n{self.message2}")


class CommitMessageEmptyError(Exception):
    def __init__(self):
        super().__init__("Commit message cannot be empty.")


class WebchanError(Exception):
    def __init__(self):
        super().__init__(
            "No WEBCHAN found in branch name. Switch to correct branch or create one."
        )


# object models
class UtilsManager:
    @staticmethod
    def get_integers_from_string(string):
        return "".join(filter(str.isdigit, string))

    def prompt(
        self,
        message="",
        webchan_id="",
        commit_type="",
    ):
        parts = []
        if webchan_id:
            parts.append(self.color_text("gold", f"[WEBCHAN-{webchan_id}]"))
        if commit_type:
            parts.append(self.color_text("green", f"[{commit_type}]"))
        return input(" ".join(parts) + " " + message)

    def color_text(self, color, text):
        colors = {
            "red": "\033[91m",
            "green": "\033[92m",
            "gold": "\033[93m",
            "reset": "\033[0m",
        }
        return f"{colors.get(color, colors['reset'])}{text}{colors['reset']}"


class BranchManager:
    def __init__(self):
        self.branch_name = self.get_branch()
        self.webchan_id = self.get_webchan()

    @staticmethod
    def get_branch():
        return os.popen("git rev-parse --abbrev-ref HEAD").read().strip()

    def get_webchan(self):
        try:
            webchan_id = UtilsManager().get_integers_from_string(
                self.branch_name.lower().split("/webchan-")[1].split("/")[0]
            )
            if webchan_id:
                return webchan_id
        except:
            raise WebchanError()


class CommitManager:
    def __init__(self):
        self.commit_type = None
        self.commit_message = None
        self.prompt = UtilsManager().prompt
        self.color_text = UtilsManager().color_text

    @staticmethod
    def format_message(commit_type, webchan_id, commit_message):
        return f"{commit_type}(WEBCHAN-{webchan_id}): {commit_message}"

    def format_command(self, commit_type, webchan_id, commit_message):
        return f'git commit -m "{self.format_message(commit_type, webchan_id, commit_message)}"'

    def validate_type(self, value):
        if value not in COMMIT_TYPES_ALLOWED:
            raise CommitTypeError()

    def validate_message(self, value):
        if not value:
            raise CommitMessageEmptyError()

    def prepare(self, webchan_id):
        self.commit_type = (
            self.prompt(
                MESSAGES["commit_type"],
                webchan_id,
                None,
            )
            .strip()
            .lower()
        )
        self.validate_type(self.commit_type)

        self.commit_message = (
            self.prompt(MESSAGES["commit_message"], webchan_id, self.commit_type)
            .strip()
            .lower()
        )
        self.validate_message(self.commit_message)

        commit_command = self.format_command(
            self.commit_type, webchan_id, self.commit_message
        )
        print("Command: " + self.color_text("green", commit_command))
        input(MESSAGES["confirm"])
        os.system(commit_command)


# setup
def main():
    try:
        branch_manager = BranchManager()
        commit_manager = CommitManager()

        commit_manager.prepare(branch_manager.webchan_id)
    except Exception as e:
        print(UtilsManager().color_text("red", str(e)))


if __name__ == "__main__":
    main()
