import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW

class SelectionScreen(toga.Box):
    def __init__(self):
        super().__init__(style=Pack(direction=COLUMN))
        self.setup()

    def setup(self):
        label = toga.Label("Which method would you like to use?")
        selection = toga.Selection(items=["Aeropress", "French Press"])
        self.add(label)
        self.add(selection)