from .util import constants

class Recipe():
    """Class representing the currently selected recipe.
    Do not manually instantiate this, simply import the instance from this module."""

    def load_recipe(self, instructions):
        """Receives a dictionary representation of a given recipe
        and uses it to initialize/update all attributes."""

        self.name = instructions.get("name")
        self.image_folder = instructions.get("image_folder")
        self.grind = instructions.get("grind")
        ratio = instructions.get("ratio")
        self.water = constants.DEFAULT_WATER
        self.coffee = constants.DEFAULT_COFFEE
        if ratio:
            self.water = ratio.get("water", constants.DEFAULT_WATER)
            self.coffee = ratio.get("coffee", constants.DEFAULT_COFFEE)
        self.ratio = self.coffee/self.water
        self.steps = instructions.get("steps")
        self.current_step = 0

    def next_step(self):
        self.current_step += 1

    def previous_step(self):
        self.current_step -= 1

    def get_current_step(self):
        """Returns the contents of the current step.
        Returns None when the final step is reached."""

        if self.current_step < len(self.steps):
            return self.steps[self.current_step]
        else:
            return None


# singleton instance
recipe = Recipe()