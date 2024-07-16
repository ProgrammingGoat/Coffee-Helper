import json, os
import toga

class JsonReader():
    def __init__(self, app: toga.App):
        self.app = app

    def read_steps(self) -> list[dict]:
        output = []

        # read all instruction files
        try:
            for file in os.scandir(self.app.paths.app / "resources/instructions"):
                with open(self.app.paths.app / "resources/instructions" / file) as f:
                    output.append(json.load(f))
        except Exception as e:
            print("Error getting files.", e, type(e))
            return None
        
        # verify if instruction files are valid and only return the valid ones
        return [instructions for instructions in output if self.verify_valid_instructions(instructions)]

    def verify_valid_instructions(self, instruction: dict) -> bool:
        if not "name" in instruction:
            return False
        
        if not "steps" in instruction or type(instruction["steps"]) != list:
            return False
        
        for step in instruction["steps"]:
            if not "text" in step:
                return False
            if "timer" in step and not type(step["timer"] == int):
                return False
        
        return True