from __future__ import print_function

from diskcache import Cache
#import random
import time
import json
import os
import logging
#import greengrasssdk
from playsound import playsound
from datetime import datetime, timedelta

cacheLocation = os.getenv('DISKCACHE_DIR', '/home/aws_cam/diskcachedir')
audioFileLocation = os.getenv('AUDIO_FILE_DIR', '/home/aws_cam/smartcycle/sc-audio/audio-files/')
#cacheLocation = os.getenv('DISKCACHE_DIR', '/tmp/diskcache')
#audioFileLocation = os.getenv('AUDIO_FILE_DIR', '/Users/simcik/src/sc-audio/audio-files/')

log = logging.getLogger()
log.addHandler(logging.StreamHandler())
log.setLevel(logging.INFO)

# Create an IoT client for getting messages from the cloud.
#client = greengrasssdk.client('iot-data')
#iot_topic = '$aws/things/{}/infer'.format(os.environ['AWS_IOT_THING_NAME'])

def is_empty(structure):
    if structure:
        return True
    else:
        return False

def date_diff(dt1, dt2):
    timediff = dt2 - dt1
    return timediff.days * 24 * 3600 + timediff.seconds

def is_alertable(alert_name):

    if alert_name == 'person':
        with Cache(cacheLocation) as cache:
            person_last_alert_time = cache.get(b'alertpersonevent', datetime.now() - timedelta(days=1))
            log.info('Person last alert time reference: {}'.format(person_last_alert_time))

        if date_diff(person_last_alert_time, datetime.now()) > 60:
            return True
        else:
            return False

    elif alert_name == 'bicycle':
        with Cache(cacheLocation) as cache:
            bicycle_last_alert_time = cache.get(b'alertbicycleevent', datetime.now() - timedelta(days=1))
            log.info('Bicycle last alert time reference: {}'.format(bicycle_last_alert_time))

        if date_diff(bicycle_last_alert_time, datetime.now()) > 60:
            return True
        else:
            return False

    elif alert_name == 'car':
        with Cache(cacheLocation) as cache:
            car_rear_last_alert_time = cache.get(b'alertcarrearevent', datetime.now() - timedelta(days=1))
            log.info('Car (rear) last alert time reference: {}'.format(car_rear_last_alert_time))

        if date_diff(car_rear_last_alert_time, datetime.now()) > 60:
            return True
        else:
            return False

    elif alert_name == 'stop sign':
        with Cache(cacheLocation) as cache:
            stop_sign_last_alert_time = cache.get(b'alertstopsignevent', datetime.now() - timedelta(days=1))
            log.info('Stop Sign last alert time reference: {}'.format(stop_sign_last_alert_time))

        if date_diff(stop_sign_last_alert_time, datetime.now()) > 60:
            return True
        else:
            return False

    elif alert_name == 'traffic light':
        with Cache(cacheLocation) as cache:
            traffic_light_last_alert_time = cache.get(b'alerttrafficlightevent', datetime.now() - timedelta(days=1))
            log.info('Traffic Light last alert time reference: {}'.format(traffic_light_last_alert_time))

        if date_diff(traffic_light_last_alert_time, datetime.now()) > 60:
            return True
        else:
            return False

    elif alert_name == 'dog':
        with Cache(cacheLocation) as cache:
            dog_last_alert_time = cache.get(b'alertdogevent', datetime.now() - timedelta(days=1))
            log.info('Dog last alert time reference: {}'.format(dog_last_alert_time))

        if date_diff(dog_last_alert_time, datetime.now()) > 60:
            return True
        else:
            return False

def alert(key):

    if key == 'person' and is_alertable('person'):
        log.info('playsound for Person')
        playsound(audioFileLocation + 'pedestrians_ahead.mp3')
        with Cache(cacheLocation) as cache:
            cache[b'alertpersonevent'] = datetime.now()

    elif key == 'bicycle' and is_alertable('bicycle'):
        log.info('playsound for Bicycle')
        playsound(audioFileLocation + 'warning_cyclists_ahead.mp3')
        with Cache(cacheLocation) as cache:
            cache[b'alertbicycleevent'] = datetime.now()

    elif key == 'car' and is_alertable('car'):
        log.info('playsound for Car (rear)')
        playsound(audioFileLocation + 'car_approaching_from_behind.mp3')
        with Cache(cacheLocation) as cache:
            cache[b'alertcarrearevent'] = datetime.now()

    elif key == 'stop sign' and is_alertable('stop sign'):
        log.info('playsound for Stop Sign')
        playsound(audioFileLocation + 'generic-warn-stop-sign.mp3')
        with Cache(cacheLocation) as cache:
            cache[b'alertstopsignevent'] = datetime.now()

    elif key == 'traffic light' and is_alertable('traffic light'):
        log.info('playsound for Stop Light')
        playsound(audioFileLocation + 'generic-warn-stop-light.mp3')
        with Cache(cacheLocation) as cache:
            cache[b'alerttrafficlightevent'] = datetime.now()

    elif key == 'dog' and is_alertable('dog'):
        log.info('playsound for Dog')
        playsound(audioFileLocation + 'dog_spotted.mp3')
        with Cache(cacheLocation) as cache:
            cache[b'alertdogevent'] = datetime.now()

def lambda_handler(event, context):
    log.info('Event data: {}'.format(event))
    #og.info('Ctx data: {}'.format(context))

    #detectedObjects = json.loads('{"person": 0.61865234375, "dog": 0.59326171875, "stop sign": 0.59326171875, "traffic light": 0.59326171875, "car": 0.59326171875}')
    detectedObjects = event

    #print(len(detectedObjects))

    for key in detectedObjects:
        alert(key)

    #time.sleep(1)

    #if not is_empty(detectedObjects):

#     while True:
#         with Cache(cacheLocation) as cache:
#
#             cache[b'heartrate'] = random.randint(1, 100)
#             print('Heartrate: ', cache[b'heartrate'])
#
#             cache[b'speed'] = random.randint(1, 100)
#             print('Speed: ', cache[b'speed'])
#
#             cache[b'cadence'] = random.randint(1, 100)
#             print('Cadence: ', cache[b'cadence'])
#
#             time.sleep(1)


if __name__ == "__main__":
    event, context = {}, {}
    lambda_handler(event, context)