.. _FL Local Operations enabler:

###########################
FL Local Operations enabler
###########################

.. contents::
  :local:
  :depth: 1

[[*TOC*]]

Introduction
============

One of key goals of FL is to assure protection of privacy of data, owned
by individual stakeholders. Therefore, data is expected to be used only
locally, to train local version of the shared model, and only parameters
update proposals of the ML algorithm are shared with others. When the FL
training process has concluded, the final shared ML model is used to
deliver specific functionality, also called inference engine. Both
operations (model training and model inference) involve access to
private data. This means that it is crucial to “encapsulate” local
processes within a single “node” (that is controlled by data owner).
However, it should be noticed that the data that is being used in both
FL training processes has to be in the same format, which is imposed by
the ML model that is being employed. In order to carry out with all
these local operations, the FL Local Operation enabler is proposed. It
will consist of components: Local Data Transformer component (that will
be in charge of guaranteeing that data is appropriately formatted for
the FL model in use), Local Model Training component, Local Model
Inference component, Communication component (to enable in and out
communications between involved local parties and FL orchestrator and FL
collector), Privacy Component (to provide privacy mechanisms for
communication e.g. encryption).

Features
========

-  Enabler embedded in each FL involved party performing local training.
-  Verification of local data formats compatibility with data formats
   required by FL.
-  Transformation of local data formats to format required by the ML
   system (possibly using predefined transformers).
-  The local results will be sent to the FL Training Collector in order
   to carry out the appropriate aggregation methodology over the common
   shared model.
-  Inference with the final shared ML model.
-  Communication of model updates via encryption mechanisms. A
   homomorphic encryptor will not permit outsiders to see the output
   model of each device/party (MITM attacks), whereas methods for
   creating differentially private noise will guarantee that Malicious
   Aggregator cannot be allowed to infer which records are actual models
   and which not.

Place in architecture
=====================

FL Local Operations enabler is one of the Federated Learning enablers
that together enable to deploy a federated learning environment.
Functionally, it operates on scalability and manageability verticals in
the Assist-IoT architecture.

User guide
==========

Interactions with this enabler are done through a REST API. In the FL
environment the FL Orchestrator enabler sends appropriate configuration
to FL Local Operations that later on communicate with FL Training
Collector and FL Repository if required.

The enabler exposes REST API (see endpoints below) to communicate with
external enablers/applications but also uses gRPC to communicate with FL
Training Collector during model trainings.

+-----------------+----------------------+-----------------------------+
| Method          | Endpoint             | Description                 |
+=================+======================+=============================+
| POST            | /job/config/{id}     | Receive configuration for a |
|                 |                      | training job                |
+-----------------+----------------------+-----------------------------+
| PUT             | /model/{id}/{version | Receive a new shared model  |
|                 | }                    |                             |
+-----------------+----------------------+-----------------------------+
| GET             | /status              | Get current status of the   |
|                 |                      | enabler                     |
+-----------------+----------------------+-----------------------------+
| POST            | /job/transformer/{id | Receive any required data   |
|                 | }                    | transformer for job with    |
|                 |                      | identifier id               |
+-----------------+----------------------+-----------------------------+
| POST            | /predict/model/{id}/ | Inference with model        |
|                 | {version}            |                             |
+-----------------+----------------------+-----------------------------+

Prerequisites
=============

If run from source code then required libraries are in the file
requirement.txt. If run in a container there are no prerequisites.

Installation
============

The installation procedure for this enabler is under development.

Configuration options
=====================

The configuration of the training process for the FL Local Operations
enabler is done with a request to REST API where the following
parameters for a training job to be executed can be set:

-  client_type_id - type of client indicating what mechanisms are used
   in it, e.g. “keras1”
-  server_address - address of FL Training Collector,
   e.g. “training_collector”
-  optimizer - name of the optimized to be used, e.g. “adam”
-  eval_metrics - list of evaluation metrics, e.g. [“MSE”]
-  eval_func - evaluation function, e.g. “Huber”
-  num_classes - number of classes, e.g. “10”
-  model_id - model identifier, e.g. “10”
-  model_version - model version, e.g. “10”
-  shape - shape of the data, e.g. [“32”, “32”, “3”]
-  config_id - identifier of the configuration to be used
-  batch_size - size of a batch, e.g. “64”
-  steps_per_epoch - number of steps in each epoch, e.g. “32”
-  epochs - number of epochs, e.g. “5”
-  learning_rate - tuning parameter in an optimization algorithm,
   e.g. “0.001”

Developer guide
===============

Components
----------

Local model trainer
~~~~~~~~~~~~~~~~~~~

The Local Model Training component is responsible for local model
training. During configuration it instantiates appropriate ML training
libraries and, if this is the beginning of the process, initial version
of the shared model. This step can be completed locally by the node
owner, but this is unlikely. The main problem would be assuring
uniformity of training methods across nodes belonging to different
owner. More likely, the necessary modules (ML algorithm libraries and
the initial version of the shared model) will be downloaded from the FL
Repository.

Local model inferencer
~~~~~~~~~~~~~~~~~~~~~~

The component is responsible for use of the trained model. Here, the
model may be used: (1) after the FL process is completed, or (2) it may
start to be used from a certain (predefined by the owner) level of
quality of the shared model. In the latter case, each new version of the
shared model would replace the previous one. Obviously, it is implicitly
assumed that each new version of the shared global model will deliver
better quality of results. Here, data to be fed into the trained model
can be transformed using the Data Transformer component. Interpretation
of the results of application of the model to specific input data
(including actions to be, possibly, undertaken on the basis of the
results) is likely to be provided by the data owner. However, it is also
possible that appropriate module is going to be downloaded from the FL
Repository.

Local communication
~~~~~~~~~~~~~~~~~~~

Responsible for communication between external entities and the enabler.

Data transformer
~~~~~~~~~~~~~~~~

In IoT ecosystems, each partner may (and is likely to) store data in its
own (private/local) format. Use of FL requires transformation of
appropriate parts of local data into the correct format. This format has
to be described as part of the FL configuration, and all participating
nodes have to oblige. This may be achieved by node owner providing
appropriate transformation component. However, such component can be
envisioned as being downloaded from the FL Repository enabler.

Privacy
~~~~~~~

TBD

Technologies
------------

scikit-learn
~~~~~~~~~~~~

A popular machine learning library often used for data preprocessing and
transformation, for example encoding labels. It is open source and
widely used in the industry.

pyTorch
~~~~~~~

An open source machine learning framework based on
the Torch library, used for applications such as computer
vision and natural language processing, primarily developed
by Facebook’s AI Research lab (FAIR).

Python
~~~~~~

Python is an interpreted high-level general-purpose programming language
with a set of libraries. Very popular for data analysis and ML
applications.

TensorFlow
~~~~~~~~~~

A free and open-source software library for machine
learning and artificial intelligence. It can be used across a range of
tasks but has a particular focus on training and inference of deep
neural networks.

Flower
~~~~~~

A federated learning framework designed to work with a large number of
clients. It is both compatible with a variety of ML frameworks and
supports a wide range of devices.

OpenVINO
~~~~~~~~

A free toolkit facilitating the optimization of a deep learning model.
It is cross-platform and free to use.

OpenCV
~~~~~~

A real-time computer vision library providing already optimized models.
It is cross-platform and open-source.

Pailier Encryption, Affine Homomorphic Encryption
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Two homomorphic encryption algorithms that will be used to preserve the
privacy of the data without affecting the performance of the model.
Component: Privacy

FastAPI
~~~~~~~

A popular web microframework written in Python, FastAPI is known for
being both robust and high performing. It is based on OpenAPI
(previously Swagger) standards.

Version control and release
===========================

TBD

Licence
=======

The FL Local Operations is licensed under the **Apache License,
Version2.0** (the “License”).

You may obtain a copy of the License at:
http://www.apache.org/licenses/LICENSE-2.0

Notice (dependencies)
=====================

Dependency list and licensing information will be provided before the
first major release.



