import json
import os


class RecipeManager:
    def __init__(self):
        self.recipes = self._load_recipes()
        self.current_recipe_index = 0
        self.current_step_index = 0

    def _load_recipes(self):
        recipes = []
        try:
            recipe_files = os.listdir("assets/recipes")
            for file in recipe_files:
                if file.endswith(".json"):
                    with open(f"assets/recipes/{file}", "r") as f:
                        recipes.append(json.load(f))
        except Exception as e:
            print(f"Error loading recipes: {e}")
            recipes = [
                {
                    "name": "Sample Recipe",
                    "ingredients": ["Ingredient 1", "Ingredient 2"],
                    "steps": ["Step 1", "Step 2"],
                }
            ]
        return recipes

    def get_current_recipe(self):
        return self.recipes[self.current_recipe_index]

    def next_step(self):
        current_recipe = self.get_current_recipe()
        if self.current_step_index < len(current_recipe["steps"]) - 1:
            self.current_step_index += 1

    def previous_step(self):
        if self.current_step_index > 0:
            self.current_step_index -= 1

    def get_current_step(self):
        return self.get_current_recipe()["steps"][self.current_step_index]
