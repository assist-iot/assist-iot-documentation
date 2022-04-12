.. _Resource provisioning enabler:

#############################
Resource provisioning enabler
#############################

.. contents::
  :local:
  :depth: 1

***************
Introduction
***************
This enabler will be able to horizontally scale (up or down) the resources devoted to a specific enabler (inside a node) in a dynamic fashion, based on time series inference and custom logic.

***************
Features
***************
Resource provisioning enabler shall store time series with the usage metrics of the components of each active enabler in the host cluster. Deep learning techniques based on time series models are used to predict usage metrics and horizontally scale the resources dedicated to each enabler component. The software will be self-contained and will act accordingly to the dynamic behaviour of each enabler.

*********************
Place in architecture
*********************
When the administrator user enables the resources provisioning controller enabler it automatically starts working. It accesses the metrics and stores them in its internal database, performs the deep learning process and infers to create the horizontal objects pod autoscalers dynamically. All this with pre-set values in the initial configuration.

.. image:: https://user-images.githubusercontent.com/100677511/162429686-7cd012c0-bd74-441b-a12d-0d7a4aae9d6a.png

- **API REST**: Contains the logic necessary to make GET and POST calls to intervene with the system behaviour, change default values or collect information.
- **Pod Resources Controller**: Performs the collection of metrics and is responsible for storing the values in 15-minute intervals.
- **History Database**: Contains the metrics history database needed to aggregate the deep learning process.
- **Training module**: Collects the raw data from the history databases and converts it to the format needed for the deep learning process. Executes the data predictions and stores them in a new database.
- **Future Database**: Contains the predicted data database of all components of each active enabler.
- **Inference module**: Adds logic to the data in the future database and generates the inference process. Creates or replaces the horizontal pod autoscaler objects. Changes the previous values to the new ones based on the results obtained.

***************
User guide
***************
The enabler has a management API that provides a flash-based REST interface that can be interacted with to configure certain values. The url must include not only the address of the enabler, but also the action to be performed and the message body if necessary. The response shall include the requested information or the result of the execution of a command.

+--------+------------------------------------------------------------------+----------------------------+---------------------------------------------+----------------------------------------------------------------------------------------------------------------------+
| Method |             Endpoint                                             | Description                | Payload (if needed)                         | Response format                                                                                                      |
+========+==================================================================+============================+=============================================+======================================================================================================================+
|  GET   | /enablers                                                        | Return enablers            |                                             | [{"components": ["comp1"],"enabler": "en1"}, {"components": ["comp1","comp2","comp3","comp4"],"enabler": "en2"}]     |
+--------+------------------------------------------------------------------+----------------------------+---------------------------------------------+----------------------------------------------------------------------------------------------------------------------+
|  GET   | /train                                                           | Execute the train          |                                             | ["Train module executed successfully","Error in execution Train module"]                                             |
+--------+------------------------------------------------------------------+----------------------------+---------------------------------------------+----------------------------------------------------------------------------------------------------------------------+
|  GET   | /train-values                                                    | Return train-values        |                                             | {"Future_data": "2","History_data": "7"}                                                                             |
+--------+------------------------------------------------------------------+----------------------------+---------------------------------------------+----------------------------------------------------------------------------------------------------------------------+
|  POST  | /train-values                                                    | Change train-values        | {"Future_data": "2","History_data": "7"}    | ["Train values changed","Content-Type not supported!","Error in json body","Values must be positive numbers"]        |
+--------+------------------------------------------------------------------+----------------------------+---------------------------------------------+----------------------------------------------------------------------------------------------------------------------+
|  GET   | /inference/<enabler>/<component>                                 | Execute the inference      |                                             | ["Infence complete sucessfully","Error in execution Inference Module"]                                               |
+--------+------------------------------------------------------------------+----------------------------+---------------------------------------------+----------------------------------------------------------------------------------------------------------------------+
|  POST  | /inference/<enabler>/<component>                                 | Select components to infer | {"components": ["comp1"],"enabler": "en1"}  | ["Enablers and components add to infer","Content-Type not supported!","Error in json body"]                          |
+--------+------------------------------------------------------------------+----------------------------+---------------------------------------------+----------------------------------------------------------------------------------------------------------------------+

***************
Prerequisites
***************
The enabler is prepared to work in a K8S environment. The creation is prepared to be autonomous in such a working environment.
It will be necessary to activate the metrics collection plug-ins.
Other enablers must exist and be active and have their labels and CPU and memory resources correctly set.

***************
Installation
***************
Enabler is provided as a Helm chart. Refer to specific deployment instructions.

*********************
Configuration options
*********************
TBD

***************
Developer guide
***************
TBD

***************************
Version control and release
***************************
Version 0.1. Under development.

***************
License
***************
TBD

********************
Notice(dependencies)
********************
TBD