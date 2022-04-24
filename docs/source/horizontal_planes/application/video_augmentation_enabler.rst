.. _Video augmentation enabler:

############
Video augmentation enabler
############

.. contents::
  :local:
  :depth: 1

***************
Introduction
***************
This enabler receives images or video captured either from ASSIST-IoT Edge nodes, or from ASSIST-IoT databases, and by means of Machine Learning Computer Vision functionalities, it provides object detection/recognition of particular end-user assets (e.g., cargo containers, cars’ damages). 

  **Note:** It should be noticed that to carry out the proper object recognition in operation, an appropriate annotated dataset should be ready and available for training and testing. 

***************
Features
***************
The following figure presents the architectural diagram of video augmentation enabler and inside components:

.. figure:: ./VA_Architecture.png
   :alt: Video Augmentation enabler
   
As it can be seen the Video Augmentation enabler is divided in 4 main components:

- **API:** The entrance gate to the video augmentation enabler. It provides a set of restful API endpoints, over which the user can easily interact with the enabler to e.g., run an ML training process, run an ML inference, or get the status of the current training process.
- **Data Pre-processor:** Since the dataset can be collected from various sources such as a Cameras or Databases, but it may not be used directly for performing ML analysis processes (e.g., the dataset contains unorganized or noisy data), a data pre-processing can be done. Data pre-processor provides tools for cleaning the raw data such as taking care of missing values, categorical features, and normalization.
- **ML trainer:** An ML model is a function with learnable parameters that maps an input to a desired output. The optimal parameters are obtained by training the model on data. ML Trainer will carry out the process of feeding the network with millions of training data points so that it systematically adjusts the knobs close to the correct values. Although the video augmentation ML trainer already support some ML models, additional ML models can be retrieved from the FL Repository. Since the training process of images/videos may be computationally intensive, because the data can be passed through Neural Network with several training rounds, it is recommended to have a dedicated GPU installed on the equipment in charge of performing the training.
- **Inference engine:** The Inference engine provides the process of running a trained ML over a specific input through an interpreter. The interpreter, based on TensorFlow, is designed to be lean and fast, and uses a static graph ordering and a custom (less-dynamic) memory allocator to ensure minimal load, initialization, and execution latency

The technologies that have been used for those components are:

- `FastAPI <https://fastapi.tiangolo.com/>`__: A modern, fast (high-performance), web framework for building APIs with Python 3.6+ based on standard Python type hints.

- `Tensorflow <https://github.com/tensorflow/tensorflow>`__: An end-to-end open source platform for machine learning

- `OpenCV <https://github.com/opencv/opencv>`__:  Provides a real-time optimized Computer Vision library, tools, and hardware


*********************
Place in architecture
*********************
Video Augmentation enabler is located in the Application and Service layer of the ASSIST-IoT architecture. As the rest of enablers of this horizontal plane, it is designed for for providing data visualisation and user interaction services, with a particular focus on smart object recognition capabilities.

***************
User guide
***************

REST API endpoints
***************

The currently supported REST API endpoints are listed below:

+---------+-----------------------+--------------------------------------------------------------------------------------------------------------------------+------------------------+------------------+
| Method  | Endpoint              | Description                                                                                                              | Payload (if needed)    | Response format  |
+=========+=======================+==========================================================================================================================+========================+==================+
| POST    | /train                | Executes a training session over the annotated data in the Video Augmentation data folder with the ML model {model_id}.  | {model_id}             |                  |
+---------+-----------------------+--------------------------------------------------------------------------------------------------------------------------+------------------------+------------------+
| GET     | /train_status         | Provides the status of the currently training model                                                                      |                        |                  |
+---------+-----------------------+--------------------------------------------------------------------------------------------------------------------------+------------------------+------------------+
| POST    | /inference_local      | Performs inference or validate process over the stored data (video or image) with the trained model model_id.            | {model_id}             |                  |
+---------+-----------------------+--------------------------------------------------------------------------------------------------------------------------+------------------------+------------------+
| POST    | /inference_streaming  | Performs inference or validate process over the video being streamed at IP_address with the trained model model_id.      | {ip_address,model_id}  |                  |
+---------+-----------------------+--------------------------------------------------------------------------------------------------------------------------+------------------------+------------------+

***************
Prerequisites
***************

***************
Installation
***************

*********************
Configuration options
*********************

***************
Developer guide
***************

***************************
Version control and release
***************************

***************
License
***************

Apache License Version 2.0

********************
Notice(dependencies)
********************
