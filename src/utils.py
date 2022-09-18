import random
import time


def random_id(length: int = 16) -> int:
    random_identity = str(random.randint(1, 9))
    for _ in range(0, length - 6):
        random_identity += str(random.randint(0, 9))
    random_identity += rand_time_func()
    return int(random_identity)


def rand_time_func():
    rand_time = int(int(time.time()) * random.random())
    return str(rand_time)[:5]