import numpy as np
from typing import Union
from cv2.typing import MatLike


def __to_ndarray(img: Union[str, np.ndarray, MatLike]) -> Union[np.ndarray, MatLike]: ...


def match_template(img: Union[str, np.ndarray, MatLike], template: Union[str, np.ndarray, MatLike], **kwargs)\
        -> tuple[float, float, tuple[int, int], tuple[int, int]]: ...


def where_img(img: Union[str, np.ndarray, MatLike], template: Union[str, np.ndarray, MatLike], threshold=0.8)\
        -> tuple[tuple[int, int]]: ...
