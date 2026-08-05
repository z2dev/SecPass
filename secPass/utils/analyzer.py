import re
import random
import string
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
COMMON_PASSWORDS_FILE = BASE_DIR / "common_passwords.txt"

try:
    COMMON_PASSWORDS = {
        line.strip().lower()
        for line in COMMON_PASSWORDS_FILE.read_text(
            encoding="utf-8"
        ).splitlines()
        if line.strip()
    }

    print(f"Loaded {len(COMMON_PASSWORDS)} common passwords")

except FileNotFoundError:

    print(f"File not found: {COMMON_PASSWORDS_FILE}")

    COMMON_PASSWORDS = {
        "password",
        "123456",
        "123456789",
        "12345678",
        "qwerty",
        "abc123",
        "111111",
        "123123",
        "admin",
        "welcome",
        "letmein"
    }


WORDS = [

    "Falcon",
    "Phoenix",
    "Galaxy",
    "Shadow",
    "Rocket",
    "Storm",
    "Ocean",
    "Nova",
    "Tiger",
    "Eagle"

]

SPECIAL_CHARACTERS = "!@#$%^&*"


STRENGTH_LEVELS = {

    "very_weak": {

        "text": "Very Weak",
        "color": "#b91c1c"

    },

    "weak": {

        "text": "Weak",
        "color": "#ef4444"

    },

    "medium": {

        "text": "Medium",
        "color": "#f59e0b"

    },

    "strong": {

        "text": "Strong",
        "color": "#22c55e"

    },

    "very_strong": {

        "text": "Very Strong",
        "color": "#15803d"

    }

}


def has_uppercase(password):

    return bool(
        re.search(r"[A-Z]", password)
    )


def has_lowercase(password):

    return bool(
        re.search(r"[a-z]", password)
    )


def has_numbers(password):

    return bool(
        re.search(r"\d", password)
    )


def has_special_characters(password):

    return bool(

        re.search(

            r"[!@#$%^&*()_\-+=\[\]{};:'\",.<>/?\\|`~]",

            password

        )

    )


def is_common_password(password):

    return password.lower() in COMMON_PASSWORDS


def has_repeated_pattern(password):

    if len(password) < 4:

        return False

    if len(set(password)) == 1:

        return True

    return bool(

        re.search(

            r"(.)\1{2,}",

            password

        )

    )


def has_sequence(password):

    password = password.lower()

    sequences = [

        "0123456789",

        "123456789",

        "abcdefghijklmnopqrstuvwxyz",

        "qwertyuiop",

        "asdfghjkl",

        "zxcvbnm"

    ]

    for sequence in sequences:

        for i in range(len(sequence) - 3):

            part = sequence[i:i + 4]

            if part in password:

                return True

            if part[::-1] in password:

                return True

    return False


def calculate_score(password):

    score = 0

    checks = {

        "length": len(password) >= 8,

        "uppercase": has_uppercase(password),

        "lowercase": has_lowercase(password),

        "number": has_numbers(password),

        "special": has_special_characters(password)

    }

    if len(password) >= 8:
        score += 20

    if len(password) >= 12:
        score += 10

    if checks["uppercase"]:
        score += 15

    if checks["lowercase"]:
        score += 15

    if checks["number"]:
        score += 20

    if checks["special"]:
        score += 20

    warning = ""

    if is_common_password(password):

        score = min(score, 20)

        warning = "Warning: This password is easy to guess because it is commonly used."

    elif has_repeated_pattern(password):

        score -= 15

        warning = "Warning: Repeated characters make your password easier to guess."

    elif has_sequence(password):

        score -= 15

        warning = "Warning: Sequential characters make your password easier to guess."

    score = max(0, min(score, 100))

    return score, checks, warning



def get_strength(score):

    if score <= 25:
        return STRENGTH_LEVELS["very_weak"]

    if score <= 49:
        return STRENGTH_LEVELS["weak"]

    if score <= 69:
        return STRENGTH_LEVELS["medium"]

    if score <= 89:
        return STRENGTH_LEVELS["strong"]

    return STRENGTH_LEVELS["very_strong"]


def generate_suggestions(password):

    suggestions = []

    base = re.sub(r"[^A-Za-z]", "", password)

    if len(base) > 6:
        base = base[:6]

    if len(base) < 3:
        base = random.choice(WORDS)

    while len(suggestions) < 3:

        suggestion = (
            base.capitalize()
            + random.choice(SPECIAL_CHARACTERS)
            + str(random.randint(100, 999))
            + random.choice(string.ascii_uppercase)
        )

        if (
            suggestion not in suggestions
            and not is_common_password(suggestion)
        ):
            suggestions.append(suggestion)

    return suggestions


def analyze_password(password):

    score, checks, warning = calculate_score(password)

    strength = get_strength(score)

    if strength["text"] in ["Strong", "Very Strong"]:
        suggestions = []
    else:
        suggestions = generate_suggestions(password)

    result = {

        "score": score,
        "strength": strength,
        "warning": warning,
        "checks": checks,
        "suggestions": suggestions

    }

    return result
