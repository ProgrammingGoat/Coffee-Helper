import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW

from .coffee_selection_screen import CoffeeSelectionScreen
from .ratio_selection_screen import RatioSelectionScreen
from .util.json_reader import JsonReader

class MainContainer(toga.Box):
    def __init__(self, app):
        super().__init__(style=Pack(direction=COLUMN, padding=10, flex=1))
        self.app = app

        json_reader = JsonReader(self.app)
        self.instructions = json_reader.read_steps()

        self.setup()
        self.load_selection_screen()

    def setup(self):
        self.main_box = toga.Box(style=Pack(flex=1))
        self.controls = toga.Box(style=Pack(direction=ROW, height=40, flex=1))

        self.add(self.main_box, self.controls)
        self.load_start_button()

    def load_start_button(self):
        self.controls.clear()
        start_button = toga.Button("Start brewing!", style=Pack(flex=1))
        self.controls.add(start_button)

    def load_control_arrows(self):
        self.controls.clear()
        backward_button = toga.Button("<-", on_press=self.backward_handler)
        spacer = toga.Box(style=Pack(flex=1))
        forward_button = toga.Button("->", on_press=self.forward_handler)
        self.controls.add(backward_button, spacer, forward_button)

    def load_selection_screen(self):
        self.coffee_selection_screen = CoffeeSelectionScreen(self.instructions)
        self.main_box.add(self.coffee_selection_screen)

    def forward_handler(self, widget=None):
        print("Forward pressed.")

    def backward_handler(self, widget=None):
        print("Backward pressed.")

    def start_button_handler(self, widget=None):
        selected = self.coffee_selection_screen.selection.value
        self.main_box.clear()
        ratio_selection_screen = RatioSelectionScreen()