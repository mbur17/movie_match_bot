from datetime import datetime
from random import choice, randint

from .constants import MIN_RELEASE_YEAR, RUSSIAN_LETTERS


def get_random_letter():
    return choice(RUSSIAN_LETTERS)


def get_random_year():
    return randint(MIN_RELEASE_YEAR, datetime.now().year)
