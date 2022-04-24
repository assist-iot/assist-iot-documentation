.. _Monitoring and Notifying enabler:

################################
Monitoring and Notifying enabler
################################

.. contents::
  :local:
  :depth: 1

***************
Introduction
***************
This enabler could be viewed as a general purpose by representing it as a combination of high-level monitoring module (which would allow to monitor devices, logs, etc.) and notifying module that could send custom messages to predefined system components.

***************
Features
***************
The monitoring and notifying enabler has the following functionalities:

- Monitor the uninterrupted functionality of edge devices
- Create a notification when an unexpexted incident occurs
- Common interfaces for quering log-data and notifications

*********************
Place in architecture
*********************

The monitoring and notifying enabler is part of the vertical plane enablers Self-*. It is directly connected to the Edge Data Broker Enabler by subscribing to its topics.


***************
User guide
***************

The user guide will be determined after the release of the enabler.

***************
Prerequisites
***************

**Apache Kafka**

Kafka provides a standardized method to enable a diverse set of technologies to communicate and interact. It is used to build real-time streaming data pipelines and real-time streaming applications which will be very useful in the IoT environment of the project.

**Java 8**

Java is a low complexity programming language and since Kafka is written in Java, it is one of the best choices for the enabler.  

**MQTT**

MQTT is a lightweight publish/subscribe messaging protocol and it is widely used l in IoT solutions. Since Edge Data Broker Enabler will use this protocol, it is under consideration to be used for easier integration.

***************
Installation
***************

The installation procedure is under development.

*********************
Configuration options
*********************

Additional configurations will be provided after the release of the enabler. The present configurations are listed below:

- BootstrapServers: Broker address:port to connect, eg. "localhost:9092"

- groupId: Group of devices the consumer belongs to, eg. "TemepratureSensors"

- topic: Topic to subscribe, eg. "device1", "device2"..

- threshold: Define the threshold value to rpoduce notifications, eg. "20"

***************
Developer guide
***************

The monitoring and notifying enabler is build on Apache Kafka, written in Java 8, using the maven repository infrastructure. The logs are stored in MongoDB.

***************************
Version control and release
***************************

Gitlab will be used as version control and release tool.

***************
License
***************

Licensing information will be provided after the release of the enabler.

********************
Notice(dependencies)
********************

Dependenies list information will be provided after the release of the enabler.
