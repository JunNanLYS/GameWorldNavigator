""" 这里定义了坐标类 """


class Pos:
    def __init__(self, *args) -> None:
        """
        Initialize a new Pos object.

        * Pos(tuple): where tuple is of the form (x, y)
        * Pos(x, y): where x and y are integers
        """
        if len(args) == 1:
            arg = args[0]
            if isinstance(arg, tuple):
                if len(arg) != 2:
                    raise TypeError("Tuple must have exactly two elements")
                self._x, self._y = arg
            else:
                raise TypeError("If a single argument is provided, it must be a tuple of two integers")
        elif len(args) == 2:
            if isinstance(args[0], int) and isinstance(args[1], int):
                self._x, self._y = args
            else:
                raise TypeError("If two arguments are provided, they must be integers")
        else:
            raise TypeError("Pos takes either one tuple or two integers as arguments")

        self.is_game = False

    @property
    def x(self) -> int:
        return self._x

    @property
    def y(self) -> int:
        return self._y

    def __add__(self, other):
        return Pos(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Pos(self.x - other.x, self.y - other.y)

    def __str__(self):
        return f"Pos({self._x}, {self._y})"

    def __repr__(self):
        return self.__str__()


if __name__ == '__main__':
    p = Pos(1, 2)
    print(p)
