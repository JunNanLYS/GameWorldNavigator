import os.path
import time
import ctypes
from datetime import datetime
from typing import Union
from threading import Thread

import win32api
import win32con
import win32gui
import win32print
import cv2
from PIL import ImageGrab
from cv2.typing import MatLike
from numpy import ndarray, array

from .core import Pos, Rect
from .keyboard_mouse_simulation import (mouse_click_position, mouse_move_to, keyboard_press,
                                        keyboard_down, keyboard_up)
from .image_recognition import match_template
from .exception import TemplateMathingFailure, WindowOutOfBoundsError
from . import log


def _get_screen_size():
    """ 电脑缩放后的分辨率 """
    w = win32api.GetSystemMetrics(0)
    h = win32api.GetSystemMetrics(1)
    return w, h


def _get_read_size():
    """ 获取电脑真实分辨率 """
    hdc = win32gui.GetDC(0)
    w = win32print.GetDeviceCaps(hdc, win32con.DESKTOPHORZRES)
    h = win32print.GetDeviceCaps(hdc, win32con.DESKTOPVERTRES)
    return w, h


def _get_scaling() -> float:
    """ 获取电脑缩放率 """
    return round(_get_read_size()[0] / _get_screen_size()[0], 2)


class Game:
    def __init__(self, game_class: Union[str, None], game_name: str):
        """
        :param game_class: 游戏类名
        :param game_name: 游戏名称
        """
        self.screenshot = None
        self._game_class = game_class
        self._game_name = game_name
        self._hwnd = win32gui.FindWindow(game_class, game_name)

        log.debug(f"class:{game_class}, name: {game_name}, hwnd: {self._hwnd}")

    @property
    def cls(self) -> str:
        return self._game_class

    @property
    def hwnd(self) -> int:
        return self._hwnd

    @property
    def width(self) -> int:
        rect = self.get_rect()
        return rect.right - rect.left

    @property
    def height(self) -> int:
        rect = self.get_rect()
        return rect.bottom - rect.top

    @property
    def top_left(self) -> Pos:
        rect = self.get_rect()
        pos = Pos(rect.left, rect.top)
        return pos

    @property
    def scaling(self) -> float:
        return ctypes.windll.user32.GetDpiForWindow(self._hwnd) / 96.0

    @property
    def name(self) -> str:
        return self._game_name

    def set_foreground(self) -> None:
        """ 设置游戏到前台API """
        win32gui.ShowWindow(self._hwnd, win32con.SW_RESTORE)
        win32gui.SetForegroundWindow(self._hwnd)

    def get_screenshot(self) -> ndarray:
        """ 游戏截图API """
        grab = ImageGrab.grab(bbox=(self.get_rect().rect()))
        img = array(grab)
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        self.screenshot = img
        return img

    def get_rect(self) -> Rect:
        """ 获取游戏的矩形 """
        x1, y1, x2, y2 = win32gui.GetWindowRect(self._hwnd)
        s = _get_scaling()  # 电脑缩放率
        x1, y1 = int(x1 * s), int(y1 * s)
        x2, y2 = int(x2 * s), int(y2 * s)
        return Rect(x1, y1, x2, y2)


class GameController:
    def __init__(self, game_class: Union[str, None], game_name: str, debug=False, filename=""):
        """
        将debug设置为True后需要设置filename才会将调试信息保存
        :param game_class: 游戏类型
        :param game_name: 游戏名称
        :param debug: 调试模式
        :param filename: 调试模式存储的文件路径
        """
        self.game = Game(game_class, game_name)
        self.debug = debug
        self.filename = filename

    def click_pos(self, pos: Pos) -> None:
        """ 模拟鼠标点击游戏内坐标API """
        self.set_foreground()
        try:
            self._click_pos(pos)
        except WindowOutOfBoundsError as e:
            self.image_debug("Error")
            raise WindowOutOfBoundsError(e)

    def click_image(self, *images: Union[str, ndarray, MatLike], **kwargs):
        """ 模拟鼠标点击游戏内图片API """
        self.set_foreground()
        try:
            self._click_image(*images, **kwargs)
        except TemplateMathingFailure as e:
            self.image_debug("Error")
            raise TemplateMathingFailure(e)

    def down_keyboard_time(self, key: str, stop_time: float, thread=False):
        """模拟按压键盘的时间
        :param key: 键盘按键
        :param stop_time: 按压时长
        :param thread: True开启子线程 | False不开启子线程
        :return: 若开启子线程则返回子线程实例，反之返回None
        """
        self.set_foreground()

        def func():
            keyboard_down(key)
            time.sleep(stop_time)
            keyboard_up(key)

        if thread:
            t = Thread(target=func)
            t.start()
            return t
            # 运行子线程并且返回子线程
        func()
        # 阻塞当前线程直到达到按压时长

    def image_debug(self, level="Debug") -> None:
        """ 保存调试照片 """
        if self.debug and self.filename:
            filename = self.__image_filename(level)
            cv2.imwrite(filename, self.game.screenshot)

    def press(self, key: str) -> None:
        """ 模拟键盘按键按压API """
        self.set_foreground()
        keyboard_press(key)

    def set_foreground(self) -> None:
        """ 设置游戏到前台 """
        hwnd = win32gui.GetForegroundWindow()
        text = win32gui.GetWindowText(hwnd)
        if text != self.game.name:
            self.game.set_foreground()
            time.sleep(1)

    @property
    def screenshot(self) -> ndarray:
        return self.game.screenshot

    def mouse_move_to(self, pos: Pos, duration: float) -> None:
        """ 模拟鼠标移动API """
        self.set_foreground()
        try:
            self._mouse_move_to(pos, duration)
        except WindowOutOfBoundsError as e:
            self.image_debug("Error")
            raise WindowOutOfBoundsError(e)

    def _click_pos(self, pos: Pos):
        """ 点击游戏内某个坐标 """
        game_pos = self.__to_game_pos(pos)
        mouse_click_position(game_pos)

    def _click_image(self, *images: Union[str, ndarray, MatLike], **kwargs):
        """ 点击游戏内图片 """
        threshold = kwargs.get("threshold", 0.8)
        mode = kwargs.get("mode", "default")
        screenshot = self.game.get_screenshot()
        v, p = 0, Pos(0, 0)
        log.debug(f"click image: threshold={threshold}, mode={mode}")
        for image in images:
            _, max_val, _, max_loc = match_template(screenshot, image, mode=mode)
            if max_val < threshold:
                if max_val > v:
                    v = max_val
                    p = Pos(max_loc)
                continue
                # 低于阈值的跳过
            else:
                log.debug(f"max_val={max_val}, threshold={threshold}")
                w, h = screenshot.shape[:1]
                center = Pos(max_loc[0] + w // 2, max_loc[1] + h // 2)
                self.click_pos(center)
        raise TemplateMathingFailure(f"Threshold: {v} < {threshold}, GamePos: {p}")

    def _mouse_move_to(self, pos: Pos, duration: float) -> None:
        """ 将鼠标移动至某坐标点上 """
        game_pos = self.__to_game_pos(pos)
        mouse_move_to(game_pos, duration)

    def __image_filename(self, level: str) -> str:
        """ 获取图片保存名称 """
        return os.path.join(self.filename,
                            f"[{level}]" +
                            datetime.now().strftime("%Y-%m-%d (%H-%M-%S)") +
                            ".png")

    def __to_game_pos(self, pos: Pos) -> Pos:
        """ 将坐标转换成游戏坐标 """
        rect = self.game.get_rect()
        x1, y1 = pos.x, pos.y
        x2, y2 = x1 + rect.left, y1 + rect.top
        game_pos = Pos(x2, y2)
        # 坐标转换成游戏内坐标
        if x2 < rect.left or x2 > rect.right or y2 < rect.top or y2 > rect.bottom:
            raise WindowOutOfBoundsError(f"The given coordinate ({x2}, {y2}) is outside "
                                         f"the game window bounds "
                                         f"({rect.left}, {rect.top}) - ({rect.right}, {rect.bottom})")
            # 给出的坐标超出游戏窗口范围
        return game_pos


if __name__ == '__main__':
    pass
