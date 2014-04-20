import random
import string


def generate_unsubscribe_token():
    return ''.join(random.choice(string.ascii_lowercase +
                                 string.ascii_uppercase +
                                 string.digits) for i in range(16))
