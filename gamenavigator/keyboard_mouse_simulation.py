"""模拟键盘鼠标

"""
import time

import pyautogui
import win32api
import win32con

from .core import Pos
from . import log


def mouse_move_to(pos: Pos, duration: float = 0.0) -> None:
    """ 模拟鼠标移动 """
    if not isinstance(pos, Pos):
        raise TypeError("pos must be Pos")
    if not isinstance(duration, float):
        raise TypeError("duration must be float")
    pyautogui.moveTo(pos.x, pos.y, duration)
    log.debug(f"mouse move to {pos}")


def mouse_click_position(pos: Pos, button: str = "left") -> None:
    """ 模拟鼠标点击坐标pos """
    if not isinstance(pos, Pos):
        raise TypeError("pos must be Pos")
    if not isinstance(button, str):
        raise TypeError("button must be str")
    if button not in ("left", "right"):
        raise ValueError("button must be left or right")
    if button == "left":
        down = win32con.MOUSEEVENTF_LEFTDOWN
        up = win32con.MOUSEEVENTF_LEFTUP
    else:
        down = win32con.MOUSEEVENTF_RIGHTDOWN
        up = win32con.MOUSEEVENTF_RIGHTUP
    x, y = pos.x, pos.y
    win32api.SetCursorPos((x, y))
    win32api.mouse_event(down, x, y, 0, 0)
    time.sleep(0.15)  # 过快的点击将导致游戏反应不过来最终导致点击失效
    win32api.mouse_event(up, x, y, 0, 0)
    log.debug(f"mouse click({button}): {pos}")


def mouse_scroll(scale: int, count: int = 1) -> None:
    """鼠标滚轮滚动
    这个“刻度”的具体滚动距离取决于你的系统设置和鼠标驱动。

    Args:
        scale (int): 刻度
        count (int): 次数
    """
    if not isinstance(scale, int):
        raise TypeError("scale must be int")
    if not isinstance(count, int):
        raise TypeError("count must be int")
    if count < 1:
        raise ValueError("count must be greater than 0")
    for _ in range(count):
        try:
            pyautogui.scroll(scale)
        except pyautogui.FailSafeException:
            print("Scrolling stopped due to failure.")
            break
        time.sleep(0.1)  # 添加0.1秒的延迟
    log.debug(f"mouse scroll scale : {scale}, count : {count}")


def mouse_drag(start: Pos, end: Pos, button='left') -> None:
    """鼠标拖拽

    Args:
        start (Pos): 起点
        end (Pos): 终点
        button (str): 鼠标按键. (default left)
    """
    if not isinstance(start, Pos):
        raise TypeError("start must be Pos")
    if not isinstance(end, Pos):
        raise TypeError("end must be Pos")
    if not button in ('left', 'right', 'middle'):
        raise ValueError("button must be left, right or middle")
    x1, y1 = start.x, start.y
    x2, y2 = end.x, end.y
    pyautogui.mouseDown(x1, y1, button)
    pyautogui.moveTo(x2, y2, duration=1)
    pyautogui.mouseUp(x1, y1)
    log.debug(f"mouse down move start : {start}, end : {end}")


def mouse_click(button: str) -> None:
    """鼠标点击

    Args:
        button (str): left or right or middle (default left)
    """
    if not isinstance(button, str):
        raise TypeError("button must be str")
    button = button.lower()
    if button == "left":
        pyautogui.leftClick()
    elif button == "right":
        pyautogui.rightClick()
    elif button == "middle":
        pyautogui.middleClick()
    else:
        ValueError(f"button must be left or right, not {button}")
    log.debug(f"mouse click button : {button}")


def mouse_double_click() -> None:
    """ 双击左键 """
    pyautogui.doubleClick()
    log.debug("mouse double click")


def keyboard_down(key: str) -> None:
    """ 模拟键盘按键按下 """
    if not isinstance(key, str):
        raise TypeError("key must be str")
    pyautogui.keyDown(key)
    log.debug(f"keyboard down: {key}")


def keyboard_up(key: str) -> None:
    """ 模拟键盘按键松开 """
    if not isinstance(key, str):
        raise TypeError("key must be str")
    pyautogui.keyUp(key)
    log.debug(f"keyboard up: {key}")


def keyboard_press(key: str) -> None:
    """ 模拟键盘按键轻按 """
    if not isinstance(key, str):
        raise TypeError("key must be str")
    pyautogui.press(key)
    log.debug(f"keyboard press: {key}")


if __name__ == '__main__':
    pass
