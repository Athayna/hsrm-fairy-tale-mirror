class User:
    """User class containing all user information set in the PeronalizeLoop"""
    def __init__(self, name:str, age:int, color:str, wordGame:int, numberGame:int, multGame:int, clockGame:int) -> None:
        self.name = name
        self.age = age
        self.color = color
        self.wordGame = 0
        self.numberGame = 0
        self.multGame = 0
        self.clockGame = 0