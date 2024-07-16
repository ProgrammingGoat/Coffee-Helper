from .util import constants

class Recipe():

    def __init__(self):
        self.current_step = None

    def load_recipe(self, instructions):
        self.name = instructions.get("name")
        self.grind = instructions.get("grind")
        ratio = instructions.get("ratio")
        self.water = constants.DEFAULT_WATER
        self.coffee = constants.DEFAULT_COFFEE
        if ratio:
            self.water = ratio.get("water", constants.DEFAULT_WATER)
            self.coffee = ratio.get("coffee", constants.DEFAULT_COFFEE)
        self.ratio = self.coffee/self.water
        self.steps = instructions.get("steps")

    def next_step(self):
        self.current_step = next(self.steps, None)



# singleton instance
recipe = Recipe()