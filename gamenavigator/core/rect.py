class Rect:
    def __init__(self, left: int, top: int, right: int, bottom: int):
        self._top = top
        self._left = left
        self._bottom = bottom
        self._right = right

    @property
    def top(self) -> int:
        return self._top

    @property
    def left(self) -> int:
        return self._left

    @property
    def bottom(self) -> int:
        return self._bottom

    @property
    def right(self) -> int:
        return self._right

    def rect(self) -> tuple[int, int, int, int]:
        return self._left, self._top, self._right, self.bottom

    def __str__(self):
        return f"{self._left, self._top, self._right, self._bottom}"

    def __repr__(self):
        return self.__str__()
