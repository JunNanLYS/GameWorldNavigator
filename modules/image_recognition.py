import cv2
import numpy as np
from typing import Union
from cv2.typing import MatLike


def __to_ndarray(img: Union[str, np.ndarray, MatLike]) -> Union[np.ndarray, MatLike]:
    """ 若img是图像路径则读取后返回，否则直接返回 """
    if isinstance(img, str):
        img = cv2.imread(img)
    return img


def match_template(img: Union[str, np.ndarray, MatLike], template: Union[str, np.ndarray, MatLike], *args, **kwargs) \
        -> tuple:
    """图像匹配
    使用的是cv2的模板匹配，必须要保证 img 和 template 是属于同一种类型图像，即都是灰度图或彩色图，且大小一致。
    使用的是cv2.TM_CCOEFF_NORMED进行模板匹配，可以通过修改method来自定义模板匹配。图像必须是BGR格式

    接受一下几种关键词：
    method: 模板匹配方法，默认是TM_CCOEFF_NORMED  str类型
    mode: 匹配模式，它接受 default gray binary 这三种值,默认模式是default  str类型
    thresh: 只有在二值图模式下才有用  int类型
    max_val: 只有在二值图模式下才有用  int类型

    返回一个tuple类型 (min_val, max_val, min_loc, max_loc)
    """
    if not isinstance(img, (str, np.ndarray, MatLike)):
        raise TypeError("only accept  str or np.ndarray or MatLike")
    elif not isinstance(template, (str, np.ndarray, MatLike)):
        raise TypeError("only accept  str or np.ndarray or MatLike")

    img = __to_ndarray(img)
    template = __to_ndarray(template)

    method = kwargs.get("method", cv2.TM_CCOEFF_NORMED)
    methods = ("TM_SQDIFF", "TM_SQDIFF_NORMED", "TM_CCOEFF_NORMED",
               "TM_CCORR_NORMED", "TM_CCORR", "TM_CCOEFF")
    mode = kwargs.get("mode", "default")
    modes = ("default", "gray", "binary")

    # 判断传入的关键词是否支持
    if method not in methods:
        raise ValueError(f"method must in {methods}")
    elif mode not in modes:
        raise ValueError(f"mode must in {modes}")

    method = getattr(cv2, method)
    i_channel = img.ndim
    t_channel = template.ndim

    if mode == "gray" or mode == "binary":
        if i_channel == 3:
            img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        else:
            img_gray = img
        if t_channel == 3:
            template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
        else:
            template_gray = template
    else:
        img_gray = None
        template_gray = None
    # 若模式需要灰度图则先将彩色图转换成灰度图

    if mode == "default":
        if i_channel != 3 or t_channel != 3:
            raise ValueError("Image or template channels not equal to 3")
        res = cv2.matchTemplate(img, template, method)
        return cv2.minMaxLoc(res)
        # 彩色图模式
    elif mode == "gray":
        res = cv2.matchTemplate(img_gray, template_gray, method)
        return cv2.minMaxLoc(res)
        # 灰度图模式
    else:
        thresh = kwargs.get("thresh", 127)
        max_val = kwargs.get("max_val", 255)
        _, img_binary = cv2.threshold(img_gray, thresh, max_val, cv2.THRESH_BINARY)
        _, template_binary = cv2.threshold(template_gray, thresh, max_val, cv2.THRESH_BINARY)
        res = cv2.matchTemplate(img_binary, template_binary, method)
        return cv2.minMaxLoc(res)
        # 二值图模式


def where_img(img: Union[str, np.ndarray, MatLike], template: Union[str, np.ndarray, MatLike], threshold=0.8) -> tuple:
    """
    查找目标图中所有符合阈值的模板图位置，暂时只支持cv2.TM_CCOEFF_NORMED。
    :param img: 目标图
    :param template: 模板图
    :param threshold: 符合该阈值的留下
    :return: tuple[(x, y), (x, y)]
    """
    img = __to_ndarray(img)
    template = __to_ndarray(template)
    res = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
    positions = np.where(res >= threshold)
    return tuple(zip(*positions[::-1]))
