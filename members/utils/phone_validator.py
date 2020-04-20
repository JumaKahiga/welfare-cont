import re


def validate_phone_number(phone_number):
    """
    Checks if user inputted phone number matches the 
    following pattern 07********

    Parameters
    ----------
    phone_number : str
        User input for phone number

    Returns
    -------
    bool
        True if number matches pattern
        False if number does not match pattern

    Examples
    --------
    >>> validate_phone_number(0700123456)
    True

    >>> validate_phone_number(700123456)
    False

    >>> validate_phone_number(07111234567)
    False
    """

    check = re.fullmatch(r"^07\d{8}", phone_number)

    if check:
        return True
    else:
        return False
