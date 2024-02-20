from uuid import uuid4


def generate_id():
    return str(uuid4())


def generate_random_str():
    s = str(uuid4())
    return s.split("-")[0]
