"""OCR模块
"""
from ppocronnx import TextSystem
from numpy import ndarray, array

from . import log

system = TextSystem(use_angle_cls=False)


def get_text_position(img: ndarray, text: str) -> ndarray:
    """获取输入的文本坐标

    优先返回与text完全相同的文本的坐标，其次返回相似度最高的文本的坐标，最后返回空坐标

    Args:
        img (ndarray): 图像
        text (str): 文本

    Returns:
        ndarray: 文本坐标
    """
    res = system.detect_and_ocr(img)
    equal = None
    equal_val = 0
    similarity = None
    similarity_val = 0
    for i in range(len(res)):
        box = res[i]
        if box.ocr_text == text:
            if box.score > equal_val:
                equal_val = box.score
                equal = box.box
        if text in box.ocr_text:
            if box.score > similarity_val:
                similarity_val = box.score
                similarity = box.box
    if equal is not None:
        log.debug("have equal text")
        return equal
    elif similarity is not None:
        log.debug("have similarity text")
        return similarity
    log.debug("There are no equal or similar texts")
    return array([])


def text_in_img(img: ndarray, text: str) -> bool:
    """ 判断图片中是否包含该文本 """
    res = get_text_position(img, text)
    return res.size != 0
