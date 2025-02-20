
class FailedExecutionError(Exception):
    """Exception for missing submodules."""
    def __init__(self, command, message="Failed to execute: "):
        self.message = message + command
        super().__init__(self.message)

class MissingDependenciesError(Exception):
    """Exception for missing submodules."""
    def __init__(self, submodule, message="Could not find submodule: "):
        self.message = message + submodule
        super().__init__(self.message)