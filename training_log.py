import json
import os
from git import Repo


class ModelTrainingLog:
    """A training and configuration log for ML models."""

    data_hashes = {}
    _current_hash = None
    training_params = {}
    train_results = {}
    test_results = {}

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
        print("Committed latest changes, ready to train.")

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
            with open(self.log_file_location, "w") as f:
                json.dump({}, f, ensure_ascii=False, indent=4)

    def _get_current_hash(self):
        self._current_hash = self.repo.head.commit.hexsha
        return self._current_hash

    @property
    def current_hash(self):
        self.check_for_non_log_changes()
        if self._current_hash is None:
            self._get_current_hash()
        return self._current_hash

    def log(self, force=False):
        if not self.training_params:
            raise IncompleteDataError(
                "You have not provided training parameter data. "
                "If this is intentional please use force=True"
            )

        if not self.train_results:
            raise IncompleteDataError(
                "You have not provided training results data. "
                "If this is intentional please use force=True"
            )
        if not self.test_results:
            raise IncompleteDataError(
                "You have not provided test results data. "
                "If this is intentional please use force=True"
            )
        log_line = {"training_parameters": self.training_params,
                    "training_results": self.train_results,
                    "test_results": self.test_results}
        self._write_log_to_file(log_line)
        print("Wrote the training results to the log file.")

    def _write_log_to_file(self, log_line):
        with open(self.log_file_location, "r") as f:
            existing_file = json.load(f)
        existing_file[self.current_hash] = log_line
        with open(self.log_file_location, "w") as f:
            json.dump(existing_file, f, ensure_ascii=False, indent=4)





class ChangesMadeError(Exception):
    pass

class IncompleteDataError(Exception):
    pass