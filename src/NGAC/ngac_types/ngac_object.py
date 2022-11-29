"""
    NGAC Object class

    This is a super class which the other types will inherit from. 
"""


class NgacObject:
    def __init__(self, type: str):
        self.type = type

    def get_type(self):
        return self.type
