import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
from toga.validators import Number

from .util import constants

class RatioSelectionScreen(toga.Box):
    def __init__(self, coffee, water):
        super().__init__(style=Pack(direction=COLUMN))
        self.coffee = coffee if coffee else constants.DEFAULT_COFFEE
        self.water = water if water else constants.DEFAULT_WATER

        self.ratio = coffee/water
        self.changing = False   # helper variable to avoid looping field updates

        self.setup()

    def setup(self):
        row1 = toga.Box(style=Pack(direction=ROW))
        coffee_label = toga.Label("Coffee")
        self.coffee_input = toga.TextInput(
            value=self.coffee, 
            on_change=self.on_coffee_change_handler,
            validators=Number)
        water_label = toga.Label("Water")
        self.water_input = toga.TextInput(
            value=self.water, 
            on_change=self.on_water_change_handler,
            validators=Number)
        row1.add(coffee_label, self.coffee_input, water_label, self.water_input)
        self.add(row1)

    # On change handlers + Utility functions

    def calculate_coffee_from_water(self, water):
        return water * self.ratio
    
    def calculate_water_from_coffee(self, coffee):
        return coffee / self.ratio
    
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