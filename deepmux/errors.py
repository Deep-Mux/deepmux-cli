class DeepmuxCLIError(Exception):
    ...


class UnknownException(DeepmuxCLIError):
    ...


class LoginRequired(DeepmuxCLIError):
    ...


class NameConflict(DeepmuxCLIError):  # 409
    ...


class NotFound(DeepmuxCLIError):  # 404
    ...
