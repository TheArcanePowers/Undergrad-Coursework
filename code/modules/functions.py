"""This module stores all the encryption and decryption functions used by main.py for Part 1.

#!EXTRA# Counts towards Part 5 Because this a Caesar cipher module containing encryption and decryption methods.

FUNCTIONS:
encrypt(message, rotation),
decrypt(message, rotation)

"""


# PART 1.4
def encrypt(message, rotation):
    """Return ceaser-cipher encrypted message using given rotation.

    Args:
        message (str): String to encrypt.
        rotation (int): Rotation to use when applying Caesar Cipher.

    Raises:
        ValueError: Rotation given as non-interger.

    Returns:
        encrypted_message: initial string encrypted via Caesar Cipher with given rotation.
    """
    encrypted_message = ""
    for char in message:
        # Determine if char is upper or lower case
        letter = False  # set default for it not to be a letter. Could also be else: letter = False but it doesn't rly matter
        if 65 <= ord(char) <= 90:
            upper = True
            letter = True
        elif 97 <= ord(char) <= 122:
            upper = False
            letter = True

        if letter is True:
            # Normalize rotation (REF:https://stackoverflow.com/questions/6685057/modular-addition-in-python)
            if rotation < 0:
                rotation = (26 - abs(rotation)) % 26
                print(rotation)
            # Add rotation to old character
            try:
                new = ord(char) + rotation
            except TypeError:
                raise ValueError("Rotation suppied must be an integer!")  # This is superfluous due to part 1.2 & part 1.3, but since functions can be imported and called it's important to have error catching in them

            # While loop to account for rotation being more than 26, requiring to be adjusted multiple times
            while (upper is True and new > 90) or (upper is False and new > 122):
                new -= 26

            # Append char to new_message
            encrypted_message += chr(new)
        else:
            encrypted_message += char
    return encrypted_message


def decrypt(message, rotation):
    """Return ceaser-cipher decrypted message using given rotation.

    Args:
        message (str): String to decrypt.
        rotation (int): Rotation to use when applying Caesar Cipher.

    Raises:
        ValueError: Rotation given as non-interger.

    Returns:
        decrypted_message: initial string decrypted via Caesar Cipher with given rotation.
    """
    decrypted_message = ""
    for char in message:
        # Determine if char is a letter, and if upper or lower case
        letter = False
        if 65 <= ord(char) <= 90:
            upper, letter = True, True
        elif 97 <= ord(char) <= 122:
            upper, letter = False, True

        if letter is True:
            # Normalize rotation (REF:https://stackoverflow.com/questions/6685057/modular-addition-in-python)
            if rotation < 0:
                rotation = (26 - abs(rotation)) % 26
                print(rotation)
            # Add rotation to old character
            try:
                new = ord(char) - rotation
            except TypeError:
                raise ValueError("Rotation suppied must be an integer!")  # This is superfluous due to part 1.2 & part 1.3, but since functions can be imported and called it's important to have error catching in them

            # While loop to account for rotation being more than 26, requiring to be adjusted multiple times
            while (upper is True and new < 65) or (upper is False and new < 97):
                new += 26

            # Append char to new_message
            decrypted_message += chr(new)
        else:
            decrypted_message += char  # no change if not a letter
    return decrypted_message
