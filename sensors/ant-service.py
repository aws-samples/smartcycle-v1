from __future__ import print_function

from diskcache import Cache
import random
import time
import json
import os

cacheLocation = os.getenv('DISKCACHE_DIR', '/home/aws_cam/diskcachedir' )

def lambda_handler(event, context):
    while True:
        with Cache(cacheLocation) as cache:

            cache[b'heartrate'] = random.randint(1, 100)
            print('Heartrate: ', cache[b'heartrate'])

            cache[b'speed'] = random.randint(1, 100)
            print('Speed: ', cache[b'speed'])

            cache[b'cadence'] = random.randint(1, 100)
            print('Cadence: ', cache[b'cadence'])

            time.sleep(1)

if __name__ == "__main__":
    event, context = {}, {}
    lambda_handler(event, context)

