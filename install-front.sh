# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0
#!/bin/bash

apt-get -y install vim

pip install --upgrade pip

hash python2  2>/dev/null || { echo >&2 "I require Python2 but it's not installed.  Aborting."; exit 1; }
hash pip2 2>/dev/null || { echo >&2 "I require Pip but it's not installed.  Aborting."; exit 1; }
hash curl 2>/dev/null || { echo >&2 "I require Curl but it's not installed.  Aborting."; exit 1; }

pip2 install -r /home/aws_cam/aws-smartcycle/sensors/requirements.txt;
pip2 install -r /home/aws_cam/aws-smartcycle/audio/requirements.txt;

# Once the model binary is trained and available, filename mxnet_deploy_model_algo_<>_FP32_FUSED.bin can be copied to /home/aws_cam/aws-smartcycle/<>
curl <model-binary-filepath;s3 location> -o /home/aws_cam/aws-smartcycle/object-detection/models/mxnet_deploy_model_algo_1_FP32_FUSED.bin

cd ..
git clone https://github.com/baderj/python-ant.git

apt-get install -y python-setuptools
cd python-ant/
python setup.py install

cp /home/aws_cam/aws-smartcycle/sensors/garmin-ant2.rules /etc/udev/rules.d/garmin-ant2.rules

lsusb

dmesg | tail
