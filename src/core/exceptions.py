from fastapi import status


class ProjectBaseException(Exception):

    def __init__(self, status_code: int, msg: str):
        self.status_code = status_code
        self.message = msg


class NotFoundException(ProjectBaseException):
    def __init__(self, message: str):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, msg=message)

