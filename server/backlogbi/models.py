import pickle


class Setting:
    """
    Setting model
    """
    endpoint = ""
    api_key = ""

    def __init__(self):
        try:
            with open('setting.pickle', 'rb') as f:
                l = pickle.load(f)
            self.endpoint = l.endpoint
            self.api_key = l.api_key
        except Exception as e:
            print(e)
            pass

    def set_option(self, endpoint: str, api_key: str) -> bool:
        self.endpoint = endpoint
        self.api_key = api_key
        try:
            with open('setting.pickle', 'wb') as f:
                pickle.dump(self, f)
            return True
        except Exception as e:
            print(e)
            return False
