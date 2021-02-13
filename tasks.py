import os
from huey import RedisHuey
import random

huey = RedisHuey(url=os.getenv('REDIS_URL'))

@huey.task(retries=3, retry_delay=60)
def get_random_num():
    print("Czesc jestem workerem i mam 3 podejscia")
    num = random.randint(1,5)
    if num == 2:
        return True
    else:
        print("Nie udało sie!")