class Settings():
    def __init__(self):
        # load settings file or load defaults and maybe create settings file here
        self.has_grinder = False


# Singleton Instance
settings = Settings()