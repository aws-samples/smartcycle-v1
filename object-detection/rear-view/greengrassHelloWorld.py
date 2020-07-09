#*****************************************************
#                                                    *
# Copyright 2018 Amazon.com, Inc. or its affiliates. *
# All Rights Reserved.                               *
#                                                    *
#*****************************************************
""" A sample lambda for object detection"""
from threading import Thread, Event
import os
import json
import numpy as np
import awscam
import cv2
import greengrasssdk
import mo
import ast
from diskcache import Cache

class LocalDisplay(Thread):
    """ Class for facilitating the local display of inference results
        (as images). The class is designed to run on its own thread. In
        particular the class dumps the inference results into a FIFO
        located in the tmp directory (which lambda has access to). The
        results can be rendered using mplayer by typing:
        mplayer -demuxer lavf -lavfdopts format=mjpeg:probesize=32 /tmp/results.mjpeg
    """
    def __init__(self, resolution):
        """ resolution - Desired resolution of the project stream """
        # Initialize the base class, so that the object can run on its own
        # thread.
        super(LocalDisplay, self).__init__()
        # List of valid resolutions
        RESOLUTION = {'1080p' : (1920, 1080), '720p' : (1280, 720), '480p' : (858, 480)}
        if resolution not in RESOLUTION:
            raise Exception("Invalid resolution")
        self.resolution = RESOLUTION[resolution]
        # Initialize the default image to be a white canvas. Clients
        # will update the image when ready.
        self.frame = cv2.imencode('.jpg', 255*np.ones([640, 480, 3]))[1]
        self.stop_request = Event()

    def run(self):
        """ Overridden method that continually dumps images to the desired
            FIFO file.
        """
        # Path to the FIFO file. The lambda only has permissions to the tmp
        # directory. Pointing to a FIFO file in another directory
        # will cause the lambda to crash.
        result_path = '/tmp/results.mjpeg'
        # Create the FIFO file if it doesn't exist.
        if not os.path.exists(result_path):
            os.mkfifo(result_path)
        # This call will block until a consumer is available
        with open(result_path, 'w') as fifo_file:
            while not self.stop_request.isSet():
                try:
                    # Write the data to the FIFO file. This call will block
                    # meaning the code will come to a halt here until a consumer
                    # is available.
                    fifo_file.write(self.frame.tobytes())
                except IOError:
                    continue

    def set_frame_data(self, frame):
        """ Method updates the image data. This currently encodes the
            numpy array to jpg but can be modified to support other encodings.
            frame - Numpy array containing the image data of the next frame
                    in the project stream.
        """
        ret, jpeg = cv2.imencode('.jpg', cv2.resize(frame, self.resolution))
        if not ret:
            raise Exception('Failed to set frame data')
        self.frame = jpeg

    def join(self):
        self.stop_request.set()

def greengrass_infinite_infer_run():
    """ Entry point of the lambda function"""
    try:
        # This object detection model is implemented as single shot detector (ssd), since
        # the number of labels is small we create a dictionary that will help us convert
        # the machine labels to human readable labels.
        model_name = "deploy_model_algo_1"
        model_type = 'ssd'
        input_width = 300
        input_height = 300
        max_threshold = 0.1
        # output_map = {0:'construction', 1:'crowd',2:'pothole',3:'person-bike',4:'person-pet', 5:'baby-strolls',6:'traffic-lights',7:'car', 8:'pedestrians'}
        output_map = {1: 'person', 2: 'bicycle', 3: 'car', 4: 'motorbike', 5: 'aeroplane', 6: 'bus', 7: 'train', 8: 'truck', 9: 'boat', 10: 'traffic light', 11: 'fire hydrant', 12: 'stop sign', 13: 'parking meter', 14: 'bench', 15: 'bird', 16: 'cat', 17: 'dog', 18: 'horse', 19: 'sheep', 20: 'cow', 21: 'elephant', 22: 'bear', 23: 'zebra', 24: 'giraffe', 25: 'backpack', 26: 'umbrella', 27: 'handbag', 28: 'tie', 29: 'suitcase', 30: 'frisbee', 31: 'skis', 32: 'snowboard', 33: 'sports ball', 34: 'kite', 35: 'baseball bat', 36: 'baseball glove', 37: 'skateboard', 38: 'surfboard', 39: 'tennis racket', 40: 'bottle', 41: 'wine glass', 42: 'cup', 43: 'fork', 44: 'knife', 45: 'spoon', 46: 'bowl', 47: 'banana', 48: 'apple', 49: 'sandwich', 50: 'orange', 51: 'broccoli', 52: 'carrot', 53: 'hot dog', 54: 'pizza', 55: 'donut', 56: 'cake', 57: 'chair', 58: 'sofa', 59: 'pottedplant', 60: 'bed', 61: 'diningtable', 62: 'toilet', 63: 'tvmonitor', 64: 'laptop', 65: 'mouse', 66: 'remote', 67: 'keyboard', 68: 'cell phone', 69: 'microwave', 70: 'oven', 71: 'toaster', 72: 'sink', 73: 'refrigerator', 74: 'book', 75: 'clock', 76: 'vase', 77: 'scissors', 78: 'teddy bear', 79: 'hair drier', 80: 'toothbrush'}
        #output_map = {0:'construction', 1:'crowd',2:'pothole',3:'person-bike',4:'person-pet', 5:'baby-strolls',6:'car',7:'pedestrians', 8:'person_bike', 9:'home',4:'person_pet',5:'baby_strolls'}

        # Create an IoT client for sending to messages to the cloud.
        client = greengrasssdk.client('iot-data')
        #iot_topic = '$aws/things/{}/infer'.format(os.environ['AWS_IOT_THING_NAME'])
        iot_topic = 'smartcycle/object-detection'
        # Create a local display instance that will dump the image bytes to a FIFO
        # file that the image can be rendered locally.
        local_display = LocalDisplay('480p')
        local_display.start()
        # The sample projects come with optimized artifacts, hence only the artifact
        # path is required.
        model_path = '/home/aws_cam/aws-smartcycle/object-detection/models/mxnet_deploy_model_algo_1_FP32_FUSED.xml'
        #error, model_path = mo.optimize(model_name, input_width, input_height , aux_inputs={'--epoch':0})
        # Load the model onto the GPU.
        client.publish(topic=iot_topic, payload='Loading object detection model: {0}'.format(model_path))
        model = awscam.Model(model_path, {'GPU': 1})
        client.publish(topic=iot_topic, payload='Object detection model loaded')
        # Set the threshold for detection
        #detection_threshold = 0.12
        detection_threshold = 0.30
        # The height and width of the training set images
        # input_height = 300
        # input_width = 300
        # Do inference until the lambda is killed.
        while True:
            # Get a frame from the video stream
            ret, frame = awscam.getLastFrame()
            if not ret:
                raise Exception('Failed to get frame from the stream')
            # Resize frame to the same size as the training set.
            frame_resize = cv2.resize(frame, (input_height, input_width))
            # Run the images through the inference engine and parse the results using
            # the parser API, note it is possible to get the output of doInference
            # and do the parsing manually, but since it is a ssd model,
            # a simple API is provided.
            parsed_inference_results = model.parseResult(model_type,
                                                         model.doInference(frame_resize))
            #client.publish(topic=iot_topic, payload = str(parsed_inference_results))
            # Compute the scale in order to draw bounding boxes on the full resolution
            # image.
            yscale = float(frame.shape[0]/input_height)
            xscale = float(frame.shape[1]/input_width)
            # Dictionary to be filled with labels and probabilities for MQTT
            cloud_output = {}
            topk = 30
            #client.publish(topic=iot_topic, payload = str(parsed_inference_results[model_type][0:topk]))
            req_list =  [2,3,4,6,8]
            # Get the detected objects and probabilities
            for obj in parsed_inference_results[model_type]:#[0:topk]:
                if obj['label'] >= 18 or obj['label'] not in req_list: #or output_map[obj['label']] != 'person' or  output_map[obj['label']] != 'bicycle' or output_map[obj['label']] != 'tst' or output_map[obj['label']] != 'motorbike' or output_map[obj['label']] != 'traffic light' or output_map[obj['label']] != 'stop sign' or output_map[obj['label']] != 'dog':
                    continue
                if obj['label'] == 3 and obj['prob'] *100 < 30: continue
                if obj['prob'] > detection_threshold:
                    #client.publish(topic=iot_topic, payload = str(obj['prob']))
                    #client.publish(topic=iot_topic, payload = str(cloud_output))
                    # Add bounding boxes to full resolution frame
                    xmin = int(xscale * obj['xmin']) \
                           + int((obj['xmin'] - input_width/2) + input_width/2)
                    ymin = int(yscale * obj['ymin'])
                    xmax = int(xscale * obj['xmax']) \
                           + int((obj['xmax'] - input_width/2) + input_width/2)
                    ymax = int(yscale * obj['ymax'])
                    # See https://docs.opencv.org/3.4.1/d6/d6e/group__imgproc__draw.html
                    # for more information about the cv2.rectangle method.
                    # Method signature: image, point1, point2, color, and tickness.
                    cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (255, 165, 20), 10)
                    # Amount to offset the label/probability text above the bounding box.
                    text_offset = 15
                    # See https://docs.opencv.org/3.4.1/d6/d6e/group__imgproc__draw.html
                    # for more information about the cv2.putText method.
                    # Method signature: image, text, origin, font face, font scale, color,
                    # and tickness
                    cv2.putText(frame, "{}: {:.2f}%".format(output_map[obj['label']],
                                                            obj['prob'] * 100),
                                (xmin, ymin-text_offset),
                                cv2.FONT_HERSHEY_SIMPLEX, 2.5, (255, 165, 20), 6)
                    # Store label and probability to send to cloud
                    cloud_output[output_map[obj['label']]] = obj['prob']

            #START SENSOR METRICS DISPLAY
            #Transparent rectangle overlays
            overlay = frame.copy()
            info_rect_color = (13,13,13)

            #top left rectangle
            cv2.rectangle(overlay, (0,0), (800,200), info_rect_color, -1)

            #bottom left rectangle
            cv2.rectangle(overlay, (0,frame.shape[0]-200), (900,frame.shape[0]), info_rect_color, -1)

            #top right rectangle
            cv2.rectangle(overlay, (frame.shape[1]-800,0), (frame.shape[1],200), info_rect_color, -1)

            #bottom right rectangle
            cv2.rectangle(overlay, (frame.shape[1]-900,frame.shape[0]-200), (frame.shape[1],frame.shape[0]), info_rect_color, -1)

            alpha = 0.60
            beta = 0.40

            cv2.addWeighted(overlay, alpha, frame, beta, 0, frame)

            cache = Cache('/home/aws_cam/aws-smartcycle/db')
            heartrate = cache[b'heartrate'] or '--'
            speed = cache[b'speed'] or '--'
            cadence = cache[b'cadence'] or '--'
            temperature = cache[b'temperature'] or '--'

            normal_font_color = (0,255,0)
            normal_font = cv2.FONT_HERSHEY_COMPLEX
            normal_font_scale = 3

            topleftcoord = (50, 125)
            bottomleftcoord = (50, frame.shape[0]-95)
            toprightcoord = (frame.shape[1]-750, 125)
            bottomrightcoord = (frame.shape[1]-750, frame.shape[0]-95)

            cv2.putText(frame, "{}: {}".format('HEARTRATE', heartrate), bottomleftcoord, normal_font, normal_font_scale, normal_font_color,6)
            cv2.putText(frame, "{}: {}".format('SPEED', speed), topleftcoord, normal_font, normal_font_scale, normal_font_color,6)
            cv2.putText(frame, "{}: {}".format('CADENCE', cadence), toprightcoord, normal_font, normal_font_scale, normal_font_color,6)
            cv2.putText(frame, "{}: {}F".format('TEMP', int(temperature)), bottomrightcoord, normal_font, normal_font_scale, normal_font_color,6)
            #cv2.putText(frame, "{}: {}".format(frame.shape[1], frame.shape[0]), (1250, 700), cv2.FONT_HERSHEY_SIMPLEX, 4.5, (66,144,161),6)

            # Set the next frame in the local display stream.
            # getall = ast.literal_eval(cloud_output)
            local_display.set_frame_data(frame)
            # Send results to the cloud
            client.publish(topic=iot_topic, payload=json.dumps(cloud_output))
    except Exception as ex:
        client.publish(topic=iot_topic, payload='Error in object detection lambda: {}'.format(ex))

greengrass_infinite_infer_run()
