from pathlib import Path

import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
from toga.validators import Number

from .recipe import recipe
from .timer import Timer

class CoffeeSelectionScreen(toga.Box):
    """Class representing the screen in which the users selects the coffee they want to prepare.
    
    Takes a dictionary representation of instructions as an argument."""

    def __init__(self, instructions):
        super().__init__(style=Pack(direction=COLUMN, alignment="center", flex=1))
        self.instructions = instructions
        self.setup()

    def setup(self):
        label = toga.Label("Which method would you like to use?")
        self.selection = toga.Selection(items=self.instructions, accessor="name")
        self.add(label, self.selection)
    

class RatioSelectionScreen(toga.Box):
    """Class representing the screen in which the user chooses how much coffee to prepare."""

    def __init__(self):
        super().__init__(style=Pack(direction=COLUMN))
        self.changing = False   # helper variable to avoid looping field updates

        self.setup()

    def setup(self):
        """Generates the user interface."""

        row1 = toga.Box(style=Pack(direction=ROW, padding=5))
        water_label = toga.Label("Water", style=Pack(width=100))
        self.water_input = toga.TextInput(
            value=recipe.water, 
            on_change=self.on_water_change_handler,
            validators=[Number()])
        ml_label = toga.Label("ml")

        row2 = toga.Box(style=Pack(direction=ROW, padding=5))
        coffee_label = toga.Label("Coffee", style=Pack(width=100))
        self.coffee_input = toga.TextInput(
            value=recipe.coffee, 
            on_change=self.on_coffee_change_handler,
            validators=[Number()])
        gram_label = toga.Label("g")

        
        row1.add(water_label, 
                 self.water_input,
                 ml_label)
        row2.add(coffee_label, 
                 self.coffee_input, 
                 gram_label)
        self.add(row1, row2)

    # On change handlers + Utility functions

    def calculate_coffee_from_water(self, water):
        return water * recipe.ratio
    
    def calculate_water_from_coffee(self, coffee):
        return coffee / recipe.ratio
    
    def on_coffee_change_handler(self, widget):
        if not self.changing:
            try:
                self.changing = True
                coffee = int(widget.value)
                water = int(self.calculate_water_from_coffee(coffee))
                self.water_input.value = water
                self.changing = False
            except ValueError:
                widget.value = "???"
                self.changing = False

    def on_water_change_handler(self, widget):
        if not self.changing:
            try:
                self.changing = True
                water = int(widget.value)
                coffee = round(self.calculate_coffee_from_water(water), 1)
                self.coffee_input.value = coffee
                self.changing = False
            except ValueError:
                widget.value = "???"
                self.changing = False


class CoffeePreparationScreen(toga.Box):
    """Class representing the screen in which the user is told to weigh and grind their coffee."""

    def __init__(self):
        super().__init__(style=Pack(flex=1, direction=COLUMN, padding=(5,0)))
        self.setup()

    def setup(self):
        try:
            image = toga.Image("resources/images/grinder.jpg")
            image_view = toga.ImageView(image, style=Pack(flex=1, padding=(5, 0)))
        except (FileNotFoundError):
            image_view = toga.Box(style=Pack(flex=1, padding=(5, 0))) # empty placeholder
        label = toga.Label(f"If you own a grinder, grind {recipe.coffee} grams of coffee.\n"\
                           "If you don't, weigh your preground coffee.\n"\
                           f"Grind setting: {recipe.grind}", style=Pack(padding=(5, 0)))
        
        self.add(image_view)
        self.add(label)


class InstructionDisplayScreen(toga.Box):
    """Represents the screen in which the user is lead through the step-by-step instructions to make coffee."""

    def __init__(self, app): # app is needed for access to the event loop
        super().__init__(style=Pack(direction=COLUMN, flex=1))
        self.app = app
        self.step: dict = recipe.get_current_step()
        self.setup()

    def setup(self):
        """Creates the containers for the user interface."""

        self.image_box = toga.Box(style=Pack(flex=1, padding=(5, 0)))
        self.text_box = toga.Box(style=Pack(padding=(5, 0)))
        self.timer_box = toga.Box(style=Pack(padding=(5, 0)))
        self.add(self.image_box, self.text_box, self.timer_box)
        self.load_step()

    def load_step(self):
        """Loads the current step into the user interface,
        adding an image and a timer as needed."""

        self.image_box.clear()
        self.text_box.clear()
        self.timer_box.clear()

        image = self.step.get("image")
        text = self.step.get("text")
        timer = self.step.get("timer")

        if image:
            self.load_image(image)
        if text:
            self.load_text(text)
        if timer:
            self.load_timer(timer)

    def load_text(self, text):
        label = toga.Label(text.format(coffee=recipe.coffee, water=recipe.water))
        self.text_box.add(label)

    def load_image(self, image):
        try:
            image_obj = toga.Image(Path("resources/images") / recipe.image_folder / image)
            image_view = toga.ImageView(image_obj, style=Pack(flex=1))
            self.image_box.add(image_view)
        except (FileNotFoundError, ValueError):
            print("Error: Image", image, "not found.")

    def load_timer(self, time):
        self.timer = Timer(self.app, time)
        self.timer_box.add(self.timer)


    def next_step(self):
        recipe.next_step()
        self.step = recipe.get_current_step()
        if self.step:
            self.load_step()
        else:
            return "finished"
        
    def previous_step(self):
        recipe.previous_step()
        self.step = recipe.get_current_step()
        self.load_step()
