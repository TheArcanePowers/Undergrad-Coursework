"""This module contains the automatic decryptor function for Part 3.

FUNCTIONS:
    auto_decrypt(initial_message)

"""


import modules.functions as functions


# Part 3
def auto_decrypt(initial_message):
    """Iterate over all possible rotations, offering potential decryption to user.

    Args:
        initial_message (str): encrypted message to be decrypted.

    Returns:
        decrypted_message: Returns fully decrypted message if successful, False if unsuccessful.
    """
    # Taken from my work in Part 2
    # Cleans all the words.
    clean_words = []
    for item in initial_message.split(" ")[:9]:  # Note [:9], giving only the first 10 words as per assignment.
        clean_word = [char for char in item if char.isalpha()]  # Checks if each char is in the alphabet, and if so adds it to a new list
        clean_word = "".join(clean_word)  # consolidates the list of alphabetic characters into one string
        clean_words.append(clean_word.lower())  # word appended to clean_words. .lower() used due to words.txt being all lowercase
    shortened_message = " ".join(clean_words)

    try:
        with open("words.txt", "r") as f:  # try load words.txt
            words = f.readlines()
            words = set([word.rstrip("\n") for word in words])  # getting rid of \n
    except FileNotFoundError:
        raise ("Fatal Error: words.txt file missing in parent directory!")  # raises custom error

    for rotation in range(1, 27):
        if set(functions.decrypt(shortened_message, rotation).split(" ")) & words:  # & is quickest way to compare two sets
            print(f"Potential decryption found: {functions.decrypt(shortened_message, rotation)}")
            user_input = input("Is this an accurate decryption? (Y/yes/N/no): ").upper()[0]
            if user_input == "Y":
                return functions.decrypt(initial_message, rotation)  # note initial_message is decrypted, not the shortened_message
            else:
                print("Continuing with decryption...\n")
    return False  # User rejected all or program couldn't find any possible decryptions
