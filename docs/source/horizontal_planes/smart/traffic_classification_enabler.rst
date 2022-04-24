.. _Trafic classification enabler:

#############################
Trafic classification enabler
#############################

.. contents::
  :local:
  :depth: 1

***************
Introduction
***************
In SDN-enabled networks, a controller is responsible for controlling the underlying switches that distribute traffic according to different rules, including 
sources/sinks, ports and type of traffic. The aim of this enabler is aid the 
controller to classify network traffic into a number of application classes 
(video streaming, VoIP, Network control, best effort, OAM, etc.), making use 
of an AI/ML framework and dedicated algo-rithms. The traffic classification 
enabler can be seen as a service of the application layer of the general SDN 
architecture.

***************
Features
***************
Two main features are supported by this enabler, especifically:

- Training a machine learning model to classify traffic packets, based on the combination of different algorithms.
- To inference the type of traffic of a specific packet based on different packet parameters.

To that end, the enabler will rely on a Deep Neural Network (DNN) which combines 
the outputs of three models, hence being a "meta-model". The underlying classifers
are based on K-Nearest Neighbours (KNN), Random Forest (RF), and Decision Tree 
(DT) algorithms.


.. note:: 
  At this moment, only the expossed API only works for classifying a packet, not for (re)training the model.


*********************
Place in architecture
*********************
The VPN enabler is located in the Smart Network and Control plane of the ASSIST-IoT 
architecture. In particular, it will be one of the enablers devoted to improve
the performance of the network, in this case acting as an application that aids the SDN 
controller.

.. figure:: ./traffic_place.PNG
   :alt: Place of the Traffic Classification enabler within the Smart Network and Control Plance architecture
   :align: center
   
   Place of the Traffic Classification enabler within the Smart Network and Control Plance architecture


The enabler is composed of three main elements, as one can see in the figure below:

- **Traffic Classification API**: an API REST will act as a central proxy of the operations that are offered by the enabler. It is responsible of managing the API calls related to starting an inference (i.e., traffic classification) process and retrain the AI model with new data. 
- **Training Module**: It will be invoked for training the DNN model and sub-models by the user, ideally when an extended or new dataset is available.
- **Classifier**: It will contain the functions in charge of executing the inference process, taking a trained model and a set of packet features as inputs.

.. figure:: ./traffic_arch.PNG
   :alt: Traffic Classification enabler architecture
   :align: center

   Traffic Classification enabler architecture

***************
User guide
***************

REST API endpoints
*******************
The API has not been finalised yet, in the following table are presented the endpoints
that will be implemented.

+--------+------------+------------------------------------------------------------------------------------------------------------+--------------------------------------------------+-----------------+
| Method | Endpoint   | Description                                                                                                | Payload (if needed)                              | Response format |
+========+============+============================================================================================================+==================================================+=================+
| POST   | /training  | Get information of the WireGuard network interface                                                         | Successful or error code depending on the result |                 |
+--------+------------+------------------------------------------------------------------------------------------------------------+--------------------------------------------------+-----------------+
| POST   | /inference | Returns the class of a specific packet, based on the inputs received and the application of the DNN model. | JSON with the output class                       |                 |
+--------+------------+------------------------------------------------------------------------------------------------------------+--------------------------------------------------+-----------------+

Currently, to classify a packet to get its class, a request has to be made to the 
IP address of the host and the corresponding port of the service (4000 by default).
The request has to be accompanied by a body with a set of parameters belonging to
the packet to be classified (extracted from .pcap files). A request example is attached 
below (e.g., *protocol = 1* corresponds to ICMP protocol):

  .. code-block:: bash

        curl --location --request POST 'http://<IP_address>:<api_port>/v1' -d
        {
          "protocol": "1",
          "src_port": "0",
          "dst_port": "0",
          "src2dst_packets": "16",
          "src2dst_bytes": "5332",
          "dst2src_packets": "8",
          "dst2src_bytes": "612"
        }

The request for performing the request has not been implemented yet.

***************
Prerequisites
***************
The current version works in a Docker environment with Docker Compose, they must be installed previously.

***************
Installation
***************
Any Helm chart nor dedicated K8s manifest has been developed yet. Two steps are needed
before using the enabler:

1. Build the docker image: ``docker build -t networkclassifier .``
   
2. Run the docker container: ``docker run -p 4000:4000 -d networkclassifier``

*********************
Configuration options
*********************
Only one configuration variable of the enabler can be configured right now. To set it
up, the Docker compose file has to be modified manually. In the future, this variable
will be managed by Helm's *values.yaml* manifest.

- **API_PORT**: Port where the Traffic Classification API is exposed.

***************
Developer guide
***************
Not Applicable.

***************************
Version control and release
***************************
Version 0.1. A major release has not been released yet as some key functionalities are missing
and it is not ready for being deployed in K8s environments.

***************
License
***************
Apache License 2.0.

This work is extends the research presented in P.K. Mondal *et.al*, "A dynamic network traffic classifier using supervised ML for a Docker-based SDN network", 2021, Connection Science, 1-26.

*********************
Notice (dependencies)
*********************
This enabler does not depend on any other. However, it provides an additional 
functionality for the SDN Controller, being interesting to be deployed together
(integration between them still pending).