import os
import pickle


class Setting(object):

    def __init__(self):
        os.makedirs('./data', exist_ok=True)
        self.__settings = self.load()

    def set_setting(self, key, value) -> None:
        self.__settings[key] = value

    @staticmethod
    def load():
        if os.path.isfile('./data/setting.pkl'):
            with open('./data/setting.pkl', 'rb') as f:
                settings = pickle.load(f)
                return settings
        else:
            return {}

    def save(self):
        with open('./data/setting.pkl', 'wb') as f:
            pickle.dump(self.__settings, f)

    def get_setting(self):
        return self.__settings
