import random
import string


def generate_random_salt():
    length = 10
    name = "".join(random.choices(string.ascii_letters + string.digits, k=length))
    return name
