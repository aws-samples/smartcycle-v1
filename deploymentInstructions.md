Bike Setup
----------

![](./myMediaFolder/media/image1.tiff){width="4.992343613298337in" height="3.745661636045494in"} *Figure1: SmartCycle bike setup*
---------------------------------------------------------------------------------------------------------------------------------

Overview
--------

The Smartcycle project was implemented as a set of Lambda functions and
scripts, along with supporting assets such as the object detection model
and MP3 audio files. Additionally, there is a sensor data reporting tool
that is deployed and used via the AWS Console. Overall, the Smartcycle
project is comprised of 4 major components:

1.  Object-detection service

2.  Audio alert service

3.  Sensor service

4.  Analytics application

Finally, we provide demo videos you can play to test out your Smartcycle
setup once complete.

Prerequisites
-------------

You can elect to implement the full Smartcycle implementation which
mounts on a bicycle or choose a minimalistic implementation based on
just one DeepLens device. We described the required hardware and
software components for both implementation approaches below.

### Required Hardware - Full Smartcycle Setup 

-   2 HDMI-compatible monitors and cables -- at least one larger
    (25-inch or greater), high-resolution monitors are recommended for
    the best detection of objects in demo videos. These monitors are for
    displaying our pre-recorded street scenes the DeepLens devices will
    watch for road hazards.

-   A bicycle -- since this is a proof-of-concept for demonstration
    purposes, we mounted the hardware listed below to a stationary
    bicycle (more specifically, a road bike attached to a bike stand).

-   At least one registered AWS DeepLens device, preferably two (front
    and rear). Available for purchase here: https://amzn.to/31OpGF9

To register your DeepLens device(s), please follow these instructions:
https://amzn.to/2TEb9rg

***For each*** DeepLens device you use, you will need:

-   An Internet connection for your DeepLens devices (Wifi or USB
    Ethernet adapter)

-   An USB hub -- we used: StarTech 4-port USB 3.0 mini hub:
    https://amzn.to/2LfoXIG

-   A Micro HDMI to HDMI adapter: https://amzn.to/2N02bpd

-   An HDMI cable to connect the DeepLens to a monitor

-   Small LCD monitor + monitor bike mount for displaying processed
    DeepLens video output: https://amzn.to/2WT9P9q,
    https://amzn.to/33Yl7co

-   For the *front* DeepLens only, a Suunto Movestick Mini ANT+ USB
    receiver (other ANT+ USB receivers may work as well):
    https://amzn.to/2FmxVOK

-   One C-clamp per DeepLens device to mount the DeepLens to the bike:
    https://amzn.to/2Y3ssnA

-   USB mouse and keyboard (used during setup)

-   Assorted zip ties or hook-and-loop straps to fasten cables to the
    bike

-   For the front DeepLens only, headphones or speakers with cable
    (connected via minijack plug) for audio alert playback

-   ANT+ devices/sensors (we started with these 4 sensors):

    -   Heart Rate Monitor (armband style): https://amzn.to/2RtwVNJ

    -   Temperature sensor: https://amzn.to/2XmJoZ3

    -   Speed + Cadence sensors: https://amzn.to/2IUOa6N

    -   (Optional) Other ANT+ compatible sensors and devices (i.e. power
        meter, suspension, shifting). Note that you will need to
        customize the Python code provided to work with these other ANT+
        Device Profiles.

### Required Software

On your local workstation

-   AWS CLI -- setup instructions can be found here:

> https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-welcome.html

-   A working Git client application, many options to choose from
    depending on your operating system. The standard Git installation
    uses a command line client or you can install a graphical client if
    you prefer: https://git-scm.com/downloads/guis/

-   Your favorite text editor or IDE: Atom, notepad, vim, etc.

On DeepLens devices:

-   Recommend installing Vim editor on your DeepLens device (for Python
    color-coded text) via apt-get:\
    sudo apt-get install vim

### Required Hardware - Minimal Smartcycle Setup

You can experience much of the Smartcycle functionality using just a
subset of the equipment required for the full Smartcycle setup. Use a
single DeepLens device, [ignore]{.underline} the hardware requirements
for the bike, bike stand, mounting brackets and C-clamps. You also only
need a subset of the ANT+ sensors -- we recommend the heartrate or
temperature sensors. You also only need one 25-inch or larger
HDMI-compatible monitor to play the pre-recorded "front-facing" street
scene video. Setup your single DeepLens using the "Configuring the
Front-facing DeepLens" instructions below. The front facing DeepLens
configuration will give you a subset of road hazards that will be
detectable, but will still provide audio and visual alerts, ANT+ sensor
data and sensor analytics.

### Configuring the Front-facing DeepLens

##### Deploy the Object Detection Sample DeepLens Project - DO NOT SKIP THIS STEP!

The Object Detection sample DeepLens project serves as the basis for the
Smartcycle. Your first step is to deploy the Object Detection project to
your front DeepLens. Instructions to do this can be found
[here](https://docs.aws.amazon.com/deeplens/latest/dg/deeplens-create-deploy-sample-project.html)[.]{.underline}

While you are on the DeepLens page, now would be a great time to copy
down your DeepLens device name and the default project topic

##### Download and Configure the Smartcycle Project Artifacts onto the DeepLens Device

Once the Object Detection sample project has been successfully deployed
to your DeepLens, you will now need to download and configure additional
code artifacts onto your DeepLens device that are required to run
Smartcycle.

First, assuming you have a keyboard/mouse/monitor connected to your
DeepLens, login to your DeepLens device to access your Ubuntu desktop.
Then launch a Terminal shell prompt. Optionally, you may choose to
connect to your DeepLens remotely over [SSH]{.underline} instead.\
\
From the *aws\_cam* user directory on the DeepLens, clone the
'aws-smartcycle' project from GitHub; once the clone download completes,
change into the 'aws-smartcycle' directory:

git clone aws-smartcycle.git\
\
cd \~/aws-smartcycle; ll

The ll command should show a directory contents, similar to the
following:\
![](./myMediaFolder/media/image2.tiff){width="6.5in"
height="2.878953412073491in"}

**At this point, make sure your ANT+ USB receiver is plugged into a USB
port on your DeepLens.** For the front-facing DeepLens device, run the
[install-front.sh]{.underline} shell script using *sudo* to deploy
additional customizations on the DeepLens. The installation script will
Python module dependencies and also configure the ANT+ USB settings.
This may take several minutes to complete.

sudo ./install-front.sh

#### Modify the Default GreenGrass Group DeepLens Deployment

You now will need to clone the Smartcycle project assets onto your local
workstation using Git. You will be deploying and configuring some of
these assets manually, such as the audio-service Lambda function. From
your workstation command line (or GUI) Git client, clone the Smartcycle
repository:

git clone ssh://git.amazon.com/pkg/Smartcyclev1

##### Deploy New Version of the deeplens-object-detection Lambda

The Smartcycle project uses its own customized copy of the
deeplens-object-detection Lambda function in order to recognize
different road hazards. You now will need to overwrite the default
deeplens-object-detection function you just deployed as part of the
DeepLens sample project with a customized version for Smartcycle.

Go to the *AWS Console \> Lambda \>* *Functions* and select the
"deeplens-object-detection" from the list of existing Lambdas.

![](./myMediaFolder/media/image3.tiff){width="8.648214129483815in"
height="0.2309886264216973in"}

Make sure you are on the most recent version of the Lambda function so
you can edit it. Select the field *Code entry type* *"Edit code inline"*
option *--* you should see the file "greenrassHelloWorld.py" loaded
inside the inline text editor.

Next, go to your local copy of the cloned Smartcycle project and open
the file object-detection/front-view/greengrassObjectDetector.py in your
local text editor. Then select all, copy and paste the contents of the
custom greengrassObjectDetector.py into the inline Lambda editor,
overwriting the existing deeplens-object-detection code. Keep all of the
other Python module dependencies already configured for the original
Lambda. *Save* your Lambda changes in the inline editor.

Note, for the front facing DeepLens device, it is important to use the
"front-view" version of the deeplens-object-detection Lambda, as it is
coded to detect hazards appearing in front of a cyclist.

Next, publish a new version of the Lambda function we just modified. Go
to the *Actions menu in the Lambda console \>* *Publish new version*.
Call it "Version 2" in the description field and click *Publish.*

![](./myMediaFolder/media/image4.tiff){width="6.5in"
height="2.140277777777778in"}

You will then need to create an Alias for the Lambda function. Aliases
are a reference we can use when deploying our Lambda functions and acts
as a placeholder, allowing us to decouple the Lambda version from the
GreenGrass Group deployment, which helps minimize the changes to our
Group configuration. Go to *Actions \> Create Alias.* In the *Name*
field, enter the name "PRODUCTION" (or whatever name you will
recognize). For the *Version* field, choose the version of the Lambda
you just created, in our case *version 2* -- **note you MUST use** **a**
**specific Lambda version number and not the "\$LATEST" option** **to
work with GreenGrass**. Click *Create* to save the new Alias.

![](./myMediaFolder/media/image5.tiff){width="6.5in"
height="3.953472222222222in"}

##### Deploy audio-service Lambda function

We will now create a new Lambda function that is responsible for playing
audio alerts when hazards are detected. Go back to the Lambda home page
and click on *Create function*.

![](./myMediaFolder/media/image6.tiff){width="6.5in"
height="2.870138888888889in"}

On the Create function page, choose *Author from scratch*, then enter a
*Function name* such as "audio-service". For the function *Runtime*,
choose "Python 2.7". Under *Permission \> Choose* or create an execution
role, select *Use an existing role*, then find an *Existing role* called
"AWSDeepLensLambdaRole" and choose that option. Finally, click *Create
Function* at the bottom corner of the page.

Once you have created the function, you will be taken the Lambda
configuration page. In the *Designer* panel (click to expand this panel
if necessary), click on the name of your function, for example
"audio-service" in the center of the panel -- this will expand the
*Function code* panel below.

![](./myMediaFolder/media/image7.tiff){width="6.5in"
height="2.3784722222222223in"}

Under *Function code \> Code entry type*, choose the *Upload a .zip
file* option from the select menu. Then under *Function package*, click
the *Upload* button to launch a dialog window and select
Smartcyclev1/audio/audio-service.zip from your local drive.

For the Runtime field, make sure "Python 2.7" has been selected. For the
Handler field, enter "audio-service.lambda\_handler" -- this is the
Python function that will be called in our audio-service.py Lambda
function code when triggered.

![](./myMediaFolder/media/image8.tiff){width="6.5in"
height="1.101388888888889in"}

Next, *Save* your changes for the audio-service Lambda function. Once
saved, you need to publish your function so you can more easily manage
any changes to the Lambda function made later. GreenGrass deployments
require that you use a specific Lambda version -- you cannot use an
intrinsic reference such as "\$LATEST".

Go to the *Actions* dropdown menu \> *Publish new version* option. For
the *Version description* field, enter "Version 1" in the text field and
click *Publish* to create the new version.

You will then need to create an Alias for the *audio-service* Lambda
function. Go to *Actions \> Create Alias.* In the *Name* field, enter
the name "PRODUCTION" (or whatever name you will recognize). For the
*Version* field, choose the version of the Lambda you just created, in
our case *version 1* -- **note you MUST use a specific Lambda version
number and not the "\$LATEST" option**. Click *Create* to save the new
Alias.

##### 

#### Modify the Default GreenGrass Project Configuration

The original Object Detection sample project is deployed as an AWS IoT
GreenGrass project to the DeepLens. In the AWS Console, go to *IoT Core
\> Greengrass \> Groups*. Find the Group that contains your DeepLens
device name and select it.

You will now need to modify the default GreenGrass configuration to
support the DeepLens hardware and local resource access required by the
Smartcycle Lambda functions and Python scripts. You will first modify
the Group's *Lambda* functions, then the *Resources*, and then
*Subscriptions*.

##### Modify audio-service Lambda for GreenGrass

First, you need to add our *audio-service* Lambda function to the
GreenGrass Group so you can assign Resources to it. In the GreenGrass
Group you selected, click on the left hand "*Lambdas*" link, then click
on "*Add Lambda*". Note, that you should see two or more existing Lambda
functions previously created when you registered you DeepLens and
deployed the Object Detection sample project to it.

Next, click on *"Use existing Lambda"* and choose the *audio-service*
Lambda you created in the earlier steps by clicking on its radio button.
Choose the "PRODUCTION" alias as the Lambda version to use, then click
Finish.

Once you are back on the Lambdas page, click on the *audio-service*
Lambda you just added, then *Edit.* Increase the *Memory limit* setting
to 32MB and increase the *Timeout* setting to 15 seconds. Finally,
Enable *Read access to the /sys directory* by clicking the Enable radio
button. Save your changes to the Lambda configuration by clicking the
*Update* button.

![](./myMediaFolder/media/image9.tiff){width="6.5in"
height="5.940972222222222in"}

##### Modify the deeplens-object-detection Lambda for GreenGrass

Now go back to your GreenGrass Group's *Lambdas* view and select the
*deeplens-object-detection Lambda* *\> Edit Configuration* menu item.

Scroll the bottom of the configuration page and click *Add another
version.* Choose the "PRODUCTION" alias you created earlier for the
deeplens-object-detection Lambda function. Then, remove any previous
Versions of the deeplens-object-detection Lambda that may exist (most
likely version 1 or version 2).

Next, you need to change the Lambda settings.

-   For the *Run as field, select the* *Another userID /group ID
    option*, then enter "1000" for the UID and "1000" for the GID.

-   *Memory limit* -- increase to "1536 MB"

-   Set *Timeout* to "2 seconds"

-   Set *Lambda lifecycle* to the *"Make this* *function long-lived and
    keep it running indefinitely"* option

-   Set *Read access to /sys directory* to the *"Enable"* option\
    \
    Finally, click *Update* to save your configuration settings.\
    \
    ![](./myMediaFolder/media/image10.tiff){width="5.7307688101487315in"
    height="7.5455129046369205in"}

##### Configure GreenGrass Group Resources

Next, you will give the Lambda functions smartcycle-audio and
deeplens-objection-detection access to local resources on the DeepLens.

Go to your GreenGrass Group's *Resources* menu option. You should see a
number of existing resources already defined for you device. GreenGrass
*Resources* give deployed Lambda functions the ability to access local
resources that are physically present on the Greengrass core device --
in this case, your DeepLens.

Click on the *Add local resource* button and enter the following
configuration information , repeating the steps for each of the four
Resources you need to create. Note that the device filesystem paths you
reference for the Resources Source Path and Destination Path must
already exist on the DeepLens device in order for the GreenGrass Group
deployment step to be successful; you have already created the required
filesystem paths when we cloned the Smartcycle project from GitHub on
the DeepLens device earlier in these instructions (any pre-existing
Resource paths have previously been created on the DeepLens as well).

Resource name: smartcycle\_audio\_files

Resource type: Volume

Source path: /home/aws\_cam/aws-smartcycle/audio/audio-files

Destination path: /home/aws\_cam/aws-smartcycle/audio/audio-files

Group owner file access permissions: select radio button for
"Automatically add OS group permissions of the Linux group that owns the
resource"

Lambda function affiliations: select the *"audio-service"* Lambda
function, then the *Read and write access* permission option.

![](./myMediaFolder/media/image11.tiff){width="6.5in"
height="5.634027777777778in"}

Resource name: diskcache\_dir

Resource type: Volume

Source path: /home/aws\_cam/aws-smartcycle/db

Destination path: /home/aws\_cam/aws-smartcycle/db

Group owner file access permissions: select radio button for
"Automatically add OS group permissions of the Linux group that owns the
resource"

Lambda function affiliations: choose BOTH "deeplens-object-detection"
AND "smartcycle-audio" Lambda functions with "Read-and-Write Access"

![](./myMediaFolder/media/image12.tiff){width="6.5in"
height="5.885416666666667in"}

Resource name: sound\_card\_resource -- this resource already exists as
part of the default DeepLens setup. However, you need to Edit this
resource and give the *audio-service* and *deeplens-object-detection*
Lambdas access to this resource by creating affiliations for them. Leave
all other settings as-is.

Lambda function affiliations: *Select another Lambda function to
attach*, then choose the audio-service Lambda with Read and write
access, save the resource settings by clicking Update at the bottom of
the page.

![](./myMediaFolder/media/image13.tiff){width="6.5in"
height="4.922916666666667in"}

Resource name: sound\_control\_resource -- this resource already exists
as part of the default DeepLens setup. However, you need to Edit this
resource and give the *audio-service* and deeplens-object-detection
Lambdas access to this resource by creating affiliations for them. Leave
all other settings as-is.

Lambda function affiliations: *Select another Lambda function to
attach*, then choose the audio-service Lambda with Read and write
access, save the resource settings by clicking Update at the bottom of
the page.

![](./myMediaFolder/media/image14.tiff){width="6.5in"
height="5.236805555555556in"}

**Finally, you will need to add your new version of the
"deeplens-object-detection" Lambda to all other pre-existing Resources
associated with this GreenGrass Group. Go into all remaining**
**Resource configurations and add the** **"PRODUCTION" (alias)**
**version of the** **"deeplens-object-detection" Lambda to the**
**Resource** **-- match the read/write permissions of the other Lambda
functions already affiliated with that Resource, otherwise you may run
into filesystem permission issues once deployed. You will have to repeat
this process several times to** **correctly associate the** **new
version of the deeplens-object-detection Lambda with each required
Resource.**

##### Add GreenGrass Group Subscriptions

Subscriptions will allow our GreenGrass Lambda functions to communicate
with each other through message passing. A Subscription consists of a
source, target, and topic. The source is the originator of the message.
The target is the destination of the message. The first step is
selecting your source and target.

You will add a GreenGrass topic Subscription that looks at only the
"smartcycle/object-detection" messages published to the IoT Cloud. The
smartcycle-audio Lambda function is triggered by incoming
"smartcycle-object-detection" messages. To configure the Subscription,
follow these steps in your GreenGrass Group.

1.  Go to the Subscriptions menu option in the GreenGrassGroup, the
    click the *Add Subscription* button.

2.  Under *Select a source,* choose the *Services\> IoT Cloud* option*.*

3.  *Under* *Select a target*, choose *Lambdas \> audio-service.* Then
    click the *Next* button.

4.  A Topic filter text field will appear, copy/paste in
    "smartcycle/object-detection" as the topic filter value, then click
    the *Next* button.

![](./myMediaFolder/media/image15.tiff){width="6.5in"
height="4.829861111111111in"}

#### Deploy Your GreenGrass Group Changes

For these changes to take effect, you need to re-deploy the GreenGrass
project itself to your front DeepLens device. In your GreenGrass Group,
go back to the *Deployments* page, then choose *Actions \> Deploy*.
Deployments with either successfully complete or will have a status of
failed. If the deployment failed, click on the failed deployment in the
listing to be taken to the error description -- drill into the detailed
error message on that page.

### 

### Test your Smartcycle deployment 

### 

Once the Smartcycle deployment has been successful, you can now run the
demo videos to test the hazard detection functionality provided by the
deeplens-object-detection Lambda. If you have ANT+ sensors, you can also
run the multi\_ant\_demo.py Python script to capture sensor data.

First, you need to download the demo videos (front and rear) to your
local workstation or whatever computer you will be demoing from. You can
download the videos from their Amazon S3 storage bucket here:

Front: https://aws-smartcycle1.s3.amazonaws.com/demo-front.mp4

Rear: https://aws-smartcycle1.s3.amazonaws.com/demo-back.mp4

### Note that each of these MP4 demo video files is approximately 720MB in size.

Next, log on to your DeepLens and start your ANT+ Python script from a
Terminal prompt change into the "sensors" directory and run the
following script:

cd \~/smartcycle-aws/sensors

sudo python multi\_ant\_demo.py

Now it's time to display the processed video stream from the DeepLens.
This video stream will be generated by the deeplens-object-detection
Lambda and will show detected road hazards, sensor metrics such as
heartrate, speed, temperature, etc. and will trigger audio alerts to
play.

From a new Terminal prompt, run the following command:

mplayer -demuxer lavf --lavfdopts format=mjpeg:probesize=32
/tmp/results.mjpeg

### 

### 

### 

### 

### 

### 

### 

### 

A window will appear showing the processed video output directly on your
DeepLens desktop. Start your demo video at this point. The object
detection model works best when demo video monitor takes up the entire
camera view. A successful test will render bounding boxes around hazards
like stop signs and stop lights as the demo video progresses through the
streets, you should see labels for your sensor data, and as each hazard
is detected you should hear an audio alert play warning you about the
specific hazard detected.

With respect to hardware setup, this is when you will need to have a
spare monitor to play the front or rear demo videos, preferably mounted
on some kind of stand. If you are not setting up the DeepLens on a bike,
a screw-mount camera tripod can be used and is really helpful to keep
the DeepLens pointing at the demo video. Be sure to have headphones or a
speaker plugged into your front DeepLens and the volume turned up to a
comfortable level so you can hear the audio alerts when a hazard is
detected in the demo video. Remember that the objects detected differ
between the front and rear DeepLens devices.

### Configuring the Rear-Facing DeepLens

Setting up your rear-facing DeepLens is much like setting up the
front-facing DeepLens. Follow all of the same instructions listed above,
except for the following:

-   Wherever there was a reference to "front-facing" installation
    scripts, use the "rear-facing" version instead.

```{=html}
<!-- -->
```
-   Omit the steps required to create and configure the audio-service
    Lambda. All audio alert playback will occur through the front-facing
    DeepLens.

-   Use the rear-facing version of the deeplens-object-detection custom
    lambda

###  \*Special thanks go to Johanne Bader and his excellent introduction to configuring the Suunto USB receiver for the Raspberry Pi, which helped greatly with the ANT+ sensor code. 

[https://www.johannesbader.ch/2014/06/track-your-heartrate-on-raspberry-pi-with-ant/]{.underline}

###     sudo systemctl restart greengrassdi 

### 

### 

### 

### 

### 

1.  

2.  a.  

    b.  i.  

3.  

4.  

5.  a.  

6.  a.  

7.  i.  
    ii. 

    ```{=html}
    <!-- -->
    ```
    a.  
    b.  

8.  
