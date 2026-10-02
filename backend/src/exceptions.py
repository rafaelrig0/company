class AppError(Exception):
    error_code: str = "APP_ERROR"
    default_message: str = "An unexpected error ocurred."

    def __init__(self, message: str | None = None):
        self.message = message
        super().__init__(self.message)

class EmailAlreadyExistsError(AppError):
    error_code="EMAIL_ALREADY_EXISTS"
    default_message="Email already registered!"

class NotFoundError(AppError):
    error_code ="NOT_FOUND"
    default_message ="The requested resource was not found."

class PermissionDeniedError(AppError):
    error_code ="PERMISSION_DENIED"
    default_message="You do not have permission to perform this action!"