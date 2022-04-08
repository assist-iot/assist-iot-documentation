.. _FL Training Collector enabler:

#############################
FL Training Collector enabler
#############################

.. contents::
  :local:
  :depth: 1

[[*TOC*]]

Introduction
============

The FL training process involves several independent parties that
commonly collaborate in order to provide an enhanced ML model. In this
process, the different local updates suggestions shall be aggregated
accordingly. This duty within ASSIST-IoT will be tackled by the FL
Training Collector, which will also be in charge of delivering back the
updated model.

Features
========

-  Aggregate local updates of the ML model prepared by independent
   parties as part of a model enhancement process. Responsible
   components: FLTC Combiner, FLTC I/O.

-  Delivering back to the parties the updated model. Responsible
   component: FLTC I/O.

Place in architecture
=====================

FL Training Collector enabler is one of the Federated Learning enablers
that together enable to deploy a federated learning environment.
Functionally, it operates on scalability and manageability verticals in
the Assist-IoT architecture.

User guide
==========

Interactions with this enabler are done through a REST API. In the FL
environment the FL Orchestrator enabler sends appropriate configuration
to FL Training Collector.

The enabler exposes REST API (see endpoints below) to communicate with
external enablers/applications but also uses gRPC to communicate with FL
Local Operations during model trainings.

+-----------------+----------------------+-----------------------------+
| Method          | Endpoint             | Description                 |
+=================+======================+=============================+
| POST            | /job/config/{id}     | Receive configuration of FL |
|                 |                      | Training Collector          |
|                 |                      | components for job with     |
|                 |                      | identifier id               |
+-----------------+----------------------+-----------------------------+
| GET             | /job/status/{id}     | Retrieve status of the      |
|                 |                      | training process with       |
|                 |                      | identifier id               |
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

The configuration of the training process for the FL Training Collector
enabler is done with a request to REST API where the following
parameters for a training job to be executed can be set:

-  strategy - name of the strategy to be used in this training job,
   e.g. “avg”
-  model_id - model identifier
-  num_rounds - number of rounds, e.g. “3”
-  min_fit_clients - minimum number of fitting clients, e.g. “1”
-  min_available_clients - minimum number of available clients, e.g. “1”
-  adapt_config e.g. “custom”
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

FLTC I/O
~~~~~~~~

Provides a REST API to allow the input and output communication to and
from the FL Training Collector enabler. On the one hand it is
responsible of receiving FL local updates that are sent to the FLC
Combiner component. On the other hand, it is responsible of
communicating updates of the new FL model obtained in the FLC Component
to the FL Repository. The communication capabilities of this component
are designed so that it can conceptually deal with situations in which
more complex topologies are used.

FLTC Combiner
~~~~~~~~~~~~~

This component will receive “suggestions” from a certain number
(possibly all) local nodes and combine them to generate an updated FL
model. It can include both homogeneous and heterogeneous FedAvg
solutions for e.g., logistic regression models, decision-tree models, or
even neural network models.

Technologies
------------

FedML
~~~~~

Research library and benchmark for Federated ML containing federated
algorithms and optimizers.

Python
~~~~~~

Python is an interpreted high-level general-purpose programming language
with a set of libraries. Very popular for data analysis and ML
applications.

FastAPI
~~~~~~~

A popular web microframework written in Python, FastAPI is known for
being both robust and high performing. It is based on OpenAPI
(previously Swagger) standards.

Flower
~~~~~~

A federated learning framework designed to work with a large number of
clients. It is both compatible with a variety of ML frameworks and
supports a wide range of devices.

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



