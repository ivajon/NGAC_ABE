"""
    NGAC policy abstraction class

    This class is used to implement policies
"""

from ngac_object import NgacObject


class Policy(NgacObject):
    def __init__(self, pol:str):
        self.pol = pol 

        super.__init__("Policy")
    
    def get_pol(self) -> str:
        return self.pol
