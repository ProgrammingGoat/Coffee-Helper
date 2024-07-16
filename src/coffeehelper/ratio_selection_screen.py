import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW

class RatioSelectionScreen(toga.Box):
    def __init__(self, coffee, water):
        super().__init__(style=Pack(direction=COLUMN))
        self.coffee = coffee
        self.water = water

        self.ratio = coffee/water

        self.setup()

    def setup(self):
        row1 = toga.Box(style=Pack(direction=ROW))
        coffee_label = toga.Label("Coffee")
        coffee_input = toga.TextInput(value=self.coffee)
        water_label = toga.Label("Water")
        water_input = toga.TextInput(value=self.water)
        row1.add(coffee_label, coffee_input, water_label, water_input)

    def calculate_coffee_from_water(self, water):
        return water / self.ratio
    
    def calculate_water_from_coffee(self, coffee):
        return coffee * self.ratio