import random
from ingredientType import IngredientType

class Dish:
    def __init__(self, dishId: int, ingredients):
        self.dishId = dishId
        self.calorie = Dish.getRandomCalories()
        self.ingredients = ingredients
        
    def __str__(self) -> str:
        return f"Dish {self.dishId}:\nIngrdients: {self.ingredients[0]}, {self.ingredients[1]}\nCalories: {self.calorie}\n\n"
   
    def getDish(self):
        return f"Dish {self.dishId}:\nIngrdients: {self.ingredients[0]}, {self.ingredients[1]}\nCalories: {self.calorie}\n\n"
    
    @staticmethod
    def getRandomCalories():
        upper_limit = 1000
        lower_limit = 1
        range_of_numbers = range(lower_limit, upper_limit)
        number = random.choice(range_of_numbers)
        return number
    
    @staticmethod
    def createDish(dishId: int, ingredientTypeOne: IngredientType, ingredientTypeTwo: IngredientType):
        dish = Dish(
            dishId, 
            [Dish.createIngredients(ingredientTypeOne), Dish.createIngredients(ingredientTypeTwo)]
        )
        return dish


    @staticmethod   
    def createIngredients(ingredientType: IngredientType):
        if ingredientType == IngredientType.Meat:
            meat = ["Beef", "Goose", "Duck", "Chicken"]
            return random.choice(meat) 
        elif ingredientType == IngredientType.Fish:
            fish = ["Salmon", "Tuna", "Sardines", "Sea Bass", "Mackerel", "Halibut", "Pollack"]
            return random.choice(fish)
        elif ingredientType == IngredientType.Nuts:
            nuts = ["Walnuts", "Peanuts", "Almonds", "Cashews", "Coconut", "Hazelnut"] 
            return random.choice(nuts)
        elif ingredientType == IngredientType.Milkproducts:
            milkproducts = ["Milk", "Cream", "Quark", "Cheese", "Butter", "Yoghurt"]
            return random.choice(milkproducts)
        elif ingredientType == IngredientType.Gluten:
            gluten = ["Pasta", "Pizza", "Bread", "Baguette", "Gnocchi", "Couscous", "Beer", "Rice"]
            return random.choice(gluten)
        elif ingredientType == IngredientType.Fruits:
            fruits = ["Apple", "Tomato", "Pineapple", "Juice", "Papaya", "Lemon", "Mango"]
            return random.choice(fruits)
        elif ingredientType == IngredientType.Vegetable:
            vegetable = ["Broccoli", "Aubergine", "Zucchini", "Potatoes", "Pepper", "Spinach"]
            return random.choice(vegetable)
        else:
            raise ValueError("Invalid direction "+ str(ingredientType))
            
