class Settings():
    """Class representing the settings of the application.
    Do not instantiate this, simply import the instance from this module."""
    
    def __init__(self):
        # load settings file or load defaults and maybe create settings file here
        self.has_grinder = False


# Singleton Instance
settings = Settings()