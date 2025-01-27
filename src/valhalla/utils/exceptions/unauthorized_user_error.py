class UnauthorizedUserError(Exception):
    """Exception raised for unauthorized user access."""
    def __init__(self, message="Unauthorized user access. Invalid username or password."):
        self.message = message
        super().__init__(self.message)