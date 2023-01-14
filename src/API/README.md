# API

A set of type-level abstractions for building APIs.

## Included

- `Endpoint`: A type-level abstraction for building APIs.
- `Result`: A modal for representing the result of an API call.

## Endpoint

An `Endpoint` is a type-level abstraction for building APIs. It is a type that helps
you build a type-safe API in python and makes the code more readable.

## Result

A `Result` is a modal for representing the result of an API call. It is heavily inspired by
rust's `Result` type.

Unwrapping a `Result` is done using the `unwrap` method. This method will raise an exception
if the `Result` is an `Error` type.

```python
from api import Result, Error, Ok

def divide(a: int, b: int) -> Result[int, str]:
    if b == 0:
        return Error("Cannot divide by zero")
    return Ok(a / b)

result = unwrap(divide(4, 2))
assert result == 2
```

This makes the usage of the API much cleaner since it removes all error-handling code from
the user app, if the user wants to handle the error they can use the `match` method.

```python
from api import Result, Error, Ok

def divide(a: int, b: int) -> Result[int, str]:
    if b == 0:
        return Error("Cannot divide by zero")
    return Ok(a / b)

result = divide(4, 2)

result.match(
    ok=lambda x: print(f"Result: {x}"),
    error=lambda x: print(f"Error: {x}")
)
```
