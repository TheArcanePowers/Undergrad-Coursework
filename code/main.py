"""Main program running all parts."""
import random
import automated  # PART 4 import
import functions  # PART 1 import
import metrics  # PART 2 import

message = None

# PART 3.1
while True:
    message_mode = (input("Message mode - File or Manual entry: ").upper())[0]
    if message_mode == "F":
        while True:
            file_loc = input("Filename or filepath: ")
            try:
                with open(file_loc, "r") as f:
                    message = f.read().replace("\n", " ")  # newlines into words
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

while True and cipher_mode != "A":
    rotation_mode = (input("Rotation mode - (M)Numerical mode or (R)Random mode: ").upper())[0]
    if rotation_mode == "M":
        try:
            rotation = int(input("Interger value for how many places cipher should shift: "))
        except ValueError:
            print("Numerical mode requires interger input.")
        break
    elif rotation_mode == "R":
        rotation = random.randint(0, 26)  # Assumed max to be 26
        break
    else:
        print("Invalid input. Please enter M for Numerical mode or R for Random mode")

if message is None:  # check if message has already been gotten from file
    message = str(input("Message to be encrypted/decrypted: ")).strip().upper()  # .upper() to comply with PART 1.4

# calling PART 1.4
if cipher_mode == "E":
    print(functions.encrypt(message, rotation))
if cipher_mode == "D":
    decrypted_message = functions.decrypt(message, rotation)  # doing this so don't call same function twice. probably quicker, just felt right
    print(decrypted_message)
# calling PART 4
if cipher_mode == "A":
    print("Beginning Auto-Decryption...")
    autodecrypt_result = automated.auto_decrypt(message)
    if autodecrypt_result is not False:
        print(f"Full decrypted message: {autodecrypt_result}")
    else:
        print("Auto-Decrypt failed!")

# calling PART 2
if autodecrypt_result is not False:  # Accounting for part 4
    if cipher_mode == "D":
        m = metrics.Metrics(decrypted_message)
    else:
        m = metrics.Metrics(message)
    m.export_metrics()
    m.print_sorted_words()
