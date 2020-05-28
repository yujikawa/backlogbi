from abc import ABCMeta, abstractmethod
from models.setting import Setting


class BaseView(metaclass=ABCMeta):
    def __init__(self, setting: Setting):
        self.setting = setting

    @abstractmethod
    def run(self) -> None:
        raise NotImplementedError()
