from abc import abstractmethod, ABC

from pynput import keyboard, mouse


class Listener(ABC):
    def __init__(self):
        self.keyboard_listener = keyboard.Listener(on_press=self.on_press,
                                                   on_release=self.on_release)
        self.mouse_listener = mouse.Listener(on_click=self.on_click)

    @abstractmethod
    def on_press(self, key):
        pass

    @abstractmethod
    def on_release(self, key):
        pass

    @abstractmethod
    def on_click(self, x, y, button):
        pass

    def start(self) -> None:
        self.keyboard_listener.start()
        self.mouse_listener.stop()

    def stop(self) -> None:
        self.keyboard_listener.stop()
        self.mouse_listener.stop()
