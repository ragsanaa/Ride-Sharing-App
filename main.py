import random


def generate_password(characters, length):
    """Generate a random password from given characters with specified length."""
    if not characters:
        print("Error: No characters provided!")
        return None
    if length <= 0:
        print("Error: Password length must be greater than 0!")
        return None

    password = "".join(random.choice(characters) for _ in range(length))
    return password


if __name__ == "__main__":
    user_chars = input("Enter the characters to use for password generation: ")
    try:
        length = int(input("Enter the desired password length: "))
        password = generate_password(user_chars, length)
        if password:
            print("Generated Password:", password)
    except ValueError:
        print("Error: Please enter a valid number for password length.")
