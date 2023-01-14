"""
Result
---

A modal wrapper for a "result" will break if unwrapping an error
"""


from types import LambdaType
from typing import Type


class Result:
    """
    Result modal
    ---

    A modal wrapper for a "result" will break if unwrapping an error
    """

    value = ""
    type = None

    def __repr__(self) -> str:
        """
        Returns the string representation of the modal
        """
        return f"Result<{self.value}>"

    def __str__(self) -> str:
        """
        Returns the string representation of the modal
        """
        return self.__repr__()

    def match(self, ok: LambdaType, error: LambdaType):
        """
        Matches the modal
        ---

        Matches the modal and returns the result of the function that was passed in.
        """
        if type(self) == OK:
            return ok(self.value)
        else:
            return error(self.value)


class OK(Result):
    """
    Ok modal
    ---

    Allows the system to know if the operation was successfull or not.

    ## Modal

    A modal is a multi functional wrapper for a value. In this case the modal is used to wrap the result of an operation.

    ### Ok

    The operation was successfull. The value is stored in the modal.
    """

    def __init__(self, value) -> None:
        self.value = value
        self.type = type(value)

    def __repr__(self) -> str:
        return f"Ok({self.value})"

    def __str__(self) -> str:
        return self.__repr__()


class ErrorType:
    """
    Each error class should derive the error type
    """

    def __str__(self) -> str:
        return ""


class ERROR(Result):
    """
    Error
    ---

    Error modal, wraps the [`ErrorType`] class.
    """

    def __init__(self, value) -> None:
        self.value = value
        self.type = type(value)

    def __repr__(self) -> str:
        return f"Error({self.value})"

    def __str__(self) -> str:
        return self.__repr__()


def Ok(value) -> OK:
    """
    Wraps the value in ok modal
    ---

    Allows the system to know if returned value is ok or error
    """
    return OK(value)


def Error(value: ErrorType) -> ERROR:
    """
    Wraps the value in error modal
    ---

    Allows the system to know if returned value is ok or error
    """
    return ERROR(value)


def unwrap(value: Result):
    """
    unwrap
    ---

    Returns the modals contained value.

    ## Error
    When unwrapping an error the program will crash
    """
    try:
        assert type(value) != ERROR
    except AssertionError:
        raise (f"Unwrapping error : {value}")
    return value.value


def is_error(value: Result) -> bool:
    """
    Checks if a value is wrapped in error
    ---
    """
    return type(value) == ERROR


def is_ok(value: Result) -> bool:
    """
    Checks if a value is ok
    ---

    If the value is wrapped in OK, return true else false
    """
    return type(value) == OK


def to_error(name: str, explination: str) -> Type:
    """
    to_error
    ---

    Creates a new class that derives the ErrorType class
    """
    # This is a "fulhack" to create a new class that derives the ErrorType class
    return type(
        # The name of the class
        name,
        # The classes that the new class derives
        (ErrorType,),
        {
            # Functions
            "__repr__": lambda self: f"{name}, {explination}",
            "__str__": lambda self: self.__repr__(),
            # Fields
            "name": name,
        },
    )
