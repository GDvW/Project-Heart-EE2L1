# EE2L1 Heart project

- Please put your documentation and notes in the /docs/module x/ folder.
- Please leave the lib/ dir empty
- Please put all your code in /src/module x/
- **Please do not commit to main**!

## Coding guidelines

- Use snakecase for variables (e.g. snake_case_var) and camelcase for classes and functions (e.g. camelCaseVar)
- Generate docstrings for every function in the following format:
```
def example(number, kwarg=3):
    """_summary_

    Args:
        number (_type_): _description_
        kwarg (int, optional): _description_. Defaults to 3.

    Raises:
        TypeError: _description_

    Returns:
        _type_: _description_
    """    
    if number < 2:
        raise TypeError

    return kwarg
```