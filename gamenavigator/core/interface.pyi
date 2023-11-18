"""界面类
通过创建一个个游戏界面类从而达到操控游戏的目的
"""
from abc import ABC, abstractmethod
from typing import Dict, Optional, Union, Callable

from cv2.typing import MatLike



class InterfaceBase(ABC):
    __obj_name: str
    def __init__(self, obj_name: str) -> None: ...

    @property
    def name(self) -> str: ...
    
    @abstractmethod
    def subinterface(self) -> list: ...
    
    def __str__(self) -> str: ...
    
    def __repr__(self) -> str: ...


class Interface(InterfaceBase):
    __current: "Interface"
    __callable: Optional[Callable]
    __items: Dict[str, "Interface"]
    __parent: Optional["Interface"]
    def __init__(self, i_name: str) -> None:
        super().__init__(i_name)
        self.__current: "Interface" = self
        self.__callable: Optional[Callable] = None
        self.__items: Dict[str, "Interface"] = dict()
        self.__parent: Optional["Interface"] = None
    
    def add_subinterface(self, i_obj: "Interface", callable: Callable) -> None: ...
    
    def back(self) -> None: ...
    
    def callable(self) -> Union[Callable, None]: ...
    
    def current(self) -> "Interface": ...

    def get_subinterface(self, i_name: str) -> "Interface": ...
    
    def parent(self) -> Union["Interface", None]: ...
    
    def subinterface(self) -> list: ...
    
    def _set_current(self, interface: "Interface") -> None: ...
    
    def _set_callable(self, callable: Callable) -> None: ...
    
    def _set_parent(self, interface: "Interface") -> None: ...
    
    def to_subinterface(self, i_name: str) -> None: ...