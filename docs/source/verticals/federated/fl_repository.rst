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

The FL Repository is a set of different collections stored in a MongoDB
database, including initial ML models ready for training, weight results
and metrics stored after specific training processes, various
aggregation strategies, as well as numerous data transformations which
can be combined and used in order to properly process the data across
multiple heterogenous devices.

Features
========

-  Provide storage for FL related data like: initial ML model weights
   and structure, the resulting training weights of specific ML models
   combined with stored metrics, aggregation strategies encapsulating
   different model weight averaging approaches and data transformations
   for reusable data preprocessing.
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
| POST            | /model               |  Adds new ML model metadata |
|                 |                      | to the library              |
+-----------------+----------------------+-----------------------------+
| PUT             | /model/{model_name}/ | Update the data (the        |
|                 | {model_version}      | structure and the weights)  |
|                 |                      | of the model stored in FL   |
|                 |                      | Repository                  |
+-----------------+----------------------+-----------------------------+
| PUT             | /model/meta/{model_n | Update metadata of a model  |
|                 | ame}/{model_version} | that is already in the      |
|                 |                      | repository under identifier |
|                 |                      | model name and version      |
+-----------------+----------------------+-----------------------------+
| GET             | /model               | Retrieve list of all models |
|                 |                      | stored in the repository    |
+-----------------+----------------------+-----------------------------+
| GET             | /model/meta/{model_n | Retrieve the metadata of a  |
|                 | ame}/{model_version} | model with a specific model |
|                 |                      | name and version            |
+-----------------+----------------------+-----------------------------+
| GET             | /model/{model_name}/ | Retrieve the data           |
|                 | {model_version}      | specifying the structure    |
|                 |                      | and weights of a model with |
|                 |                      | a specific name and version |
|                 |                      | in the format of zipped     |
|                 |                      | files                       |
+-----------------+----------------------+-----------------------------+
| DELETE          | /model/{model_name}/ | Delete a model with a       |
|                 | {model_version}      | specific model name and     |
|                 |                      | version                     |
+-----------------+----------------------+-----------------------------+
| POST            | /training-results    |  Adds new ML training       |
|                 |                      | results to the collection   |
+-----------------+----------------------+-----------------------------+
| PUT             | /training-results/{m | Update the model weights    |
|                 | odel_name}/{model_ve | serving as the training     |
|                 | rsion}/{training_id} | results of a specific model |
|                 | /{configuration_id}  | name and version during the |
|                 |                      | training process marked     |
|                 |                      | with training_id using a    |
|                 |                      | configuration marked as     |
|                 |                      | configuration_id            |
+-----------------+----------------------+-----------------------------+
| GET             | /training-results    | Retrieve the list of all    |
|                 |                      | training results metadata   |
|                 |                      | stored in the FL Repository |
+-----------------+----------------------+-----------------------------+
| GET             | /training-results/{m | Retrieve the list of all    |
|                 | odel_name}/{model_ve | training results of         |
|                 | rsion}               | training processes          |
|                 |                      | conducted for a selected    |
|                 |                      | model name and version      |
|                 |                      | stored in the FL Repository |
+-----------------+----------------------+-----------------------------+
| GET             | /training-results/we | Retrieve the training       |
|                 | ights/{model_name}/{ | weights which were a        |
|                 | model_version}/{trai | product of the training of  |
|                 | ning_id}/{configurat | a specific model during the |
|                 | ion_id}              | training with a specific    |
|                 |                      | configuration and training  |
|                 |                      | id                          |
+-----------------+----------------------+-----------------------------+
| DELETE          | /training-results/{m | Delete the training results |
|                 | odel_name}/{model_ve | of the training of a        |
|                 | rsion}/{training_id} | specific model name and     |
|                 |                      | version obtained throughout |
|                 |                      | the training with this      |
|                 |                      | training_id                 |
+-----------------+----------------------+-----------------------------+
| POST            | /strategy            |  Adds new ML aggregation    |
|                 |                      | strategy metadata to the    |
|                 |                      | library                     |
+-----------------+----------------------+-----------------------------+
| PUT             | /strategy/{name}     | Update the aggregation      |
|                 |                      | strategy object stored      |
|                 |                      | under the selected name     |
+-----------------+----------------------+-----------------------------+
| PUT             | /strategy/meta/{name | Update metadata of a        |
|                 | }                    | strategy marked by this     |
|                 |                      | specific name               |
+-----------------+----------------------+-----------------------------+
| GET             | /strategy            | Retrieve list of all        |
|                 |                      | aggregation strategies      |
|                 |                      | stored in the repository    |
+-----------------+----------------------+-----------------------------+
| GET             | /strategy/{name}     | Download the selected       |
|                 |                      | strategy in the form of a   |
|                 |                      | pickle file                 |
+-----------------+----------------------+-----------------------------+
| DELETE          | /strategy/{name}     | Delete the file and         |
|                 |                      | metadata of a selected      |
|                 |                      | strategy                    |
+-----------------+----------------------+-----------------------------+
| POST            | /transformation      |  Adds new ML data           |
|                 |                      | transformation metadata to  |
|                 |                      | the library                 |
+-----------------+----------------------+-----------------------------+
| PUT             | /transformation/{id} | Update the transformation   |
|                 |                      | object stored under a       |
|                 |                      | specific name and version   |
+-----------------+----------------------+-----------------------------+
| PUT             | /transformation/meta | Update metadata of the data |
|                 | /{id}                | transformation object       |
|                 |                      | marked by this specific id  |
+-----------------+----------------------+-----------------------------+
| GET             | /transformation      | Retrieve the list of all ML |
|                 |                      | data transformations stored |
|                 |                      | in the repository           |
+-----------------+----------------------+-----------------------------+
| GET             | /transformation/{id} | Download the selected ML    |
|                 |                      | collector in the form of a  |
|                 |                      | pickle file                 |
+-----------------+----------------------+-----------------------------+
| DELETE          | /transformation/{id} | Delete the file and         |
|                 |                      | metadata of a selected ML   |
|                 |                      | data transformation         |
+-----------------+----------------------+-----------------------------+

Prerequisities
==============

There are three possible ways to run the FL Repository. The first, no
longer actively supported mode of deployment necessitates a local
installation of Python 3.8+, along with all the packages located in
``requirements.txt`` files already preinstalled. A second mode of
deployment uses Docker and docker-compose to locally create the
appropriate containers. The final and most encouraged mode of deployment
relies on the inclusion of the appropriate Helm charts. In order to use
this mode of deployment, the local machine needs a preinstalled version
of Kubernetes.

Installation
============

Helm chart
----------

The FL Repository enabler has been developed with the assumption that it
will be deployed on Kubernetes with a dedicated Helm chart. To do so,
just run ``helm install flrepositorylocaldb flrepositorydb``. To make
sure that before that the enabler has been configured properly, check if
the values in the ``repository-configmap`` have been properly set (to
change them, you can always modify the configmap with
``kubectl edit cm repository-configmap`` and then recreate the FL
Repository pod to propagate the changes).

By default, the chart also uses the host’s ports ``30001`` as a Node
Port. Other port may also be used, but they will have to be explicitely
changed in the ``values.yaml`` file/ Kubernetes service. You can also
set there the specific NodePort you would like to use to reach the FL
Repository API by changing the values in the flrepository service.

If you’d like to see and experiment with the API, the recommended
approach is to go to the http://127.0.0.1:XXXXX/docs URL, where XXXXX
stands for the flrepository service NodePort, and use the Swagger docs
generated by the FastAPI framework.

Docker image
------------

Run
``docker-compose -f docker-compose.yml up --force-recreate --build -d``
in the root of this repository to build a custom image to be used by the
FL Repository.

Configuration options
=====================

The are no configuration options for this enabler.

Developer guide
===============

Collections
~~~~~~~~~~~

FL Models
^^^^^^^^^

This collection stores the ready-for-training data of a selected model.
The information about the model weights and structure is stored in files
inside a zipped directory, allowing for easy incorporation of different
formats preferred by different libraries. Aside from that, metadata like
information about the library that this model data uses or the
capabilities needed to train this model will be saved here as well.

For example:

.. code:: json

   {
       "meta": {
         "library": "keras",
         "description": "A CNN (Convolutional Neural Network) designed to solve the CIFAR-10 image classification task. Used as a test model for the development of the Keras library."
       },
       "model_name": "base",
       "model_version": "base2",
       "model_id": "62aae16f6ee3b61c9c6c2921"
     }

The models collection can be manipulating using the following endpoints:

-  **POST /model**
   Adds the metadata of a new initial model to the library.
-  **PUT /model/{name}/{version}**
   Depending on whether a model with a given name and version exists in
   the FL Repository, its object file is created or updated.
-  **PUT /model/meta/{name}/{version}**
   For the given model name and version its metadata is updated.
-  **GET /model**
   Return the list encompassing the metadata of all available models.
-  **GET /model/meta**
   Return the metadata of the model with a given name and version.
-  **GET /model/{name}/{version}**
   Return the binary file containing the final model weights and
   structure.
-  **DELETE /model/{name}/{version}**
   Delete the metadata and binary file of a model with a given name and
   version.
-  **GET /models/available** Return the list encompassing the metadata
   of all available models, sorted by their upload date.
-  **GET /models/download/shell/{filename}** Download the binary files
   containing the model weights and structure for all available models,
   sorted by their upload date.

More information about the construction and upload of new models, along
with a quick tutorial on how to update the ML Model with the selected
training results will be found in the documentation of the FL Local
Operations.

FL Training Results
^^^^^^^^^^^^^^^^^^^

This collection stores the training results obtained after finishing the
training of a specific ML model. It incorporated the obtained metrics,
information about the training and configuration id, as well as the
final training weights saved in the ``pickle`` format. For example:

.. code:: json

   {
       "model_name": "keras_test",
       "model_version": "version_1",
       "training_id": "12",
       "results": {
         "rounds": "3",
         "final_loss": "78.94696807861328",
         "accuracy": "0.21299999952316284",
         "min_fit_clients": "1",
         "min_evaluate_clients": "1",
         "min_available_clients": "1"
       },
       "weights_id": "652838994e96467edfe72a9a",
       "configuration_id": "10"
   }

The training results collection can be manipulating using the following
endpoints:

-  **POST /training-results**
   Upload new training results (including final model weights and
   metadata containing aggregated metrics and configuration) for a given
   model_name, model_version, training_id and configuration_id.
-  **GET /training-results** Get the list with the metadata of all
   training results available in this FL Repository instance.
-  **GET /training-results/{name}/{version}**
   Get the list with the metadata of all training results available in
   this FL Repository instance for a given model name and version.
-  **PUT
   /training-results/{name}/{version}/{training-id}/{configuration-id}**
   Update the final training weights of a given training results
   instance.
-  **GET /training-results/weights/{name}/{version}/{training-id}**
   Return the final weights achieved as a result of a training.
-  **DELETE /training-results/{name}/{version}/{training-id}**
   Delete the selected training results (the weights along with the
   metadata).

More information about the format of the training results sent from the
FL Training Collector and how to use them to update the weights of a
given FL model can be found in the documentation of the FL Local
Operations and of the FL Training Collector.

FL Strategies
^^^^^^^^^^^^^

FL Strategies contain information about the available weight aggregation
strategies for the FL enabler. The custom strategies have to implement
the Strategy Abstract Base Class from the Flower library in order to
easily incorporate them into the FL Training Collector. The strategy
files will contain a pickled strategy object, with the metadata
describing the purpose and usage of this strategy.For example:

.. code:: json

   {
       "meta": {
       },
       "strategy_name": "fault-tolerant-fedavg",
       "strategy_description": "A fault tolerant version of FedAvg",
       "strategy_id": "632b8668657188818260a056"
   }

The aggregation strategy collection can be manipulating using the
following endpoints:

-  **POST /strategy**
   Create a new aggregation strategy with the specified metadata.
-  **PUT /strategy/{name}**
   Update the object file for the aggregation strategy with a given
   name.
-  **PUT /strategy/meta/{name}** Update the metadata for the aggregation
   strategy with a given name.
-  **GET /strategy** Get the metadata of all available aggregation
   strategies in the form of a list.
-  **GET /strategy/{name}**
   Get the object file of the aggregation strategy with a given name.
-  **DELETE /strategy/{name}**
   Delete the aggregation strategy of a given name.

More information about the format of the aggregation strategies that can
be used by the FL Training Collector and how to add new ones can be
found in the documentation of the FL Training Collector.

FL Transformations
^^^^^^^^^^^^^^^^^^

FL Transformations contain information about the available data
transformations for the FL Local Operations or FL Training Collector.
The custom transformations have to implement the DataTransformation
Abstract Base Class described in the ``data_transformation`` module in
FL Local Operations. The metadata of this collection will include not
only the description of this specific transformation, but also necessary
parameter types, default values and the capabilities needed to run this
transformation on the local machine. The transformation files will
contain a Data Transformation object in a dill or pickle format. For
example:

.. code:: json

   {
       "id": "application.tests.categorical_transformation",
       "description": "This class transforms y data into categorical data",
       "parameter_types": {
         "categories": "int"
       },
       "default_values": {
         "categories": 10
       },
       "outputs": [
         "np.ndarray",
         "np.ndarray"
       ],
       "needs": {
         "storage": 0,
         "RAM": 0,
         "GPU": false,
         "preinstalled_libraries": {},
         "available_models": {}
       }
     }

The data transformations collection can be manipulating using the
following endpoints:

-  **POST /transformation**
   Create a new data transformation with the specified metadata.
-  **PUT /transformation/{id}**
   Update the object file for a given data transformation.
-  **PUT /transformation/meta/{id}** Update the metadata of a given data
   transformation.
-  **GET /transformation**
   Get the list with the metadata of all data transformations available
   in this FL Repository instance.
-  **GET /transformation/{id}**
   Get the object file of a data transformation with a given id.
-  **DELETE /transformation/{id}**
   Delete the metadata and the object file of a data transformation with
   a given id.

More information about how to construct, connect and reuse data
transformations can be found in the documentation of the FL Local
Operations.

Local communication
^^^^^^^^^^^^^^^^^^^

The communication between the collections and an outside developer is
carried out through the (described above) RESTful endpoints. In order to
do so, a FastAPI application has been implemented.

Serializing and deserializing the database
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you want for the MongoDB database on your custom repositorydb image
to initialize with some of the preexisting objects already stored in the
collections, you can achieve that by: 1. Use the API to add and subtract
the objects in the database until it has the desired content. 2. Use the
``kubectl exec -i -t <podname> -- /bin/bash`` command to reach the
commandline of the repositorydb pod. 3. Use the
``mongodump --archive=db.dump`` tool with the appropriate options to
create the backup file. 4. Use
``kubectl cp <podname>:/db.dump .db.dump`` to move the archive file from
the pod to the repository. 5. Move the db.dump file to the mongo_db
directory. 6. Run the
``docker-compose -f docker-compose.yml up --force-recreate --build -d``
command to construct the right image.

Technologies
~~~~~~~~~~~~

Python
^^^^^^

Python is an interpreted high-level general-purpose programming language
with a set of libraries. Very popular for data analysis and ML
applications. Component: Local communication

FastAPI
^^^^^^^

A popular web microframework written in Python, FastAPI is known for
being both robust and high performing. It is based on OpenAPI
(previously Swagger) standards. Component: Local communication

MongoDB
^^^^^^^

MongoDB is a source-available cross-platform document-oriented database
program. Classified as a NoSQL database program. Component: ML Models
Libraries, Auxiliary

GridFS
^^^^^^

GridFS is a specification for storing and retrieving MongoDB files that
exceed the BSON-document size limit of 16 MB. It uses the technique of
dividing them into chunks for this specific purpose.

Pickle
^^^^^^

A Python library allowing for the serialization and de-serialization of
any Python object through converting them to a byte stream. An extension
(one of many) of the pickle library is known as dill.

Authors
=======

-  Karolina Bogacka
-  Katarzyna Wasielewska-Michniewska

License
=======

The FL Repository is released under the Apache 2.0 license, as we have
internally concluded that we are not “offering the functionality of
MongoDB, or modified versions of MongoDB, to third parties as a
service”. However, potential future commercial adopters should be aware
that our project uses MongoDB in order to be able to accurately
determine the license most applicable to their projects.

You may obtain a copy of the License at:
http://www.apache.org/licenses/LICENSE-2.0

Notice (dependencies)
=====================

The information about the dependencies needed to run a specific part of
the application can be found described in the appropriate
``requirements.txt`` files located. However, since they are downloaded
automatically during the construction of the appropriate Docker images,
the local dependencies needed to deploy the application include only a
local Docker along with Docker Compose or Kubernetes installation.



