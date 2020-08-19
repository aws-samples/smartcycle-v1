# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0
from diskcache import Cache

with Cache('../db') as cache:
    print('Heartrate: ', cache[b'heartrate'])
    print('Speed: ', cache[b'speed'])
    print('Cadence: ', cache[b'cadence'])
