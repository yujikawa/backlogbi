from enum import Enum

class Menu(Enum):
    DASHBOARD = 'Dashboard'
    SETTING = 'Settings'

    @staticmethod
    def get_menus():
        return [Menu.DASHBOARD.name, Menu.SETTING.name]