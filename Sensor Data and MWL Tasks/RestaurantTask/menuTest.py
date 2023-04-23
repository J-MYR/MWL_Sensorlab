from dish import Dish
from ingredientType import IngredientType
import random
from task import Task

class MenuTest(Dish):
    
    # question = "No nuts"
    # correctDish = ""
    # dishes = []

    def __init__(self, question, correctDish, dishes):
        self.question = question
        self.correctDish = correctDish
        self.dishes = dishes
    
    @classmethod
    def getTasks(self, task: Task):
        if task == Task.One:
            dishOne = Dish.createDish(
                dishId= 1,
                ingredientTypeOne= IngredientType.Fish,
                ingredientTypeTwo= IngredientType.Vegetable
            )
            dishTwo =  Dish.createDish(
                dishId= 2,
                ingredientTypeOne= IngredientType.Nuts,
                ingredientTypeTwo= IngredientType.Milkproducts
            )
            menuTest = MenuTest(
                question= "is allergic to fish.\n\n",
                correctDish= dishTwo,
                dishes= [dishOne, dishTwo]
            )
            return menuTest
        
        elif task == Task.Two:
            dishOne = Dish.createDish(
                dishId= 1,
                ingredientTypeOne= IngredientType.Meat,
                ingredientTypeTwo= IngredientType.Gluten
            )
            dishTwo =  Dish.createDish(
                dishId= 2,
                ingredientTypeOne= IngredientType.Nuts,
                ingredientTypeTwo= IngredientType.Vegetable
            )
            menuTest = MenuTest(
                question= "does NOT want animal ingredients.\n\n",
                correctDish= dishTwo,
                dishes= [dishOne, dishTwo]
            )
            return menuTest
        
        elif task == Task.Three:
            dishOne = Dish.createDish(
                dishId= 1,
                ingredientTypeOne= IngredientType.Fish,
                ingredientTypeTwo= IngredientType.Milkproducts
            )
            dishTwo =  Dish.createDish(
                dishId= 2,
                ingredientTypeOne= IngredientType.Fruits,
                ingredientTypeTwo= IngredientType.Nuts
            )
            if dishOne.calorie < dishTwo.calorie:
                correctDish = dishOne
            else:
                correctDish = dishTwo
            menuTest = MenuTest(
                question= "is on a diet.\n\n",
                correctDish= correctDish,
                dishes= [dishOne,dishTwo]
            )
            return menuTest
        
        elif task == Task.Four:
            dishOne = Dish.createDish(
                dishId= 1,
                ingredientTypeOne= IngredientType.Fish,
                ingredientTypeTwo= IngredientType.Vegetable
            )
            dishTwo =  Dish.createDish(
                dishId= 2,
                ingredientTypeOne= IngredientType.Nuts,
                ingredientTypeTwo= IngredientType.Milkproducts
            )
            dishThree = Dish.createDish(
                dishId= 3,
                ingredientTypeOne= IngredientType.Gluten,
                ingredientTypeTwo= IngredientType.Meat
            )
            menuTest = MenuTest(
                question= "wants vegetables.\n\n",
                correctDish= dishTwo,
                dishes= [dishOne, dishTwo, dishThree]
            )
            return menuTest
        
        elif task == Task.Five:
            dishOne = Dish.createDish(
                dishId= 1,
                ingredientTypeOne= IngredientType.Meat,
                ingredientTypeTwo= IngredientType.Nuts
            )
            dishTwo =  Dish.createDish(
                dishId= 2,
                ingredientTypeOne= IngredientType.Milkproducts,
                ingredientTypeTwo= IngredientType.Meat
            )
            dishThree = Dish.createDish(
                dishId= 3,
                ingredientTypeOne= IngredientType.Vegetable,
                ingredientTypeTwo= IngredientType.Gluten
            )
            if dishOne.calorie < dishTwo.calorie:
                correctDish = dishOne
            else:
                correctDish = dishTwo
            menuTest = MenuTest(
                question= "wants meat\nand\nfewest calories.\n\n",
                correctDish= correctDish,
                dishes= [dishOne, dishTwo, dishThree]
            )
            return menuTest
        
        elif task == Task.Six:
            dishOne = Dish.createDish(
                dishId= 1,
                ingredientTypeOne= IngredientType.Fish,
                ingredientTypeTwo= IngredientType.Milkproducts
            )
            dishTwo =  Dish.createDish(
                dishId= 2,
                ingredientTypeOne= IngredientType.Nuts,
                ingredientTypeTwo= IngredientType.Meat
            )
            dishThree = Dish.createDish(
                dishId= 3,
                ingredientTypeOne= IngredientType.Nuts,
                ingredientTypeTwo= IngredientType.Fruits
            )
            if dishTwo.calorie < dishThree.calorie:
                correctDish = dishThree
            else:
                correctDish = dishTwo
            menuTest = MenuTest(
                question= "is lactoseINTOLERANT\nbut\nwants highest calories.\n\n",
                correctDish= correctDish,
                dishes= [dishOne, dishTwo, dishThree]
            )
            return menuTest
        
        elif task == Task.Seven:
            dishOne = Dish.createDish(
                dishId= 1,
                ingredientTypeOne= IngredientType.Meat,
                ingredientTypeTwo= IngredientType.Gluten
            )
            dishTwo =  Dish.createDish(
                dishId= 2,
                ingredientTypeOne= IngredientType.Fish,
                ingredientTypeTwo= IngredientType.Milkproducts
            )
            dishThree = Dish.createDish(
                dishId= 3,
                ingredientTypeOne= IngredientType.Vegetable,
                ingredientTypeTwo= IngredientType.Meat
            )
            dishFour = Dish.createDish(
                dishId= 4,
                ingredientTypeOne= IngredientType.Vegetable,
                ingredientTypeTwo= IngredientType.Fruits
            )
            menuTest = MenuTest(
                question= "wants meat\nand\nvegetables.\n\n",
                correctDish= dishTwo,
                dishes= [dishOne, dishTwo, dishThree, dishFour]
            )
            return menuTest
        
        elif task == Task.Eight:
            dishOne = Dish.createDish(
                dishId= 1,
                ingredientTypeOne= IngredientType.Meat,
                ingredientTypeTwo= IngredientType.Nuts
            )
            dishTwo =  Dish.createDish(
                dishId= 2,
                ingredientTypeOne= IngredientType.Milkproducts,
                ingredientTypeTwo= IngredientType.Meat
            )
            dishThree = Dish.createDish(
                dishId= 3,
                ingredientTypeOne= IngredientType.Vegetable,
                ingredientTypeTwo= IngredientType.Gluten
            )
            dishFour = Dish.createDish(
                dishId= 4,
                ingredientTypeOne= IngredientType.Nuts,
                ingredientTypeTwo= IngredientType.Milkproducts
            )
            menuTest = MenuTest(
                question= "wants nuts\nbut\nNO meat.\n\n",
                correctDish= dishTwo,
                dishes= [dishOne, dishTwo, dishThree, dishFour]
            )
            return menuTest
        
        elif task == Task.Nine:
            dishOne = Dish.createDish(
                dishId= 1,
                ingredientTypeOne= IngredientType.Fish,
                ingredientTypeTwo= IngredientType.Nuts
            )
            dishTwo =  Dish.createDish(
                dishId= 2,
                ingredientTypeOne= IngredientType.Meat,
                ingredientTypeTwo= IngredientType.Meat
            )
            dishThree = Dish.createDish(
                dishId= 3,
                ingredientTypeOne= IngredientType.Fruits,
                ingredientTypeTwo= IngredientType.Gluten
            )
            dishFour = Dish.createDish(
                dishId= 4,
                ingredientTypeOne= IngredientType.Vegetable,
                ingredientTypeTwo= IngredientType.Milkproducts
            )
            if dishOne.calorie < dishTwo.calorie and dishOne.calorie < dishThree.calorie and dishOne.calorie < dishFour.calorie:
                correctDish = dishOne
            elif dishTwo.calorie < dishOne.calorie and dishTwo.calorie < dishThree.calorie and dishTwo.calorie < dishFour.calorie:
                correctDish = dishTwo
            elif dishThree.calorie < dishOne.calorie and dishThree.calorie < dishTwo.calorie and dishThree.calorie < dishFour.calorie:
                correctDish = dishThree
            else:
                correctDish = dishFour
            menuTest = MenuTest(
                question= "wants fewest calories.\n\n",
                correctDish= correctDish,
                dishes= [dishOne, dishTwo, dishThree, dishFour]
            )
            return menuTest
        
        elif task == Task.Ten:
            dishOne = Dish.createDish(
                dishId= 1,
                ingredientTypeOne= IngredientType.Milkproducts,
                ingredientTypeTwo= IngredientType.Nuts
            )
            dishTwo =  Dish.createDish(
                dishId= 2,
                ingredientTypeOne= IngredientType.Milkproducts,
                ingredientTypeTwo= IngredientType.Meat
            )
            dishThree = Dish.createDish(
                dishId= 3,
                ingredientTypeOne= IngredientType.Vegetable,
                ingredientTypeTwo= IngredientType.Gluten
            )
            dishFour = Dish.createDish(
                dishId= 4,
                ingredientTypeOne= IngredientType.Vegetable,
                ingredientTypeTwo= IngredientType.Milkproducts
            )
            dishFive = Dish.createDish(
                dishId= 5,
                ingredientTypeOne= IngredientType.Fish,
                ingredientTypeTwo= IngredientType.Meat
            )
            menuTest = MenuTest(
                question= "wants milkproducts\nand\nmeat.\n\n",
                correctDish= dishTwo,
                dishes= [dishOne, dishTwo, dishThree, dishFour, dishFive]
            )
            return menuTest
        
        else:
            return "It does not work."