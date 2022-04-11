.. _FL Repository enabler:

#####################
FL Repository enabler
#####################

.. contents::
  :local:
  :depth: 1

[[*TOC*]]

Introduction
============

The FL repository is a set of different databases, including initial ML
algorithms, already trained ML models suitable for specific data sets
and formats, averaging approaches, and auxiliary repositories for other
additional functionalities that may be needed, and are not specifically
identified yet.

Features
========

-  Provide storage for FL related data like: initial ML algorithms,
   already trained ML models suitable for specific data sets and
   formats, averaging approaches, and auxiliary repositories for other
   additional functionalities that may be needed, and are not
   specifically identified yet.
-  Provide interfaces to put and retrieve data from different components
   of the enabler.
-  Communication with other FL enablers.

Place in architecture
=====================

FL Repository enabler is one of the Federated Learning enablers that
together enable to deploy a federated learning environment.
Functionally, it operates on scalability and manageability verticals in
the Assist-IoT architecture.

User guide
==========

Interactions with this enabler are done through a REST API. In the FL
environment this enabler interacts with FL Orchestrator, FL Training
Collector and FL Local Operations.

+-----------------+----------------------+-----------------------------+
| Method          | Endpoint             | Description                 |
+=================+======================+=============================+
| POST            | /model               |  Adds new ML model to the   |
|                 |                      | library                     |
+-----------------+----------------------+-----------------------------+
| PUT             | /model/{id}/{version | Update model that is        |
|                 | }                    | already in the repository   |
|                 |                      | under identifier id and     |
|                 |                      | version                     |
+-----------------+----------------------+-----------------------------+
| PUT             | /model/meta/{id}/{ve | Update metadata of a model  |
|                 | rsion}               | that is already in the      |
|                 |                      | repository under identifier |
|                 |                      | id and version              |
+-----------------+----------------------+-----------------------------+
| GET             | /model               | Retrieve list of all models |
|                 |                      | stored in the repository    |
+-----------------+----------------------+-----------------------------+
| GET             | /model/{id}/{version | Retrieve model with a       |
|                 | }                    | specific identifier and     |
|                 |                      | version                     |
+-----------------+----------------------+-----------------------------+
| DELETE          | /model/{id}/{version | Delete a model with a       |
|                 | }                    | specific identifier and     |
|                 |                      | version                     |
+-----------------+----------------------+-----------------------------+
| POST            | /algorithm           | Add new ML algorithm to the |
|                 |                      | repository                  |
+-----------------+----------------------+-----------------------------+
| PUT             | /algorithm/{name}/{v | Update algorithm that is    |
|                 | ersion}              | already in the repository   |
|                 |                      | with a given name and       |
|                 |                      | version                     |
+-----------------+----------------------+-----------------------------+
| PUT             | /algorithm/meta/{nam | Update metadata of an       |
|                 | e}/{version}         | algorithm that is already   |
|                 |                      | in the repository with a    |
|                 |                      | given name and version      |
+-----------------+----------------------+-----------------------------+
| GET             | /algorithm           | Retrieve lis of all ML      |
|                 |                      | algorithms stored in the    |
|                 |                      | repository                  |
+-----------------+----------------------+-----------------------------+
| GET             | /algorithm/{name}/{v | Retrieve a ML algorithm     |
|                 | ersion}              | identified with a given     |
|                 |                      | name and version            |
+-----------------+----------------------+-----------------------------+
| DELETE          | /algorithm/{name}/{v |  Delete a ML algorithm with |
|                 | ersion}              | a specific name and version |
+-----------------+----------------------+-----------------------------+
| POST            | /collector           | Add new ML training         |
|                 |                      | collector algorithm to the  |
|                 |                      | repository                  |
+-----------------+----------------------+-----------------------------+
| PUT             | /collector/{name}/{v |  Update ML training         |
|                 | ersion}              | collector algorithm that is |
|                 |                      | already in the repository   |
|                 |                      | with a given name and       |
|                 |                      | version                     |
+-----------------+----------------------+-----------------------------+
| PUT             | /collector/meta/{nam |  Update metadata of a ML    |
|                 | e}/{version}         | training collector          |
|                 |                      | algorithm that is already   |
|                 |                      | in the repository with a    |
|                 |                      | given name and version      |
+-----------------+----------------------+-----------------------------+
| GET             | /collector           |  Retrieve lis of all ML     |
|                 |                      | training collector          |
|                 |                      | algorithms stored in the    |
|                 |                      | repository                  |
+-----------------+----------------------+-----------------------------+
| GET             | /collector/{name}/{v |  Retrieve a ML training     |
|                 | ersion}              | collector algorithm         |
|                 |                      | identified with a given     |
|                 |                      | name and version            |
+-----------------+----------------------+-----------------------------+
| DELETE          | /collector/{name}/{v |  Delete a ML training       |
|                 | ersion}              | collector algorithm with a  |
|                 |                      | specific name and version   |
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

The are no configuration options for this enabler.

Developer guide
===============

Components
----------

ML Algorithms Libraries
~~~~~~~~~~~~~~~~~~~~~~~

These libraries will be used by local nodes to instantiate local
processes. The way that libraries (modules) will be stored will be
similar to the way that standard ML libraries It will made available ML
algorithms that can be used for either regular ML modelling, or for FL
modelling. Moreover, as in the well-known cases of use of external ML
modules, appropriate ML library modules are to be downloaded to the
local node, installed and used to complete model training.

FL Collectors
~~~~~~~~~~~~~

As described in the FL Training Collector enabler, different Federated
averaging algorithms can be applied to combine local results. This
component of the FL repository will store them.

ML Model Libraries
~~~~~~~~~~~~~~~~~~

The repository will also persist ML trained models. These models can be
conceptualized in two “scenarios”.

-  If the enabler is installed on a local node, it will store models
   that are currently in training and/or are “in use” by this node.

-  If the repository is instantiated in some “more central location” it
   will store current versions of shared models (including initial
   models). Here, depending on the topology, shared models may represent
   a group of nodes (e.g., in the case of use of mediators), or be
   common to all nodes.

Auxiliary
~~~~~~~~~

Any other modules that may be needed to instantiate FL can be also
stored in the FL Repository. Among them possible modules related to
process verification, error handling, stopping criteria, authorization,
belong to this category.

Local communication
~~~~~~~~~~~~~~~~~~~

Communication between external entities and the enabler.

Technologies
------------

RDF
~~~

W3C Resource Description Framework Description (RDF) is a standard for
representing information on the Web designed as a data model for
metadata. It is one of the foundations for semantic technologies. It
will provide flexible and adaptable model for ML algorithms metadata or
any auxiliary data. Components: ML Algorithms library, Auxiliary

FedML
~~~~~

Research library and benchmark for Federated ML containing federated
algorithms and optimizers. Components: FL Collectors, Auxiliary

Python
~~~~~~

Python is an interpreted high-level general-purpose programming language
with a set of libraries. Very popular for data analysis and ML
applications. Component: Local communication

FastAPI
~~~~~~~

A popular web microframework written in Python, FastAPI is known for
being both robust and high performing. It is based on OpenAPI
(previously Swagger) standards. Component: Local communication

MongoDB
~~~~~~~

MongoDB is a source-available cross-platform document-oriented database
program. Classified as a NoSQL database program. Component: ML Models
Libraries, Auxiliary

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



