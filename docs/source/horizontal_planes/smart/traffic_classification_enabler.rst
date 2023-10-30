.. _Traffic classification enabler:

#############################
Traffic classification enabler
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
of an AI/ML framework and dedicated algorithms. The traffic classification 
enabler can be seen as a service of the application layer of the general SDN 
architecture.

***************
Features
***************
Two main features are supported by this enabler, especifically:

- Training a machine learning model to classify traffic packets, in, type or application.
- To inference the type of traffic of a specific packet/s passed via .pcap file.

To that end, the enabler will rely on Convolutional Neural Network (CNN) and RESNET models.


.. note:: 
   At this moment, the enabler has only been validated to work with CNN models. Code for Resnet has been added and tested, but not validated with real data. Additional modifications are expected (code cleaning, management of models via SemRepo enabler, average of results of .pcap file rather than packet-based).


*********************
Place in architecture
*********************
The VPN enabler is located in the Smart Network and Control plane of the ASSIST-IoT 
architecture. In particular, it will be one of the enablers devoted to improve
the performance of the network, in this case acting as an application that aids the SDN 
controller.

.. figure:: ./traffic_place.png
   :alt: Place of the Traffic Classification enabler within the Smart Network and Control Plance architecture
   :align: center
   
   Place of the Traffic Classification enabler within the Smart Network and Control Plance architecture


The enabler is composed of three main elements, as one can see in the figure below:

- **Traffic Classification API**: an API REST will act as a central proxy of the operations that are offered by the enabler. It is responsible of managing the API calls related to starting a training and an inference process. It also includes necessary calls for preparing data used for further training.
- **Training Module**: It will be invoked for training the DNN model and sub-models by the user, ideally when an extended or new dataset is available. In future releases, this component might be conditionally deployed (as nodes with low resources might not be suitable for training operations).
- **Classifier**: It will contain the functions in charge of executing the inference process, taking a trained model and a set of packet features as inputs.

.. figure:: ./traffic_arch.png
   :alt: Traffic Classification enabler architecture
   :align: center

   Traffic Classification enabler architecture

***************
User guide
***************

REST API endpoints
*******************
The following API endpoints have been developed:

+--------+------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------+-----------------------------------------------------------------------------------------------------------------------------+--------------------------------------------------+
| Method | Endpoint                     | Description                                                                                                                                            | Payload (if needed)                                                                                                         | Response format                                  |
+========+==============================+========================================================================================================================================================+=============================================================================================================================+==================================================+
| GET    | /version                     | Returns the version of the enabler.                                                                                                                    |                                                                                                                             | JSON with the output class                       |
+--------+------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------+-----------------------------------------------------------------------------------------------------------------------------+--------------------------------------------------+
| GET    | /health                      | Returns status of the enabler (it is considered healthy if its components are deployed and can be communicated).                                       |                                                                                                                             | JSON with the output class                       |
+--------+------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------+-----------------------------------------------------------------------------------------------------------------------------+--------------------------------------------------+
| get    | /v1/api-export               | Returns the openapi specifications of the enabler.                                                                                                     |                                                                                                                             | JSON with the output class                       |
+--------+------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------+-----------------------------------------------------------------------------------------------------------------------------+--------------------------------------------------+
| POST   | /v1/preprocess               | Given a set of .pcap files via volume (in ML_folder/data), these are prepared for further training.                                                    |                                                                                                                             | Successful or error code depending on the result |
+--------+------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------+-----------------------------------------------------------------------------------------------------------------------------+--------------------------------------------------+
| POST   | /v1/create_train_test_set    | Given a set of preprocessed files (in ML_folder/preprocessed), these are split in two sets for training and validation, and parcel files are prepared. |                                                                                                                             | Successful or error code depending on the result |
+--------+------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------+-----------------------------------------------------------------------------------------------------------------------------+--------------------------------------------------+
| POST   | /v1/train                    | Given a set of prepared files (in ML_folder/target), a training process is started. This may take a long time depending on the input data volume       | {“model_type”: “cnn”, “task”: “app”} Other options: "resnet" and "traffic", respectively.                                   | Successful or error code depending on the result |
+--------+------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------+-----------------------------------------------------------------------------------------------------------------------------+--------------------------------------------------+
| POST   | /v1/cnn_inference_app        | Returns the application of the packets of a .pcap file, considering a previously trained CNN model (present in ML_folder/model).                       |                                                                                                                             | JSON with inferenced application class/es        |
+--------+------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------+-----------------------------------------------------------------------------------------------------------------------------+--------------------------------------------------+
| POST   | /v1/cnn_inference_traffic    | Returns the traffic type of the packets of a .pcap file, considering a previously trained CNN model (present in ML_folder/model).                      |                                                                                                                             | JSON with inferenced traffic class/es            |
+--------+------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------+-----------------------------------------------------------------------------------------------------------------------------+--------------------------------------------------+
| POST   | /v1/resnet_inference_app     | Returns the application of the packets of a .pcap file, considering a previously trained resnet model (present in ML_folder/model).                    |                                                                                                                             | JSON with inferenced application class/es        |
+--------+------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------+-----------------------------------------------------------------------------------------------------------------------------+--------------------------------------------------+
| POST   | /v1/resnet_inference_traffic | Returns the traffic type of the packets of a .pcap file, considering a previously trained resnet model (present in ML_folder/model).                   |                                                                                                                             | JSON with inferenced traffic class/es            |
+--------+------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------+-----------------------------------------------------------------------------------------------------------------------------+--------------------------------------------------+

Currently, to classify a packet to get its class, a request has to be made to the IP address of the host and the corresponding port of the service (10000 by default). The request has to be accompanied by a body with the.pcap file with packets to classify. A request example for some of the above endpoints is attached below:

  .. code-block:: bash

        curl -F pcap_data=@email.pcap -X POST http://<IP_address>:10000/v1/cnn_inference_traffic 

***************
Prerequisites
***************
The current version works in a Docker environment with Docker Compose; or Kubernetes environment with Helm chart; or ASSIST-IoT environment managed by the Smart orchestrator. The two latter approaches are encouraged.

***************
Installation
***************
Enabler is provided as a Helm chart. Hence, it can be deployed with the manageability enablers (see 2.5.1) or directly via Helm install. Data and/or models are currently passed from a volume from the host's path (can be configured at *values.yaml*).

*********************
Configuration options
*********************
Only two configuration variables of the enabler can be configured right now. To set it
up, the chart's *values.yaml* manifest can be changed.

- **API_PORT**: Port where the Traffic Classification API is exposed.
- **ML_PORT**: Internal port for the traffic classification training and inference.

***************
Developer guide
***************
This code is expected to be executed within a Helm chart, in a Kubernetes-governed platform. It has been also tested with Docker compose and directly over Ubuntu x64 distributions, with and without GPU NVIDIA processors. In case that developers aims at using the code directly over a given Operating System, non-virtualized, the code has been tested only in Ubuntu 20.04 machines, and hence we do not grant that it will work in any other OS.

This code is open source and can be freely used by the innovation and research community. In case that commits are to be made, the mantainer team (UPV) holds the rights to accept or deny them. Best practices are encouraged in the latter case.

***************************
Version control and release
***************************
Version 1.0. 

***************
License
***************
Apache License 2.0.

This work builds upon the research presented in Lotfollahi, M., Jafari Siavoshani, M., Shirali Hossein Zade, R. et al. Deep packet: a novel approach for encrypted traffic classification using deep learning. Soft Comput 24, 1999–2012 (2020). https://doi.org/10.1007/s00500-019-04030-2
It also extends the work done in: https://blog.munhou.com/2020/04/05/Pytorch-Implementation-of-Deep-Packet-A-Novel-Approach-For-Encrypted-Tra%EF%AC%83c-Classi%EF%AC%81cation-Using-Deep-Learning/

*********************
Notice (dependencies)
*********************
ASSIST-IoT - Architecture for Scalable, Self-*, human-centric, Intelligent, Se-cure, and Tactile next generation IoT

This project has received funding from the European Union's Horizon 2020
research and innovation programme under grant agreement No 957258.

Traffic classification enabler
Copyright 2020-2023 Universitat Politècnica de València

I. Included Software
-	Deep-Packet (https://github.com/munhouiani/Deep-Packet), MIT license 

II. Used Software

-	colorama 0.4.4 (https://github.com/tartley/colorama/tree/0.4.4), BSD-3-Clause license
-	joblib (https://github.com/joblib/joblib), BSD-3-Clause license
-	Flask 2.0.2 (https://github.com/pallets/flask/tree/2.0.x), BSD-3-Clause li-cense
-	itsdangerous 2.0.1 (https://github.com/pallets/itsdangerous/tree/2.0.1) BSD-3-Clause license
-	Jinja2 3.0.3 (https://github.com/pallets/jinja/tree/3.0.3), BSD-3-Clause license
-	MarkupSafe 2.0.1 (https://github.com/pallets/markupsafe/tree/2.0.1), BSD-3-Clause license
-	Werkzeug 2.0.2 (https://github.com/pallets/werkzeug/tree/2.0.x), BSD-3-Clause license
-	Gunicorn 20.1.0 (https://github.com/benoitc/gunicorn/tree/20.x), custom li-cense (see list below)
-	Requests 2.27.1 (https://github.com/psf/requests/tree/v2.27.x), Apache-2.0 license
-	flask_wtf 1.0.0 (https://github.com/wtforms/flask-wtf/tree/1.0.x), BSD-3-Clause license
-	peewee 3.14.10 (https://github.com/coleifer/peewee/tree/3.14.10), MIT license
-	wtforms (https://github.com/wtforms/wtforms), BSD-3-Clause license
-	pymysql (https://github.com/PyMySQL/PyMySQL), MIT license
-	click 8.1.3 (https://github.com/pallets/click/tree/8.1.x), BSD-3-Clause li-cense
-	jupyterlab 3.4.7 (https://jupyter.org/governance/projectlicense.html), BSD-3-Clause license
-	matplotlib 3.5.3 (https://matplotlib.org/stable/users/project/license.html), custom license (PSF-based, see list below)
-	datasets 2.5.1 (https://github.com/huggingface/datasets/tree/2.5.1), Apache-2.0 license
-	pandas 1.4.4 (https://github.com/pandas-dev/pandas/tree/1.4.x), BSD-3-Clause license
-	plotly 5.10.0 (https://github.com/plotly/plotly.py/tree/v5.10.0), MIT li-cense
-	pyspark 3.3.0 (https://github.com/apache/spark/tree/master/python/pyspark), Apache-2.0 license
-	pytorch-lightning 1.7.7 (https://github.com/Lightning-AI/lightning/tree/1.7.7), Apache-2.0 license
-	scapy[complete] 2.5.0rc1 (https://github.com/secdev/scapy/tree/v2.5.0rc1), GPL-2.0 license
-	scikit-learn 1.1.2 (https://github.com/scikit-learn/scikit-learn/tree/1.1.X), BSD-3-Clause license
-	seaborn 0.11.2 (https://github.com/mwaskom/seaborn/tree/v0.11.2), BSD-3-Clause li-cense
-	tensorboard 2.10.0 (https://github.com/tensorflow/tensorboard/tree/2.10), Apache-2.0 license

III. List of licenses
-	BSD-3-Clause license
-	Gunicorn license
-	Apache-2.0 license
-	MIT license
-	matplotlib license
-	GPL-2.0 license
