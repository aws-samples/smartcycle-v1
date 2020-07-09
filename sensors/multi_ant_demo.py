"""
    Code based on:
        https://github.com/mvillalba/python-ant/blob/develop/demos/ant.core/03-basicchannel.py
    in the python-ant repository and
        https://github.com/tomwardill/developerhealth
    by Tom Wardill
"""
import sys
import time
from ant.core import driver, node, event, message, log
from ant.core.constants import CHANNEL_TYPE_TWOWAY_RECEIVE, TIMEOUT_NEVER
import binascii
from diskcache import Cache

class HeartrateCallback(event.EventCallback):
    def process(self, msg):
        if isinstance(msg, message.ChannelBroadcastDataMessage):
            print('heartrate: received message')
            #print(len(msg.payload))
            hexValues = ''.join(['[{}] '.format(str(binascii.hexlify(b))) for b in msg.payload])
            #hexValues = binascii.hexlify(msg.payload)
            #print( "id:{} value:{} type:{}".format(message.number, hexValues, type(msg) ) )
            print(hexValues)
            cacheLocation = '/home/aws_cam/aws-smartcycle/db'
            with Cache(cacheLocation) as cache:
                cache[b'heartrate'] = ord(msg.payload[8])
                print('Cached heartrate: {}'.format(cache[b'heartrate']))

class TemperatureCallback(event.EventCallback):
    def process(self, msg):
        if isinstance(msg, message.ChannelBroadcastDataMessage):
            print('Temperature: received message')
            #print(len(msg.payload))
            hexValues = ''.join(['[{}] '.format(str(binascii.hexlify(b))) for b in msg.payload])
            #hexValues = binascii.hexlify(msg.payload)
            #print( "id:{} value:{} type:{}".format(message.number, hexValues, type(msg) ) )
            print(hexValues)

            print('Temperature Page ID: {}'.format(ord(msg.payload[1])))

            if ord(msg.payload[1]) == 1:
                current_temperature = 32 + (1.8 * (0.01 * int(str(binascii.hexlify(msg.payload[8])) + str(binascii.hexlify(msg.payload[7])),16)))
                print('Current Page1 Temnperature: {}'.format(current_temperature))

                cacheLocation = '/home/aws_cam/aws-smartcycle/db'
                with Cache(cacheLocation) as cache:
                    cache[b'temperature'] = current_temperature
                    print('Cached temperature: {}'.format(cache[b'temperature']))


class CadenceCallback(event.EventCallback):
    def process(self, msg):
        if isinstance(msg, message.ChannelBroadcastDataMessage):
            print('cadence: received message')
            #print(len(msg.payload))
            hexValues = ''.join(['[{}] '.format(str(binascii.hexlify(b))) for b in msg.payload])
            #hexValues = binascii.hexlify(msg.payload)
            #print( "id:{} value:{} type:{}".format(message.number, hexValues, type(msg) ) )
            print(hexValues)

            print('Cadence Data Page Ord: {} '.format(ord(msg.payload[1])))

            #Only process data page 128 data
            if ord(msg.payload[1]) == 128:
                curr_cad_rev_count = int(str(binascii.hexlify(msg.payload[8])) + str(binascii.hexlify(msg.payload[7])), 16)
                print('Cadence Rev Count: {}'.format(curr_cad_rev_count))
                curr_cad_event_time = int(str(binascii.hexlify(msg.payload[6])) + str(binascii.hexlify(msg.payload[5])), 16)
                print('Cadence Event Time: {}'.format(curr_cad_event_time))

                #Stop bit doesn't seem to exist for the Garmin cadence sensor
                #print('Cadence Page ID: {} Stop Bit: {}'.format(ord(msg.payload[1]), ord(msg.payload[2])))

                cacheLocation = '/home/aws_cam/aws-smartcycle/db'

                with Cache(cacheLocation) as c:
                    prev_cad_rev_count = c.get(b'prevcadrevcount', 0)
                    prev_cad_event_time = c.get(b'prevcadevttime', 0)

                    c[b'prevcadrevcount'] = curr_cad_rev_count
                    c[b'prevcadevttime'] = curr_cad_event_time

                    delta_cad_rev_count = curr_cad_rev_count - prev_cad_rev_count
                    delta_cad_event_time = curr_cad_event_time - prev_cad_event_time

                    print('Cadence Delta Rev Count: {} , Cadence Delta Evt Time: {}'.format(delta_cad_rev_count, delta_cad_event_time))

                    #avoid divide-by-zero errors; only re-calculate speed if input values greater than zero

                    if delta_cad_event_time > 0:
                        rpm = (delta_cad_rev_count * 60 * 1024)/delta_cad_event_time

                        print('Calc Cadence [RPM]: {}'.format(str(rpm)))
                        c[b'cadence'] = str(rpm)
                        print('Cached cadence (modified): {} \n =====\n'.format(c[b'cadence']))
                    else:
                        #save as a string to return a Truthy value
                        c[b'cadence'] = str(0)
                        print('Cached cadence (no new data): {} \n =====\n'.format(c[b'cadence']))


class SpeedCallback(event.EventCallback):
    def process(self, msg):
        if isinstance(msg, message.ChannelBroadcastDataMessage):
            print('speed: received message')
            #print(len(msg.payload))
            hexValues = ''.join(['[{}] '.format(str(binascii.hexlify(b))) for b in msg.payload])
            #hexValues = binascii.hexlify(msg.payload)
            #print( "id:{} value:{} type:{}".format(message.number, hexValues, type(msg) ) )
            print(hexValues)


            #Only process data page 5 data
            if ord(msg.payload[1]) == 5:
                curr_speed_rev_count = int(str(binascii.hexlify(msg.payload[8])) + str(binascii.hexlify(msg.payload[7])), 16)
                print('Speed Rev Count: {}'.format(curr_speed_rev_count))
                curr_speed_event_time = int(str(binascii.hexlify(msg.payload[6])) + str(binascii.hexlify(msg.payload[5])), 16)
                print('Speed Event Time (1024): {}'.format(curr_speed_event_time))

                print('Speed Page ID: {} Stop Bit: {}'.format(ord(msg.payload[1]), ord(msg.payload[2])))

                stop_bit = ord(msg.payload[2])
                #Only update speed value when stop bit = 0 which means bike is moving

                cacheLocation = '/home/aws_cam/aws-smartcycle/db'

                #false (zero) bit value means bike is in motion
                if stop_bit == 0:

                    with Cache(cacheLocation) as c:
                        prev_speed_rev_count = c.get(b'prevspdrevcount', 0)
                        prev_speed_event_time = c.get(b'prevspdevttime', 0)

                        c[b'prevspdrevcount'] = curr_speed_rev_count
                        c[b'prevspdevttime'] = curr_speed_event_time

                        delta_speed_rev_count = curr_speed_rev_count - prev_speed_rev_count
                        delta_speed_event_time = curr_speed_event_time - prev_speed_event_time

                        print('Delta Rev Count: {} , Delta Evt Time: {}'.format(delta_speed_rev_count, delta_speed_event_time))

                        #avoid divide-by-zero errors; only re-calculate speed if input values greater than zero

                        if delta_speed_event_time > 0:
                            #736mm = 29 inch circumfrence wheel
                            calc_speed = (delta_speed_rev_count * 0.736 * 1024)/delta_speed_event_time
                            kmh = int((calc_speed * 60 * 60) / 1000)
                            print('Calc Speed [m/s]: {}, KMH: {}'.format(str(calc_speed), str(kmh)))
                            c[b'speed'] = str(kmh)
                            print('Cached speed: {} \n =====\n'.format(c[b'speed']))
                else:
                    #Otherwise our speed is zero km/h (bike not moving)
                    with Cache(cacheLocation) as c:
                        c[b'speed'] = str(0)
                        c[b'prevspdrevcount'] = 0
                        c[b'prevspdevttime'] = 0
                        print('Cached speed: {} \n =====\n'.format(c[b'speed']))


class HRM(event.EventCallback):

    def __init__(self, serial, netkey):
        self.serial = serial
        self.netkey = netkey
        self.antnode = None
        self.channel = None
        self.channel2 = None
        self.channel3 = None
        self.channel4 = None

    def start(self):
        print("starting node")
        self._start_antnode()
        self._setup_channel()
        self.channel.registerCallback(CadenceCallback())
        self.channel2.registerCallback(SpeedCallback())
        self.channel3.registerCallback(HeartrateCallback())
        self.channel4.registerCallback(TemperatureCallback())
        print("start listening for device events")

    def stop(self):
        if self.channel:
            self.channel.close()
            self.channel.unassign()

        if self.channel2:
            self.channel2.close()
            self.channel2.unassign()

        if self.channel3:
            self.channel3.close()
            self.channel3.unassign()

        if self.channel4:
            self.channel4.close()
            self.channel4.unassign()

        if self.antnode:
            self.antnode.stop()

    def __enter__(self):
        return self

    def __exit__(self, type_, value, traceback):
        self.stop()

    def _start_antnode(self):
        stick = driver.USB2Driver(self.serial)
        self.antnode = node.Node(stick)
        
        print('node running:{}'.format(self.antnode.running))
        #if self.antnode.running == False:
        self.antnode.start()
        print('Antnode capabilities-Channels: {}, Networks: {}').format(self.antnode.getCapabilities()[0], self.antnode.getCapabilities()[1])

    def _setup_channel(self):
        key = node.NetworkKey('N:ANT+', self.netkey)
        self.antnode.setNetworkKey(0, key)

        #Cadence channel
        self.channel = self.antnode.getFreeChannel()
        self.channel.name = 'C:CAD'
        self.channel.assign('N:ANT+', CHANNEL_TYPE_TWOWAY_RECEIVE)
        self.channel.setID(122, 0, 0)
        self.channel.setSearchTimeout(TIMEOUT_NEVER)
	self.channel.setPeriod(8102)
        self.channel.setFrequency(57)
        self.channel.open()

        #Channel 2 - Speed
        self.channel2 = self.antnode.getFreeChannel()
        self.channel2.name = 'C:SPD'
        self.channel2.assign('N:ANT+', CHANNEL_TYPE_TWOWAY_RECEIVE)
        self.channel2.setID(123, 0, 0)
        self.channel2.setSearchTimeout(TIMEOUT_NEVER)
        self.channel2.setPeriod(8118)
        self.channel2.setFrequency(57) 
        self.channel2.open()

        #Channel 3  - Heartrate
        self.channel3 = self.antnode.getFreeChannel()
        self.channel3.name = 'C:HR'
        self.channel3.assign('N:ANT+', CHANNEL_TYPE_TWOWAY_RECEIVE)
        self.channel3.setID(120, 0, 0)
        self.channel3.setSearchTimeout(TIMEOUT_NEVER)
        self.channel3.setPeriod(8070)
        self.channel3.setFrequency(57)
        self.channel3.open()

        #Channel 4  - Temperature
        self.channel4 = self.antnode.getFreeChannel()
        self.channel4.name = 'C:TMP'
        self.channel4.assign('N:ANT+', CHANNEL_TYPE_TWOWAY_RECEIVE)
        self.channel4.setID(25, 0, 0)
        self.channel4.setSearchTimeout(TIMEOUT_NEVER)
        self.channel4.setPeriod(8192)
        self.channel4.setFrequency(57)
        self.channel4.open()

SERIAL = '/dev/ttyUSB0'
NETKEY = 'B9A521FBBD72C345'.decode('hex')

with HRM(serial=SERIAL, netkey=NETKEY) as hrm:
    hrm.start()
    while True:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            sys.exit(0)
