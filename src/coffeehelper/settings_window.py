import toga
from toga.style import Pack
from toga.style.pack import COLUMN

from .util.settings import settings


class SettingsWindow(toga.Window):
    """A window to edit the settings."""

    def __init__(self):
        super().__init__(size=(210, 100), title="Settings")
        self.content = toga.Box(style=Pack(direction=COLUMN, padding=20))
        self.setup()

    def setup(self):
        """Creates the user interface."""
        has_grinder = settings.get_coffee_grinder()
        self.grinder_checkbox = toga.Switch(
            "Has grinder", value=bool(has_grinder), style=Pack(padding=(5, 0))
        )  # if None = unset, convert to False for unchecked box
        save_button = toga.Button("Save settings", on_press=self.save_settings)
        self.content.add(self.grinder_checkbox, save_button)

    def save_settings(self, widget=None):
        """Reads out the settings and saves them into the config file."""
        has_grinder = self.grinder_checkbox.value
        settings.set_coffee_grinder(has_grinder)
        self.close()
