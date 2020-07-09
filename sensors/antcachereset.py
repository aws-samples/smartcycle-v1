from diskcache import Cache

cache_location ="../db" 
with Cache(cache_location) as cache:
    cache[b'speed'] = 0
    cache[b'prevspdrevcount'] = 0
    cache[b'prevspdevttime'] = 0
    cache[b'prevcadrevcount'] = 0
    cache[b'prevcadevttime'] = 0
    cache[b'cadence'] = 0
    cache[b'heartrate'] = 0
    cache[b'temperature'] = 0

    print('Speed cached value: ' + str(cache[b'speed']))
    print('Prev Speed Rev Count cached value: ' + str(cache[b'prevspdrevcount']))
    print('Prev Speed Event Time cached value: ' + str(cache[b'prevspdevttime']))
    print('Previous Cadence Rev Count cached value: ' + str(cache[b'prevcadrevcount']))
    print('Previous Cadence Event Time cached value: ' + str(cache[b'prevcadevttime']))
    print('Cadence cached value: ' + str(cache[b'cadence']))
    print('Heartrate cached value: ' + str(cache[b'heartrate']))
    print('Temperature cached value: ' + str(cache[b'temperature']))




