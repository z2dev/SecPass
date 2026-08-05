# Password generator
from utils.analyzer import is_common_password
import random
import string

SPECIAL_CHARACTERS = "!@#$%^&*"

def generate_password(length=16):

    if length < 12:
        length = 12

    while True:

        password = [

            random.choice(string.ascii_uppercase),

            random.choice(string.ascii_lowercase),

            random.choice(string.digits),

            random.choice(SPECIAL_CHARACTERS)

        ]

        characters = (

            string.ascii_letters
            + string.digits
            + SPECIAL_CHARACTERS

        )

        while len(password) < length:

            password.append(

                random.choice(characters)

            )

        random.shuffle(password)

        password = "".join(password)

        if not is_common_password(password):

            return password

