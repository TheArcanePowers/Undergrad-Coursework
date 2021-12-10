"""Main program running all parts."""
import random
import automated  # PART 4 module import
import functions  # PART 1 module import
import metrics  # PART 2 module import

message = None

print()  # newline for aesthetics

# PART 3.1
while True:
    message_mode = (input("Message mode - (F)ile or (M)anual entry: ").upper())[0]
    if message_mode == "F":
        while True:
            file_loc = input("Filename or filepath: ")
            try:
                with open(file_loc, "r") as f:
                    message = f.read().replace("\n", " ").upper()  # newlines into words, .upper() to comply with Part 1.4
                break  # as open file will not have thrown an exception
            except FileNotFoundError:
                pass  # do nothing, and thus let while True continue
        break  # once completed, break out of main while True loop
    elif message_mode == "M":
        break
    else:
        print("Invalid input. Please enter E for Encrypt or D for Decrypt")

# PART 1.2, 1.3
while True:
    cipher_mode = (input("Cipher mode - (E)ncrypt, (D)ecrypt, or (A)utodecrypt: ").upper())[0]  # taking upper and index 0 to account for lower case or full word input
    if cipher_mode == "E" or cipher_mode == "D" or cipher_mode == "A":
        break
    else:
        print("Invalid input. Please enter E for Encrypt or D for Decrypt")

while True and cipher_mode != "A":  # ciper_mode check due to part 4
    rotation_mode = (input("Rotation mode - (M)Numerical mode or (R)andom mode: ").upper())[0]
    if rotation_mode == "M":
        try:
            rotation = int(input("Interger value for how many places cipher should shift: "))
        except ValueError:
            print("Numerical mode requires interger input.")
        break
    elif rotation_mode == "R":
        rotation = random.randint(0, 26)  # Assumed max to be 26
        print(f"Random rotation chosen to be: {rotation}")
        break
    else:
        print("Invalid input. Please enter M for Numerical mode or R for Random mode")

if message is None:  # check if message has already been gotten from Part 3
    message = str(input("Message to be encrypted/decrypted: ")).strip().upper()  # .upper() to comply with PART 1.4

# print("\n")  # makes output look pretty :)

# calling PART 1.4
if cipher_mode == "E":
    print(f"\nEncrypted Message: {functions.encrypt(message, rotation)}")
if cipher_mode == "D":
    decrypted_message = functions.decrypt(message, rotation)  # doing this so don't call same function twice. probably quicker, just felt right
    print(f"\nDecrypted Message: {decrypted_message}")

# calling PART 4
if cipher_mode == "A":
    print("Beginning Auto-Decryption...")
    autodecrypt_result = automated.auto_decrypt(message)
    if autodecrypt_result is not False:  # False returned on failure of auto_decrypt
        print(f"Full decrypted message: {autodecrypt_result}")
        m = metrics.Metrics(autodecrypt_result)
    else:
        print("Auto-Decrypt failed!")
        quit()  # peacefully quit. this prevents part 2 from executing
# initializing PART 2
elif cipher_mode == "D":
    m = metrics.Metrics(decrypted_message)
elif cipher_mode == "E":
    m = metrics.Metrics(message)

# Printing Part 2
m.export_metrics()
list_of_words, word_dictionary = m.sort_words()
print("\nMetrics:")
print(f"List of up to five most frequent unique words: {list_of_words}")
print("Most common words in descending order:")
for i in word_dictionary:
    print(f"{i}: {word_dictionary[i]}")  # doing it individually like this because we were asked to in Part 2.4

# #!EXTRA#
m.produce_barchart()
