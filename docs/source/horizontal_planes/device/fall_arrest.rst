.. _fall_arrest:

##################
Fall Arrest Device
##################

.. contents::
  :local:
  :depth: 1

************
Introduction
************
The ASSIST-IoT fall arrest device is a localisation tag with an Inertial Measurement Unit (IMU) and a push button. The push button is used by the person wearing the tag, to indicate that this person is in an emergency situation and needs immediate help. The fall arrest device uses the IMU to determine if the person has fallen or not. If an emergency situation is detected, a message is transmitted to the anchors immediately. An enabler can pick up this message and act accordingly.

********
Features
********
Localisation accuracy is better than 50cm.

*********************
Place in architecture
*********************
The fall arrest device is part of the device and edge plane.

**********
User guide
**********
The battery of the fall arrest device has to be charged during non-working hours.
The monitored assets needs to have a tag attached (e.g., in case of a worker, he/she has to wear a belt or helmet with it).
Information about the correspondence between tag and asset must be noted, so they can be later on related. In case of a worker, information about whether it is connected to a belt or helmet should be noted as well.

*************
Prerequisites
*************
The localization processing enabler need to know which person is wearing which fall arrest device.

************
Installation
************
The fall arrest device has to be mounted to a belt or to a helmet.

*********************
Configuration options
*********************
N/A

***************
Developer guide
***************
N/A

***************************
Version control and release
***************************
To be determined.

*******
License
*******
N/A

********************
Notice(dependencies)
********************
N/A
