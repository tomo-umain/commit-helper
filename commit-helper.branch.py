import os

# constants
BRANCH_TYPES_ALLOWED = ["feature", "bugfix", "hotfix", "task", "release"]

MESSAGES = {
    "branch_type": "Branch type (" + ", ".join(BRANCH_TYPES_ALLOWED) + "): ",
    "webchan_id": "Enter WEBCHAN ID: ",
    "description": "Enter a short branch description (no quotes): ",
    "confirm": "Press Enter to create branch or Ctrl+C to cancel...",
}


# error exceptions
class BranchTypeError(Exception):
    def __init__(self):
        self.message1 = "Branch type is not allowed."
        self.message2 = "Allowed: " + ", ".join(BRANCH_TYPES_ALLOWED)
        super().__init__(f"{self.message1}\n{self.message2}")


class GitRepoError(Exception):
    def __init__(self):
        super().__init__("Not a valid Git repository.")


class WebchanError(Exception):
    def __init__(self):
        super().__init__("Invalid WEBCHAN ID. Only numbers are allowed.")


class DescriptionError(Exception):
    def __init__(self):
        super().__init__("Description cannot be empty.")


# object models
class UtilsManager:
    @staticmethod
    def get_integers_from_string(string):
        return "".join(filter(str.isdigit, string))

    def prompt(
        self,
        message="",
        webchan_id="",
        branch_type="",
    ):
        parts = []
        if webchan_id:
            parts.append(self.color_text("gold", f"[WEBCHAN-{webchan_id}]"))
        if branch_type:
            parts.append(self.color_text("green", f"[{branch_type}]"))
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
        self.webchan_id = None
        self.branch_type = None
        self.prompt = UtilsManager().prompt
        self.color_text = UtilsManager().color_text

    @staticmethod
    def validate_git_repo():
        if not os.path.exists(".git"):
            raise GitRepoError()

    def validate_webchan(self, webchan_id):
        webchan_id = UtilsManager().get_integers_from_string(webchan_id)
        if not webchan_id:
            raise WebchanError()
        return webchan_id

    def validate_type(self, value):
        if value not in BRANCH_TYPES_ALLOWED:
            raise BranchTypeError()

    def validate_description(self, description):
        if not description:
            raise DescriptionError()

    def format_command(self, webchan_id, branch_type, description):
        formatted_description = description.strip().lower().replace(" ", "-")
        return f'git checkout -b "{branch_type}/WEBCHAN-{webchan_id}-{formatted_description}"'

    def prepare(self):
        self.validate_git_repo()

        self.webchan_id = self.prompt(
            MESSAGES["webchan_id"],
        )
        self.webchan_id = self.validate_webchan(self.webchan_id)

        self.branch_type = (
            self.prompt(
                MESSAGES["branch_type"],
                self.webchan_id,
                None,
            )
            .strip()
            .lower()
        )
        self.validate_type(self.branch_type)

        self.description = self.prompt(
            MESSAGES["description"], self.webchan_id, self.branch_type
        )
        self.validate_description(self.description)

        git_branch_command = self.format_command(
            self.webchan_id, self.branch_type, self.description
        )

        print(
            "Command: "
            + self.color_text(
                "green",
                git_branch_command,
            )
        )
        input(MESSAGES["confirm"])
        os.system(git_branch_command)


# setup
def main():
    try:
        branch_manager = BranchManager()
        branch_manager.prepare()
    except Exception as e:
        print(UtilsManager().color_text("red", str(e)))


if __name__ == "__main__":
    main()
