import os
from git import Repo


class ModelTrainingLog:
    """A training and configuration log for ML models."""

    current_hash = None
    data_hashes = {}

    def __init__(self, git_root=None, log_file=None):
        self.git_root = git_root or os.path.dirname(os.path.realpath(__file__))
        self.log_file_location = log_file or os.path.join(self.git_root, "training_log_file.json")
        self.repo = Repo(self.git_root)

    def commit(self, add_new_files=False):
        """Commit to the git repo and save the hash."""
        self.repo.index.add("*.ipynb")
        self.repo.index.add("*.py")
        message = input("Please give us a nice git commit message.")
        self.repo.index.commit(message)
        print("Committed latest cvhange")


    def check_for_non_log_changes(self):
        """Check that nothing has changed before saving against a given commit hash."""
        index = self.repo.index
        diff = index.diff(None)
        if len(diff) > 0:
            # Check if it's just the log file that changed.
            if len(diff) == 1:
                if diff[0].b_path == os.path.relpath(self.log_file_location, self.git_root):
                    return
            raise ChangesMadeError("There have been changes made to this repo since "
                       "the last commit. Please commit before training again.")

    def create_log_file(self, recreate=False):
        """Creates a blank log file."""
        if not os.path.isfile(self.log_file_location) or recreate:
            open(self.log_file_location, 'w')


class ChangesMadeError(Exception):
    pass