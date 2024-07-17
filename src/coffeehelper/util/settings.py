import configparser

import toga

class Settings():
    """Class representing the settings of the application.
    Do not manually instantiate this, simply import the instance from this module."""

    def __init__(self):
        """Initializes the config file. """
        # load settings file or load defaults and maybe create settings file here
        self.app = None
        self.config = configparser.ConfigParser()

    def load_config(self, app: toga.App):
        """Loads the current settings file.
        Requires the app parameter to know where to look for it."""
        
        self.app = app

        try:
            with open(self.app.paths.config / "config.ini", "r") as f:
                self.config.read(self.app.paths.config / "config.ini")
        except FileNotFoundError:
            print("File not found.")

    def write_config(self) -> bool:
        """Writes the current state of the config into the settings file.
        Returns True if the operation is successful, otherwise False"""

        try:
            self.app.paths.config.mkdir(parents=True, exist_ok=True) # create path if it doesn't exist
            with open(self.app.paths.config / "config.ini", "w") as f:
                self.config.write(f)
            return True
        except OSError as e:
            print("Error writing file. Error:", e)
            return False

    def get_coffee_grinder(self) -> bool | None:
        """Parses the config file to determine if the user owns a coffee grinder.
        Returns the value of the key if it exists, or None if it is unset."""

        if self.config.has_section("Hardware"):
            return self.config["Hardware"].getboolean("CoffeeGrinder", None)
        else:
            return None

    def set_coffee_grinder(self, value: bool):
        """Updates the config file and sets wether the user has a coffee grinder or not."""

        if not self.config.has_section("Hardware"):
            self.config["Hardware"] = {}
        self.config["Hardware"]["CoffeeGrinder"] = str(value)
        self.write_config()


# Singleton Instance
settings = Settings()