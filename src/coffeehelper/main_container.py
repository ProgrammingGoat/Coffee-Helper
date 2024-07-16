import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW

from .selection_screen import SelectionScreen

class MainContainer(toga.Box):
    def __init__(self):
        super().__init__(style=Pack(direction=COLUMN, padding=10, flex=1))
        self.setup()
        self.load_selection_screen()

    def setup(self):
        self.main_box = toga.Box(style=Pack(flex=1))
        self.controls = toga.Box(style=Pack(direction=ROW, height=40, flex=1))

        self.add(self.main_box, self.controls)

        back = toga.Button("<-")
        spacer = toga.Box(style=Pack(flex=1))
        forward = toga.Button("->")
        self.controls.add(back, spacer, forward)

    def load_selection_screen(self):
        selection_screen = SelectionScreen()
        self.main_box.add(selection_screen)