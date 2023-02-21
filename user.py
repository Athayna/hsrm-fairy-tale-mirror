class User:
    """User class containing all user information set in the PeronalizeLoop"""
    def __init__(self, name:str, age:int, color:str) -> None:
        self.name = name
        self.age = age
        self.color = color