import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
from toga.validators import Number

from ..recipe import recipe

class RatioSelectionScreen(toga.Box):
    def __init__(self):
        super().__init__(style=Pack(direction=COLUMN))
        self.changing = False   # helper variable to avoid looping field updates

        self.setup()

    def setup(self):        
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