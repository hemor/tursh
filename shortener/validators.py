import re
import validators
from .models import ShortUrl


def valid_short_url(short_url):
    #   Validate that short url is of length 6 and it's of the format [0-9a-zA-Z]
    if len(short_url) == 6:
        pattern = r'[0-9a-zA-Z]{6}'
        result = re.match(pattern, short_url)
        if result:
            return True
    return False


def valid_url(full_url):
    return (validators.url(full_url) == True )  #   Validate full url via validatos module


def unique_short_url(short_url):
    #   Validate that short url doesn't exist
    try:
        url = ShortUrl.objects.get(short_url=short_url)
        return False
    except ShortUrl.DoesNotExist:
        return True
