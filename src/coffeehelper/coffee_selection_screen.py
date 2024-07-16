import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW

class CoffeeSelectionScreen(toga.Box):
    def __init__(self, instructions):
        super().__init__(style=Pack(direction=COLUMN, alignment="center", flex=1))
        self.instructions = instructions
        self.setup()

    def setup(self):
        label = toga.Label("Which method would you like to use?")
        tems = self.get_items()
        self.selection = toga.Selection(items=self.instructions, accessor="name")
        self.add(label, self.selection)

    def get_items(self):
        output = []
        if self.instructions:
            for instruction in self.instructions:
                # double checking that a name exists to avoid key error
                name = instruction.get("name")
                if name:
                    output.append(name)
        return output