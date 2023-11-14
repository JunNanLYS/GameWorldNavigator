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
    pyautogui.moveTo(pos.x, pos.y, duration)
    log.debug(f"mouse move to {pos}")


def mouse_click_position(pos: Pos, button: str = "left") -> None:
    """ 模拟鼠标点击坐标pos """
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
    :param scale: 刻度
    :param count: 次数
    """
    for _ in range(count):
        try:
            pyautogui.scroll(scale)
        except pyautogui.FailSafeException:
            print("Scrolling stopped due to failure.")
            break
        time.sleep(0.1)  # 添加0.1秒的延迟
    log.debug(f"mouse scroll: [scale|{scale}], [count|{count}]")


def mouse_press_and_move(start: Pos, end: Pos, button='left') -> None:
    """按压鼠标移动到达目标点放开
    :param start: 鼠标起点
    :param end: 鼠标终点
    :param button: 鼠标按键 left right
    """
    x1, y1 = start.x, start.y
    x2, y2 = end.x, end.y
    pyautogui.mouseDown(x1, y1, button)
    pyautogui.moveTo(x2, y2, duration=1)
    pyautogui.mouseUp(x1, y1)
    log.debug(f"mouse down move: [start|{start}], [end|{end}]")


def keyboard_down(key: str) -> None:
    """ 模拟键盘按键按下 """
    pyautogui.keyDown(key)
    log.debug(f"keyboard down: {key}")


def keyboard_up(key: str) -> None:
    """ 模拟键盘按键松开 """
    pyautogui.keyUp(key)
    log.debug(f"keyboard up: {key}")


def keyboard_press(key: str) -> None:
    """ 模拟键盘按键轻按 """
    pyautogui.press(key)
    log.debug(f"keyboard press: {key}")


class MouseSimulation:
    pass


class KeyboardSimulation:
    pass


if __name__ == '__main__':
    pass
