import re


def is_space(character: str) -> bool:
    """Determines if charactter is space.

    Args:
        character (str): input character to check.

    Returns:
        bool: boolean value of if character is space.
    """
    return bool(re.match("^[ \t\n]$", str(character)))


def is_letter(character: str) -> bool:
    """Determines if charactter is letter.

    Args:
        character (str): input character to check.

    Returns:
        bool: boolean value of if character is letter.
    """
    return bool(re.match("^[A-Za-z]$", str(character)))


def is_nonzero(character: str) -> bool:
    """Determines if charactter is non-zero.

    Args:
        character (str): input character to check.

    Returns:
        bool: boolean value of if character is non-zero.
    """
    return bool(re.match("^[1-9]$", str(character)))


def is_digit(character: str) -> bool:
    """Determines if charactter is digit.

    Args:
        character (str): input character to check.

    Returns:
        bool: boolean value of if character is digit.
    """
    return bool(re.match("^[0-9]$", str(character)))


def is_alphanum(character: str) -> bool:
    """Determines if charactter is alphanum.

    Args:
        character (str): input character to check.

    Returns:
        bool: boolean value of if character is _ or a letter.
    """
    return bool(re.match("^[_]$", str(character))) or is_letter(str(character)) or is_digit(str(character))
