import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW

from .recipe import recipe
from .screens import (
    CoffeePreparationScreen,
    CoffeeSelectionScreen,
    FinishScreen,
    InstructionDisplayScreen,
    RatioSelectionScreen,
)
from .util.constants import (
    COFFEE_PREPARATION,
    COFFEE_SELECTION,
    FINISHED,
    INSTRUCTIONS,
    RATIO_SELECTION,
)
from .util.json_reader import JsonReader


class MainContainer(toga.Box):
    """The main container which will display most of the user interface.
    Handles managing the various screens and switching between them."""

    def __init__(self, app):
        super().__init__(style=Pack(direction=COLUMN, padding=10, flex=1))
        self.app = app

        self.current_step = 0

        json_reader = JsonReader(self.app)
        self.instructions = json_reader.read_steps()

        self.setup()

    def setup(self):
        """Generates the overall layout and loads the initial screen."""
        self.main_box = toga.Box(style=Pack(flex=1))
        self.controls = toga.Box(style=Pack(direction=ROW, height=40, flex=1))

        self.add(self.main_box, self.controls)
        self.load_selection_screen()

    # Element Loading Methods

    def load_control_arrows(self):
        """Loads in the buttons that allow moving forward and backward through the instructions."""

        self.controls.clear()
        backward_button = toga.Button("<-", on_press=self.backward_handler)
        spacer = toga.Box(
            style=Pack(flex=1)
        )  # ensures that the buttons "stick" to the left and right by filling any remaining space.
        forward_button = toga.Button("Continue ->", on_press=self.forward_handler)
        self.controls.add(backward_button, spacer, forward_button)

    def load_selection_screen(self):
        """Loads the screen in which the user selects their coffee of choice from the options available."""

        self.current_step = COFFEE_SELECTION
        self.main_box.clear()
        self.coffee_selection_screen = CoffeeSelectionScreen(self.instructions)
        self.main_box.add(self.coffee_selection_screen)
        self.controls.clear()
        start_button = toga.Button(
            "Start brewing!", style=Pack(flex=1), on_press=self.start_button_handler
        )
        self.controls.add(start_button)

    def load_ratio_screen(self):
        """Loads the screen in which the user chooses how much water/coffee to brew."""

        self.current_step = RATIO_SELECTION
        selected = self.coffee_selection_screen.selection.value
        instruction = None
        for i in self.instructions:
            if i["name"] == selected.name:
                instruction = i
                break

        recipe.load_recipe(instruction)

        ratio_selection_screen = RatioSelectionScreen()
        self.main_box.clear()
        self.main_box.add(ratio_selection_screen)

        self.load_control_arrows()

    def load_coffee_preparation_screen(self):
        """Loads the screen which tells the user to weigh and grind their coffee."""

        self.current_step = COFFEE_PREPARATION
        self.main_box.clear()
        coffee_preparation_screen = CoffeePreparationScreen()
        self.main_box.add(coffee_preparation_screen)

    def load_instruction_display_screen(self):
        """Loads the screen that will guide the user through step-by-step instructions."""

        self.current_step = INSTRUCTIONS
        self.main_box.clear()
        self.instruction_display_screen = InstructionDisplayScreen(self.app)
        self.main_box.add(self.instruction_display_screen)

    def load_finish_screen(self):
        """Loads the screen that congratulates the user to their cup of coffee."""
        self.current_step = FINISHED
        self.main_box.clear()
        finish_screen = FinishScreen()
        self.main_box.add(finish_screen)

        restart_button = toga.Button(
            "Brew more coffee!",
            style=Pack(flex=1),
            on_press=self.restart_button_handler,
        )
        self.controls.clear()
        self.controls.add(restart_button)

    # Event Handlers

    def forward_handler(self, widget=None):
        """Handles presses of the forward button.
        Determines the current step and performs the appropriate action."""

        if self.current_step == RATIO_SELECTION:
            self.load_coffee_preparation_screen()
        elif self.current_step == COFFEE_PREPARATION:
            self.load_instruction_display_screen()
        elif self.current_step == INSTRUCTIONS:
            result = self.instruction_display_screen.next_step()
            if result == "finished":
                self.current_step == FINISHED
                self.load_finish_screen()
        else:
            print("Forward pressed.")

    def backward_handler(self, widget=None):
        """Handles presses of the backward button.
        Determins the current step and performs the appropriate action."""

        if self.current_step == RATIO_SELECTION:
            self.load_selection_screen()
        elif self.current_step == COFFEE_PREPARATION:
            self.load_ratio_screen()
        elif self.current_step == INSTRUCTIONS and recipe.current_step <= 0:
            self.load_coffee_preparation_screen()
        elif self.current_step == INSTRUCTIONS:
            self.instruction_display_screen.previous_step()
        else:
            print("Backward pressed.")

    def start_button_handler(self, widget=None):
        """Handles presses of the start button."""

        self.load_ratio_screen()

    def restart_button_handler(self, widget=None):
        """Handles presses of the restart button."""

        self.load_selection_screen()
