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
from .keyboard_mouse_simulation import (mouse_click_position, mouse_move_to, mouse_press_and_move, mouse_scroll,
                                        keyboard_press, keyboard_down, keyboard_up)
from .image_recognition import match_template
from .ocr_recognition import get_text_position
from .exception import TemplateMathingFailure, WindowOutOfBoundsError, TextMatchingFailure
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

        Args:
            game_class (str, None): 游戏类型
            game_name (str): 游戏名称
            debug (bool): 调试模式
            filename (str): 调试模式存储的文件路径
        """
        self.game = Game(game_class, game_name)
        self.debug = debug
        self.filename = filename

    def click_pos(self, pos: Pos) -> None:
        """模拟鼠标点击游戏内坐标API

        Args:
            pos (Pos): 坐标
        """
        self.set_foreground()
        try:
            self._click_pos(pos)
        except WindowOutOfBoundsError:
            self.image_debug("Error")
            raise

    def click_image(self, *images: Union[str, ndarray, MatLike], **kwargs):
        """模拟鼠标点击游戏内图片API

        鼠标点击图片中心位置

        Args:
            images (str, ndarray, MatLike): 图像

        Keyword Arguments:
            threshold (int, float): 匹配阈值(default 0.8)
            mode (str): 匹配模式(default)
        """
        self.set_foreground()
        try:
            self._click_image(*images, **kwargs)
        except TemplateMathingFailure:
            self.image_debug("Error")
            raise

    def click_text(self, text: str, position: str = "center") -> None:
        """模拟鼠标点击游戏内文字API

        Args:
            text (str): 文字
            position (str): 文字位置(default "center") left, center, right
        """
        try:
            self._click_text(text, position)
        except TextMatchingFailure:
            self.image_debug("Error")
            raise

    def down_keyboard_time(self, key: str, stop_time: float, thread=False) -> Union[None, Thread]:
        """模拟按压键盘的时间

        开启线程后将在子线程中运行从而不阻塞主线程，因为这个按压时间是通过time.sleep()实现的

        Args:
            key (str): 键盘按键
            stop_time (float): 按压时间
            thread (bool): 开启线程(default False)

        Returns:
            None | Thread
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
        """模拟鼠标移动API

        鼠标从当前位置移动到pos持续duration

        Args:
            pos (Pos): 坐标
            duration (float): 持续时间
        """
        self.set_foreground()
        try:
            self._mouse_move_to(pos, duration)
        except WindowOutOfBoundsError:
            self.image_debug("Error")
            raise

    def mouse_press_and_move(self, start: Pos, end: Pos) -> None:
        """按压鼠标并移动到end松开API"""
        self.set_foreground()
        try:
            start = self._to_game_pos(start)
            end = self._to_game_pos(end)
        except WindowOutOfBoundsError:
            self.image_debug("Error")
            raise
        mouse_press_and_move(start, end)

    def mouse_scroll(self, pos: Pos, scale: int, count: int, duration=0.0):
        """鼠标移动至pos滚动scale刻度count次
        Args:
            pos (Pos): 坐标
            scale (int): 刻度
            count (int): 次数
            duration (float): 移动到坐标点的时间
        """
        self.set_foreground()
        self.mouse_move_to(pos, duration)
        mouse_scroll(scale, count)

    def wait_image(self, *images: Union[str, ndarray, MatLike], **kwargs) -> None:
        """等待游戏内图片API

        Args:
            images: (str, ndarray, MatLike)可以多张图片，也可以单张图片

        Keyword Arguments:
            all (bool): True等待所有图片，False其中一个图片(default False)
            timeout (int, float): 等待时间(default 60)
            spacing (int, float): 每次匹配时间间隔(default 1)
            threshold (int, float): 达到该阈值算匹配成功(default 0.8)
            mode (str): 匹配模式

        Raises:
            TimeoutError: 超时
        """
        self.set_foreground()
        try:
            self._wait_image(*images, **kwargs)
        except TimeoutError:
            self.image_debug("Error")
            raise

    def _click_pos(self, pos: Pos) -> None:
        """ 点击游戏内某个坐标 """
        game_pos = self._to_game_pos(pos)
        mouse_click_position(game_pos)

    def _click_image(self, *images: Union[str, ndarray, MatLike], **kwargs) -> None:
        """ 点击游戏内图片 """
        threshold = kwargs.get("threshold", 0.8)
        mode = kwargs.get("mode", "color")
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
        log.error(f"template matching failure, max value is {v}")
        raise TemplateMathingFailure(f"Threshold: {v} < {threshold}, GamePos: {p}")

    def _click_text(self, text: str, position: str = "center") -> None:
        """ 点击游戏内文字 """
        positions = get_text_position(self.game.get_screenshot(), text)
        if positions.size == 0:
            raise TextMatchingFailure(f"The text does not exist in the game")
            # 没有匹配到相关的文字
        index = 0
        if position == "center":
            index = (positions.size - 1) // 2
            if index < 0:
                index = 0
        elif position == "right":
            index = -1
        position = positions[index]
        x, y = position
        pos = Pos(int(x), int(y))
        self.click_pos(pos)

    def _mouse_move_to(self, pos: Pos, duration: float) -> None:
        """ 将鼠标移动至某坐标点上 """
        game_pos = self._to_game_pos(pos)
        mouse_move_to(game_pos, duration)

    def _to_game_pos(self, pos: Pos) -> Pos:
        """ 将坐标转换成游戏坐标 """
        if pos.is_game:
            return pos
        rect = self.game.get_rect()
        x1, y1 = pos.x, pos.y
        x2, y2 = x1 + rect.left, y1 + rect.top
        game_pos = Pos(x2, y2)
        # 坐标转换成游戏内坐标
        if x2 < rect.left or x2 > rect.right or y2 < rect.top or y2 > rect.bottom:
            log.error(f"The given coordinate ({x2}, {y2}) is outside")
            raise WindowOutOfBoundsError(f"The given coordinate ({x2}, {y2}) is outside "
                                         f"the game window bounds "
                                         f"({rect.left}, {rect.top}) - ({rect.right}, {rect.bottom})")
            # 给出的坐标超出游戏窗口范围
        return game_pos

    def _wait_image(self, *images: Union[str, ndarray, MatLike], **kwargs) -> None:
        """ 等待图片 """
        all_ = kwargs.get("all", False)
        threshold = kwargs.get("threshold", 0.8)
        mode = kwargs.get("mode", "color")
        timeout = kwargs.get("timeout", 60)  # second
        spacing = kwargs.get("spacing", 1)  # second
        start_time = time.time()
        length = len(images)

        while time.time() - start_time <= timeout:
            count = 0
            for image in images:
                screenshot = self.game.get_screenshot()
                _, max_val, _, max_loc = match_template(screenshot, image, mode=mode)
                if max_val >= threshold:
                    count += 1
                    if not all_:
                        # 不需要全部匹配成功
                        return
                if count == length:
                    # 全部匹配成功
                    return
            time.sleep(spacing)
        log.error(f"Wait timeout: timeout={timeout}, spacing={spacing}")
        raise TimeoutError(f"Wait timeout")

    def __image_filename(self, level: str) -> str:
        """ 获取图片保存名称 """
        return os.path.join(self.filename,
                            f"[{level}]" +
                            datetime.now().strftime("%Y-%m-%d (%H-%M-%S)") +
                            ".png")
