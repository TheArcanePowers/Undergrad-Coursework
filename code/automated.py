"""This module just contains the automatic decryptor function.

FUNCTIONS:
auto_decrypt(initial_message)

"""


import functions


def auto_decrypt(initial_message):
    """Iterate over all possible rotations, offering potential decryption to user.

    Args:
        initial_message (str): encrypted message to be decrypted.

    Returns:
        decrypted_message: Returns fully decrypted message if successful, False if unsuccessful.
    """
    # Taken from my work in Part 2
    clean_words = []
    for item in initial_message.split(" ")[:9]:  # Should have just used regex, but not included in the exercises so didn't want to lose out on marks
        clean_word = [char for char in item if char.isalpha()]  # Should check if each char is in the alphabet, and if so add it
        clean_word = "".join(clean_word)
        clean_words.append(clean_word.lower())  # HAVE TO ADD .lower() BECAUSE words.txt file is all lower case!!
    shortened_message = " ".join(clean_words)

    with open("words.txt", "r") as f:  # try load words.txt
        words = f.readlines()
        words = set([word.rstrip("\n") for word in words])  # getting rid of \n

    for rotation in range(1, 27):
        if set(functions.decrypt(shortened_message, rotation).split(" ")) & words:  # & is quickest way to compare two sets
            print(f"Potential decryption found: {functions.decrypt(shortened_message, rotation)}")
            user_input = input("Is this an accurate description? (Y/yes/N/no): ").upper()[0]
            if user_input == "Y":
                return functions.decrypt(initial_message, rotation)
            else:
                print("Continuing with decryption...")
    return False
