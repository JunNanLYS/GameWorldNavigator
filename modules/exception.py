class ErrorBase(Exception):
    def __init__(self, mes):
        self.mes = mes

    def __str__(self):
        return self.mes


class TemplateMathingFailure(ErrorBase):
    pass


class WindowOutOfBoundsError(ErrorBase):
    pass


if __name__ == '__main__':
    raise WindowOutOfBoundsError("123")
