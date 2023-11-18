"""界面类
通过创建一个个游戏界面类从而达到操控游戏的目的
"""
from abc import ABC, abstractmethod
from typing import Dict, Optional, Union, Callable

from cv2.typing import MatLike



class InterfaceBase(ABC):
    def __init__(self, obj_name: str) -> None:
        self.__obj_name = obj_name

    @property
    def name(self) -> str:
        return self.__obj_name
    
    @abstractmethod
    def subinterface(self) -> list:
        pass
    
    def __str__(self) -> str:
        return f"<Interface : {self.__obj_name}>"
    
    def __repr__(self) -> str:
        return self.__str__()


class Interface(InterfaceBase):
    def __init__(self, i_name: str) -> None:
        super().__init__(i_name)
        self.__current: "Interface" = self
        self.__callable: Optional[Callable] = None
        self.__items: Dict[str, "Interface"] = dict()
        self.__parent: Optional["Interface"] = None
    
    def add_subinterface(self, i_obj: "Interface", callable: Callable) -> None:
        """ 添加新的子界面 """
        if not isinstance(i_obj, self.__class__):
            raise TypeError("The added object must be of the same type as the current object.")
        i_name = i_obj.name
        if i_name in self.__items:
            raise ValueError(f"A sub-interface named '{i_name}' already exists. Duplicate addition is not allowed.")
        self.__items[i_name] = i_obj
        i_obj._set_parent(self)
        i_obj._set_callable(callable)
    
    def back(self) -> None:
        if self.current() is self:
            pass
        else:
            pass
    
    def callable(self) -> Union[Callable, None]:
        return self.__callable
    
    def current(self) -> "Interface":
        """ 返回当前界面 """
        return self.__current

    def get_subinterface(self, i_name: str) -> "Interface":
        """获取界面

        Args:
            i_name (str): 界面名称
        
        Returns:
            Interface
        """
        if not isinstance(i_name, str):
            raise TypeError("i_name type must is str")
        if i_name not in self.__items:
            raise KeyError(f"not have {i_name}")
        return self.__items[i_name]
    
    def parent(self) -> Union["Interface", None]:
        """ 返回父界面, 若为None则不存在父界面 """
        return self.__parent
    
    def subinterface(self) -> list:
        """ 返回所有子界面 """
        return list(self.__items.values())
    
    def _set_current(self, interface: "Interface") -> None:
        """设置当前界面
        
        当前界面的父界面也会被设置一直递归直至到达顶层父界面
        
        这么做的目的是保证顶层界面的能通过self.current()知道现在是什么界面
        """
        self.__current = interface
        parent = self.parent()
        if parent is None:
            return
        parent._set_current(interface)
    
    def _set_callable(self, callable: Callable) -> None:
        """ 设置callable """
        self.__callable = callable
    
    def _set_parent(self, interface: "Interface") -> None:
        """ 设置父界面 """
        self.__parent = interface
    
    def to_subinterface(self, i_name: str) -> None:
        """ 前往子界面 """
        interface = self.get_subinterface(i_name)
        call = interface.callable()
        if call is None:
            raise ValueError()
        call()
        self._set_current(interface)