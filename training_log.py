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

    def git_commit(self):
        """Commit to the git repo and save the hash."""

    def check_for_non_log_changes(self):
        """Check that nothing has changed before saving against a given commit hash."""
        index = self.repo.index
        diff = index.diff(None)



