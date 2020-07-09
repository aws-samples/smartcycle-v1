## Bike Setup

## ![](./myMediaFolder/media/image1.tiff)
_Figure1: SmartCycle bike setup_

## Overview

The Smartcycle project was implemented as a set of Lambda functions and scripts, along with supporting assets such as the object detection model and MP3 audio files. Additionally, there is a sensor data reporting tool that is deployed and used via the AWS Console. Overall, the Smartcycle project is comprised of 4 major components:

1. Object-detection service
2. Audio alert service
3. Sensor service
4. Analytics application

Finally, we provide demo videos you can play to test out your Smartcycle setup once complete.

## Prerequisites

You can elect to implement the full Smartcycle implementation which mounts on a bicycle or choose a minimalistic implementation based on just one DeepLens device. We described the required hardware and software components for both implementation approaches below.

### Required Hardware - Full Smartcycle Setup


- 2 HDMI-compatible monitors and cables – at least one larger (25-inch or greater), high-resolution monitors are recommended for the best detection of objects in demo videos. These monitors are for displaying our pre-recorded street scenes the DeepLens devices will watch for road hazards.

- A bicycle – since this is a proof-of-concept for demonstration purposes, we mounted the hardware listed below to a stationary bicycle (more specifically, a road bike attached to a bike stand).

- At least one registered AWS DeepLens device, preferably two (front and rear). Available for purchase here: [https://amzn.to/31OpGF9](https://amzn.to/31OpGF9)

To register your DeepLens device(s), please follow these instructions: [https://amzn.to/2TEb9rg](https://amzn.to/2TEb9rg)

_ **For each** _ DeepLens device you use, you will need:

- An Internet connection for your DeepLens devices (Wifi or USB Ethernet adapter)
- An USB hub – we used: StarTech 4-port USB 3.0 mini hub: [https://amzn.to/2LfoXIG](https://amzn.to/2LfoXIG)
- A Micro HDMI to HDMI adapter: [https://amzn.to/2N02bpd](https://amzn.to/2N02bpd)
- An HDMI cable to connect the DeepLens to a monitor
- Small LCD monitor + monitor bike mount for displaying processed DeepLens video output: [https://amzn.to/2WT9P9q](https://amzn.to/2WT9P9q), [https://amzn.to/33Yl7co](https://amzn.to/33Yl7co)
- For the _front_ DeepLens only, a Suunto Movestick Mini ANT+ USB receiver (other ANT+ USB receivers may work as well): [https://amzn.to/2FmxVOK](https://amzn.to/2FmxVOK)
- One C-clamp per DeepLens device to mount the DeepLens to the bike: [https://amzn.to/2Y3ssnA](https://amzn.to/2Y3ssnA)
- USB mouse and keyboard (used during setup)
- Assorted zip ties or hook-and-loop straps to fasten cables to the bike
- For the front DeepLens only, headphones or speakers with cable (connected via minijack plug) for audio alert playback
- ANT+ devices/sensors (we started with these 4 sensors):
  - Heart Rate Monitor (armband style): [https://amzn.to/2RtwVNJ](https://amzn.to/2RtwVNJ)
  - Temperature sensor: https://amzn.to/2XmJoZ3
  - Speed + Cadence sensors: [https://amzn.to/2IUOa6N](https://amzn.to/2IUOa6N)
  - (Optional) Other ANT+ compatible sensors and devices (i.e. power meter, suspension, shifting). Note that you will need to customize the Python code provided to work with these other ANT+ Device Profiles.

### Required Software

On your local workstation

- AWS CLI – setup instructions can be found here:

[https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-welcome.html](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-welcome.html)

- A working Git client application, many options to choose from depending on your operating system. The standard Git installation uses a command line client or you can install a graphical client if you prefer: [https://git-scm.com/downloads/guis/](https://git-scm.com/downloads/guis/)

- Your favorite text editor or IDE: Atom, notepad, vim, etc.

On DeepLens devices:

- Recommend installing Vim editor on your DeepLens device (for Python color-coded text) via apt-get:
sudo apt-get install vim

Smartcycle uses Python 2.7.

### Required Hardware - Minimal Smartcycle Setup

You can experience much of the Smartcycle functionality using just a subset of the equipment required for the full Smartcycle setup. Use a single DeepLens device, ignore the hardware requirements for the bike, bike stand, mounting brackets and C-clamps. You also only need a subset of the ANT+ sensors – we recommend the heartrate or temperature sensors. You also only need one 25-inch or larger HDMI-compatible monitor to play the pre-recorded &quot;front-facing&quot; street scene video. Setup your single DeepLens using the &quot;Configuring the Front-facing DeepLens&quot; instructions below. The front facing DeepLens configuration will give you a subset of road hazards that will be detectable, but will still provide audio and visual alerts, ANT+ sensor data and sensor analytics.

### Configuring the Front-facing DeepLens

##### Deploy the Object Detection Sample DeepLens Project - DO NOT SKIP THIS STEP!

The Object Detection sample DeepLens projects serves as the basis for the Smartcycle project. Your first step is to deploy the Object Detection project to your front DeepLens. Instructions to do this can be found [here](https://docs.aws.amazon.com/deeplens/latest/dg/deeplens-create-deploy-sample-project.html).

While you are on the DeepLens page, now would be a great time to copy down your DeepLens device name and the default project topic

##### Download and Configure the Smartcycle Project Artifacts onto the DeepLens Device

Once the Object Detection sample project has been successfully deployed to your DeepLens, you will now need to download and configure additional code artifacts onto your DeepLens device that are required to run Smartcycle.

First, assuming you have a keyboard/mouse/monitor connected to your DeepLens, login to your DeepLens device to access your Ubuntu desktop. Then launch a Terminal shell prompt. Optionally, you may choose to connect to your DeepLens remotely over SSH instead.

From the _aws\_cam_ user directory on the DeepLens, clone the &#39;aws-smartcycle&#39; project from GitHub; once the clone download completes, change into the &#39;aws-smartcycle&#39; directory:

git clone aws-smartcycle.git

 cd ~/aws-smartcycle; ll

The llcommand should show a directory contents, similar to the following:
 ![](RackMultipart20200709-4-1s1c7lq_html_d5ab460898505091.gif)

**At this point, make sure your ANT+ USB receiver is plugged into a USB port on your DeepLens.** For the front-facing DeepLens device, run the install-front.sh shell script using _sudo_ to deploy additional customizations on the DeepLens. The installation script will Python module dependencies and also configure the ANT+ USB settings. This may take several minutes to complete.

sudo ./install-front.sh

#### Modify the Default GreenGrass Group DeepLens Deployment

You now will need to clone the Smartcycle project assets onto your local workstation using Git. You will be deploying and configuring some of these assets manually, such as the audio-service Lambda function. From your workstation command line (or GUI) Git client, clone the Smartcycle repository:

git clone ssh://git.amazon.com/pkg/Smartcyclev1

##### Deploy New Version of the deeplens-object-detection Lambda

The Smartcycle project uses its own customized copy of the deeplens-object-detection Lambda function in order to recognize different road hazards. You now will need to overwrite the default deeplens-object-detection function you just deployed as part of the DeepLens sample project with a customized version for Smartcycle.

Go to the _AWS Console \&gt; Lambda \&gt; Functions_ and select the &quot;deeplens-object-detection&quot; from the list of existing Lambdas.

![](RackMultipart20200709-4-1s1c7lq_html_9021d2705b7df683.gif)

Make sure you are on the most recent version of the Lambda function so you can edit it. Select the field _Code entry type_ _&quot;Edit code inline&quot;_option _–_ you should see the file &quot;greenrassHelloWorld.py&quot; loaded inside the inline text editor.

Next, go to your local copy of the cloned Smartcycle project and open the fileobject-detection/front-view/greengrassObjectDetector.py in your local text editor. Then select all, copy and paste the contents of the custom greengrassObjectDetector.py into the inline Lambda editor, overwriting the existing deeplens-object-detection code. Keep all of the other Python module dependencies already configured for the original Lambda. _Save_ your Lambda changes in the inline editor.

Note, for the front facing DeepLens device, it is important to use the &quot;front-view&quot; version of the deeplens-object-detection Lambda, as it is coded to detect hazards appearing in front of a cyclist.

Next, publish a new version of the Lambda function we just modified. Go to the _Actions menu in the Lambda console \&gt; __Publish new version_. Call it &quot;Version 2&quot; in the description field and click _Publish__._

![](RackMultipart20200709-4-1s1c7lq_html_59efde9239647952.gif)

You will then need to create an Alias for the Lambda function. Aliases are a reference we can use when deploying our Lambda functions and acts as a placeholder, allowing us to decouple the Lambda version from the GreenGrass Group deployment, which helps minimize the changes to our Group configuration. Go to _Actions \&gt; Create Alias._ In the _Name_ field, enter the name &quot;PRODUCTION&quot; (or whatever name you will recognize). For the _Version_ field, choose the version of the Lambda you just created, in our case _version 2_ – **note you MUST use a specific Lambda version number and not the &quot;$LATEST&quot; option to work with GreenGrass**. Click _Create_ to save the new Alias.

![](RackMultipart20200709-4-1s1c7lq_html_4f9b6ec6778c7711.gif)

##### Deploy audio-service Lambda function

We will now create a new Lambda function that is responsible for playing audio alerts when hazards are detected. Go back to the Lambda home page and click on _Create function_.

![](RackMultipart20200709-4-1s1c7lq_html_94320cfc52a65168.gif)

On the Create function page, choose _Author from scratch_, then enter a _Function name_ such as &quot;audio-service&quot;. For the function _Runtime_, choose &quot;Python 2.7&quot;. Under _Permission \&gt; Choose_ or create an execution role, select _Use an existing role_, then find an _Existing role_ called &quot;AWSDeepLensLambdaRole&quot; and choose that option. Finally, click _Create Function_ at the bottom corner of the page.

Once you have created the function, you will be taken the Lambda configuration page. In the _Designer_ panel (click to expand this panel if necessary), click on the name of your function, for example &quot;audio-service&quot; in the center of the panel – this will expand the _Function code_ panel below.

![](RackMultipart20200709-4-1s1c7lq_html_b5558caf8554c8d4.gif)

Under _Function code \&gt; Code entry type_, choose the _Upload a .zip file_ option from the select menu. Then under _Function package_, click the _Upload_ button to launch a dialog window and selectSmartcyclev1/audio/audio-service.zip from your local drive.

For the Runtime field, make sure &quot;Python 2.7&quot; has been selected. For the Handler field, enter &quot;audio-service.lambda\_handler&quot; – this is the Python function that will be called in our audio-service.py Lambda function code when triggered.

![](RackMultipart20200709-4-1s1c7lq_html_f44e91c8e5dd4f2f.gif)

Next, _Save_ your changes for the audio-service Lambda function. Once saved, you need to publish your function so you can more easily manage any changes to the Lambda function made later. GreenGrass deployments require that you use a specific Lambda version – you cannot use an intrinsic reference such as &quot;$LATEST&quot;.

Go to the _Actions_ dropdown menu \&gt; _Publish new version_ option. For the _Version description_ field, enter &quot;Version 1&quot; in the text field and click _Publish_ to create the new version.

You will then need to create an Alias for the _audio-service_ Lambda function. Go to _Actions \&gt; Create Alias._ In the _Name_ field, enter the name &quot;PRODUCTION&quot; (or whatever name you will recognize). For the _Version_ field, choose the version of the Lambda you just created, in our case _version 1_ – **note you MUST use a specific Lambda version number and not the &quot;$LATEST&quot; option**. Click _Create_ to save the new Alias.

##### Deploy Smartcycle-audio Lambda function


You will add a GreenGrass topic Subscription that looks at only the &quot;smartcycle/object-detection&quot; messages published to the IoT Cloud. The smartcycle-audio Lambda function is triggered by incoming &quot;smartcycle-object-detection&quot; messages (the smartcycle-audio Lambda function does not use the triggering mechanism in the Lambda console per se). To configure the Subscription, follow these steps:

#### Modify the Default GreenGrass Project Configuration

The Object Detection project is deployed as an AWS IoT GreenGrass project to the DeepLens. You will now need to modify the default GreenGrass configuration to support the DeepLens hardware and local resource access required by the Smartcycle.The original Object Detection sample project is deployed as an AWS IoT GreenGrass project to the DeepLens. In the AWS Console, go to _IoT Core \&gt; Greengrass \&gt; Groups_. Find the Group that contains your DeepLens device name and select it.

You will now need to modify the default GreenGrass configuration to support the DeepLens hardware and local resource access required by the Smartcycle Lambda functions and Python scripts. You will first modify the Group&#39;s _Lambda_ functions, then the _Resources_, and then _Subscriptions_.

#####
 In the AWS Console, go to IoT Core \&gt; Greengrass \&gt; Groups. Find the Group that contains your DeepLens device name and select it. Then click on the &#39;Resources&#39; menu option. Resources give deployed Lambda functions the ability to access local resources that are physically present on the Greengrass core device. Repeat the steps below to create four GreenGrass resources Smartcycle requires.Modify audio-service Lambda for GreenGrass

First, you need to add our _audio-service_ Lambda function to the GreenGrass Group so you can assign Resources to it. In the GreenGrass Group you selected, click on the left hand &quot;_Lambdas_&quot; link, then click on &quot;_Add Lambda_&quot;. Note, that you should see two or more existing Lambda functions previously created when you registered you DeepLens and deployed the Object Detection sample project to it.

Next, click on _&quot;Use existing Lambda&quot;_ and choose the _audio-service_ Lambda you created in the earlier steps by clicking on its radio button. Choose the &quot;PRODUCTION&quot; alias as the Lambda version to use, then click Finish.

Once you are back on the Lambdas page, click on the _audio-service_ Lambda you just added, then _Edit._ Increase the _Memory limit_ setting to 32MB and increase the _Timeout_ setting to 15 seconds. Finally, Enable _Read access to the /sys directory_ by clicking the Enable radio button. Save your changes to the Lambda configuration by clicking the _Update_ button.

![](RackMultipart20200709-4-1s1c7lq_html_8b58acc16838cf7d.gif)

##### Modify the deeplens-object-detection Lambda for GreenGrass

Now go back to your GreenGrass Group&#39;s _Lambdas_ view and select the _deeplens-object-detection Lambda \&gt; Edit Configuration_ menu item.

Scroll the bottom of the configuration page and click _Add another version._ Choose the &quot;PRODUCTION&quot; alias you created earlier for the deeplens-object-detection Lambda function. Then, remove any previous Versions of the deeplens-object-detection Lambda that may exist (most likely version 1 or version 2).

Next, you need to change the Lambda settings.

- For the _Run as field, select the Another userID /group ID option_, then enter &quot;1000&quot; for the UID and &quot;1000&quot; for the GID.
- _Memory limit_ – increase to &quot;1536 MB&quot;
- Set _Timeout_ to &quot;2 seconds&quot;


- Set _Lambda lifecycle_ to the _&quot;Make this function long-lived and keep it running indefinitely&quot;_ option
- Set _Read access to /sys directory_ to the _&quot;Enable&quot;_ option

 Finally, click _Update_ to save your configuration settings.

 ![](RackMultipart20200709-4-1s1c7lq_html_32e1bf66a65d7009.gif)

##### Configure GreenGrass Group Resources

Next, you will give the Lambda functions smartcycle-audio and deeplens-objection-detection access to local resources on the DeepLens.

Go to your GreenGrass Group&#39;s _Resources_ menu option. You should see a number of existing resources already defined for you device. GreenGrass _Resources_ give deployed Lambda functions the ability to access local resources that are physically present on the Greengrass core device – in this case, your DeepLens.

Click on the _&quot;Add local resource&quot;_ button and enter the following configuration information.

, repeating the steps for each of the four Resources you need to create. Note that the device filesystem paths you reference for the Resources Source Path and Destination Path must already exist on the DeepLens device in order for the GreenGrass Group deployment step to be successful; you have already created the required filesystem paths when we cloned the Smartcycle project from GitHub on the DeepLens device earlier in these instructions (any pre-existing Resource paths have previously been created on the DeepLens as well).

Resource name: smartcycle\_audio\_files

Resource type: Volume

Source path:/home/aws\_cam/src/aws-smartcycle/audio/audio-files

Destination path:/home/aws\_cam/src/aws-smartcycle/audio/audio-files

Group owner file access permissions:select radio button for &quot;Automatically add OS group permissions of the Linux group that owns the resource&quot;

Lambda function affiliations:choose select the _&quot;smartcycle-audioaudio-service&quot;_ Lambda function, then the _Read and write access_ permission option.

![](RackMultipart20200709-4-1s1c7lq_html_a4af2e62b04d4cd8.gif) \&lt;insert screenshot here\&gt;

Resource name:diskcache\_dir

Resource type: Volume

Source path: /home/aws\_cam/src/aws-smartcycle/localdb

Destination path: /home/aws\_cam/src/aws-smartcycle/localdb

Group owner file access permissions: select radio button for &quot;Automatically add OS group permissions of the Linux group that owns the resource&quot;

Lambda function affiliations: choose BOTH &quot;deeplens-object-detection&quot; AND &quot;smartcycle-audio&quot; Lambda functions with &quot;Read-and-Write Access&quot;

\&lt;insert screenshot here\&gt;

![](RackMultipart20200709-4-1s1c7lq_html_a505dd676111e7f6.gif)

Resource name: sound\_card\_resource – this resource already exists as part of the default DeepLens setup. However, you need to Edit this resource and give the _audio-service_ and _deeplens-object-detection_ Lambdas access to this resource by creating affiliations for them. Leave all other settings as-is.

Resource type: Device

Device path: /dev/snd/pcmC0D0p

Group owner file access permissions: select radio button for &quot;Automatically add OS group permissions of the Linux group that owns the resource&quot;

Lambda function affiliations: _choose BOTH &quot;deeplens-object-detection&quot; AND &quot;smartcycle-audio&quot; Lambda functionsSelect another Lambda function to attach_, then choose the audio-service Lambda with Read and write access, save the resource settings by clicking Update at the bottom of the page.

![](RackMultipart20200709-4-1s1c7lq_html_dd1b6ad5a5149bf1.gif) \&lt;insert screenshot here\&gt;

Resource name: sound\_control\_resource – this resource already exists as part of the default DeepLens setup. However, you need to Edit this resource and give the _audio-service_ and deeplens-object-detection Lambdas access to this resource by creating affiliations for them. Leave all other settings as-is.

Resource type: Device

Device path: /dev/snd/controlC0

Group owner file access permissions: select radio button for &quot;Automatically add OS group permissions of the Linux group that owns the resource&quot;

Lambda function affiliations: _Select another Lambda function to attach_, then choose the audio-service Lambda with Read and write access, save the resource settings by clicking Update at the bottom of the page.choose BOTH &quot;deeplens-object-detection&quot; AND &quot;smartcycle-audio&quot; Lambda functions

![](RackMultipart20200709-4-1s1c7lq_html_b67dddc6a8afa962.gif)

**Finally, you will need to add your new version of the &quot;deeplens-object-detection&quot; Lambda to all other pre-existing Resources associated with this GreenGrass Group. Go into all remaining Resource configurations and add the &quot;PRODUCTION&quot; (alias) version of the &quot;deeplens-object-detection&quot; Lambda to the Resource – match the read/write permissions of the other Lambda functions already affiliated with that Resource, otherwise you may run into filesystem permission issues once deployed. You will have to repeat this process several times to correctly associate the new version of the deeplens-object-detection Lambda with each required Resource.**

##### Add GreenGrass Group Subscriptions

Subscriptions will allow our GreenGrass Lambda functions to communicate with each other through message passing. A Subscription consists of a source, target, and topic. The source is the originator of the message. The target is the destination of the message. The first step is selecting your source and target.

You will add a GreenGrass topic Subscription that looks at only the &quot;smartcycle/object-detection&quot; messages published to the IoT Cloud. The smartcycle-audio Lambda function is triggered by incoming &quot;smartcycle-object-detection&quot; messages. To configure the Subscription, follow these steps in your GreenGrass Group.

1. Go to the Subscriptions menu option in the GreenGrassGroup, the click the _Add Subscription_ button.
2. Under _Select a source,_ choose the _Services\&gt; IoT Cloud_ option_._
3. _Under Select a target_, choose _Lambdas \&gt; audio-service._ Then click the _Next_ button.
4. A Topic filter text field will appear, copy/paste in &quot;smartcycle/object-detection&quot; as the topic filter value, then click the _Next_ button.

![](RackMultipart20200709-4-1s1c7lq_html_37d8e7dd1e8fed19.gif)

#### Deploy Your GreenGrass Group Changes

For these changes to take effect, you need to re-deploy the GreenGrass project itself to your front DeepLens device. In your GreenGrass Group, go back to the _Deployments_ page, then choose _Actions \&gt; Deploy_. Deployments with either successfully complete or will have a status of failed. If the deployment failed, click on the failed deployment in the listing to be taken to the error description – drill into the detailed error message on that page.

###

### Test your Smartcycle deployment Download the Smartcycle Artifacts to the DeepLens Device

###

Once the Smartcycle deployment has been successful, you can now run the demo videos to test the hazard detection functionality provided by the deeplens-object-detection Lambda. If you have ANT+ sensors, you can also run the multi\_ant\_demo.py Python script to capture sensor data.

First, you need to download the demo videos (front and rear) to your local workstation or whatever computer you will be demoing from. You can download the videos from their Amazon S3 storage bucket here:

Front: https://aws-smartcycle1.s3.amazonaws.com/demo-front.mp4

Rear: https://aws-smartcycle1.s3.amazonaws.com/demo-back.mp4

### Note that each of these MP4 demo video files is approximately 720MB in size.You now need to download and configure the code artifacts required to run Smartcycle.

Next, log on to your DeepLens and start your ANT+ Python script from a Terminal prompt change into the &quot;sensors&quot; directory and run the following script:First, assuming you have a keyboard/mouse/monitor connected to your DeepLens, login to your DeepLens device to access your Ubuntu desktop. Then launch a Terminal shell prompt. Optionally, you may choose to connect to your DeepLens remotely over SSH instead.

~~Create a directory to clone the Smartcycle project artifacts to your user home directly on the DeepLens. Copy and run the following commands:~~

cd ~/smartcycle-aws/sensors

sudo python multi\_ant\_demo.py

Now it&#39;s time to display the processed video stream from the DeepLens. This video stream will be generated by the deeplens-object-detection Lambda and will show detected road hazards, sensor metrics such as heartrate, speed, temperature, etc. and will trigger audio alerts to play.

From a new Terminal prompt, run the following command:

mplayer -demuxer lavf –lavfdopts format=mjpeg:probesize=32 /tmp/results.mjpeg

### ~~cd ~; mkdir src; cd src~~

### From the &#39;src&#39; directory, clone the &#39;smartcycle&#39; project from GitHub; once the clone download completes, change into the &#39;smartcycle&#39; directory:

### git clone https://github.com/simcikdt/aws-smartcycle.git

cd ./aws-smartcycle; ll

### The ll command should show a directory contents similar to the following:
 \&lt;screenshot of smartcycle src directory here\&gt;

### Run the install-front.sh shell script to

###

### Next, you will need to overwrite the original Object Detection Lambda function deployed locally on the DeepLens via GreenGrass with the customized version from the Smartcycle project. Run the following commands to make a backup copy of the original .py file, then overwrite it with the version from the Smartcycle project source.

### \&lt;insert screenshot here\&gt;

A window will appear showing the processed video output directly on your DeepLens desktop. Start your demo video at this point. The object detection model works best when demo video monitor takes up the entire camera view. A successful test will render bounding boxes around hazards like stop signs and stop lights as the demo video progresses through the streets, you should see labels for your sensor data, and as each hazard is detected you should hear an audio alert play warning you about the specific hazard detected.

With respect to hardware setup, this is when you will need to have a spare monitor to play the front or rear demo videos, preferably mounted on some kind of stand. If you are not setting up the DeepLens on a bike, a screw-mount camera tripod can be used and is really helpful to keep the DeepLens pointing at the demo video. Be sure to have headphones or a speaker plugged into your front DeepLens and the volume turned up to a comfortable level so you can hear the audio alerts when a hazard is detected in the demo video. Remember that the objects detected differ between the front and rear DeepLens devices.

### Configuring the Rear-Facing DeepLens

Setting up your rear-facing DeepLens is much like setting up the front-facing DeepLens. Follow all of the same instructions listed above, except for the following:

- Wherever there was a reference to &quot;front-facing&quot; installation scripts, use the &quot;rear-facing&quot; version instead.

- Omit the steps required to create and configure the audio-service Lambda. All audio alert playback will occur through the front-facing DeepLens.
- Use the rear-facing version of the deeplens-object-detection custom lambda

###
\*Special thanks go to Johanne Bader and his excellent introduction to configuring the Suunto USB receiver for the Raspberry Pi, which helped greatly with the ANT+ sensor code.

[https://www.johannesbader.ch/2014/06/track-your-heartrate-on-raspberry-pi-with-ant/](https://www.johannesbader.ch/2014/06/track-your-heartrate-on-raspberry-pi-with-ant/)

###

 sudo systemctl restart greengrassdi


###

###

###

###

###

**Front DeepLens**

1. Deploy Object-detection Lambda project (deploy the Lambda artifact itself or the default project and then overwrite?....probably the latter case


2. Deploy smartcycle-audio lambda
  1. Create initial smartcycle-audio Lambda using deployment artifact in Lambda console
  2. GG Lambda settings (on-demand container)
    1. Subscription to smartcycle/object-detection topic to trigger smartcycle-audio lambda


3. Configure GG Resources
4. Deploy revised GG project to DeepLens


5. Deploy Analytics application

  1. See Sarita&#39;s document

1. While Logged into the DeepLens Ubuntu console
  1. Clone Git aws-smartcycle project locally
2. Run install-front.sh shell script to copy files for the FRONT DeepLens

    1. Copy/overwrite default object-detection Lambda (front) with custom version (that has sensor overlay and custom model references, etc.)Make sure references to audio files, new object-detection model, diskcache DB are correct
    2.
  1. Install required Python modules (diskache, audio-player) via Pip (global/standard device deployment)
  2. Make sure references to audio files, new object-detection model, diskcache DB are correct

1. Manually configure ANT+ USB settings (or can we automate this via the install.sh shell script?)

Start ant\_multi\_demopy

**Rear DeepLens**
