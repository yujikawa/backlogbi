import os
import pickle


class Setting(object):
    def __init__(self):
        os.makedirs('./data', exist_ok=True)
        if os.path.isfile('./data/setting.pkl'):
            with open('./data/setting.pkl', 'rb') as f:
                self.__settings = pickle.load(f)
        else:
            self.__settings = {}

    def save(self):
        with open('./data/setting.pkl', 'wb') as f:
            pickle.dump(self.__settings, f)

    def __getitem__(self, key):
        return self.__settings.get(key, '')

    def __setitem__(self, key, value):
        self.__settings[key] = value

    def __bool__(self):
        # validation
        return set(self.__settings) >= {'endpoint', 'api_key'}