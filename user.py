class User:
    """User class containing all user information set in the PeronalizeLoop"""
    def __init__(self, name:str, age:int, school:bool, color:str, alarm:str, wordGame:int, numberGame:int, multGame:int, clockGame:int) -> None:
        self.name = name
        self.age = age
        self.school = school
        self.color = color
        self.alarm = alarm
        self.wordGame = wordGame
        self.numberGame = numberGame
        self.multGame = multGame
        self.clockGame = clockGame