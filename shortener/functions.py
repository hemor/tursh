import string
import random


def generate_django_secret_key():
    """ Generate 50 characters to use as django's secret key"""
    ascii_chars = string.ascii_letters
    digits = string.digits
    punctuations = string.punctuation
    punctuations = punctuations.replace('\'', '')   # Remove '
    punctuations = punctuations.replace('"', '')    # Remove "
    punctuations = punctuations.replace('\\', '')   # Remove \
    punctuations = punctuations.replace('`', '')  # Remove \

    chars = ''.join([ascii_chars, digits, punctuations])

    SECRET_KEY = ''.join([random.SystemRandom().choice(chars)
                          for i in range(50)])

    return SECRET_KEY
