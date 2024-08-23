"""
A tool to help you prepare delicious coffee.
"""

import toga
from toga.style import Pack
from toga.style.pack import ROW

from .main_container import MainContainer
from .settings_window import SettingsWindow
from .util.settings import settings


class CoffeeHelper(toga.App):
    def startup(self):
        """Construct and show the Toga application."""

        main_box = toga.Box(style=Pack(direction=ROW, alignment="center", flex=1))

        settings.load_config(self)
        main_container = MainContainer(app=self)
        main_box.add(main_container)

        settings_window_cmd = toga.Command(
            self.open_settings_window, text="Settings", group=toga.Group.FILE
        )

        self.commands.add(settings_window_cmd)

        self.main_window = toga.MainWindow(
            title=self.formal_name, size=(300, 480), resizable=False
        )
        self.main_window.content = main_box
        self.main_window.show()

    def open_settings_window(self, command=None):
        """Creates and opens the settings window."""
        settings_window = SettingsWindow()
        settings_window.show()


def main():
    return CoffeeHelper()
