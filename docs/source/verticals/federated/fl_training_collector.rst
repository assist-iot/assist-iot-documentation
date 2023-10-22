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

It was developed as a part of an FL system along with the FL
Orchestrator, FL Local Operations and FL Repository and should ideally
be deployed with those enablers in order to use its full functionality
(although it is possible to conduct an FL training process without using
the FL Orchestrator which serves as a GUI, configuring the enabler
throught the use of its dedicated REST API). It encapsulates the
functionalities of a federated learning (FL) server by synchronizing the
training with multiple FL Local Operations instances (clients) while
continuously sending updates to the FL Orchestrator (GUI) and storing
the results of the training (final weights of the model and relevant
metrics) in the FL Repository (database).

Features
========

-  Aggregate local updates of the ML model prepared by independent
   parties as part of a model enhancement process.

-  Allow for the flexible use of the custom aggregation strategies
   located in FL Repository.

-  Allow for the use of selected privacy mechanisms (Adaptive
   Differential Privacy, Homomorphic Encryption) during the Federated
   Learning process.

-  Aggregate evaluation metrics throughout the FL training process,

-  Delivering the results of the training (final aggregated weights and
   metrics) to the FL Repository for storage.

-  Stopping the FL Local Operations instances (gracefully in situations
   of achieving target metrics early, and not gracefully in situations
   when the number of FL Local Operations is insufficient.

Place in architecture
=====================

FL Training Collector enabler is one of the Federated Learning enablers
that together allow to deploy a federated learning environment.
Functionally, it operates on scalability and manageability verticals in
the Assist-IoT architecture.

User guide
==========

Interactions with this enabler are done through a REST API. In the FL
environment the FL Orchestrator enabler sends the appropriate
configuration to FL Training Collector.

The enabler exposes REST API (see endpoints below) to communicate with
external enablers/applications but also uses gRPC to communicate with FL
Local Operations during model trainings.

+-----------------+----------------------+-----------------------------+
| Method          | Endpoint             | Description                 |
+=================+======================+=============================+
| POST            | /job/config/{id}     | Receive configuration for   |
|                 |                      | the specific training of a  |
|                 |                      | selected model for job with |
|                 |                      | identifier id               |
+-----------------+----------------------+-----------------------------+
| GET             | /job/status/{id}     | Retrieve status of the      |
|                 |                      | training process with       |
|                 |                      | identifier id               |
+-----------------+----------------------+-----------------------------+
| GET             | /job/stop            | Stop all ongoing training   |
|                 |                      | processes                   |
+-----------------+----------------------+-----------------------------+

Training Configuration
----------------------

In order to initiate the training, a JSON encompassing the following
configuration should be sent to the endpoint shown below. The most
important available keys and their meaning will be explained further
down.

**POST /job/config/{training_id}/**

.. code:: json

   {
     "strategy": "string", 
     "model_name": "string", 
     "model_version": "string",
     "adapt_config": "string",
     "server_conf": {
       "num_rounds": 0,
       "round_timeout": 0
     },
     "strategy_conf": {
       "fraction_fit": 0,
       "fraction_evaluate": 0,
       "min_fit_clients": 0,
       "min_evaluate_clients": 0,
       "min_available_clients": 0,
       "accept_failures": true,
       "server_learning_rate": 0,
       "server_momentum": 0,
       "min_completion_rate_fit": 0,
       "min_completion_rate_evaluate": 0,
       "eta": 0,
       "eta_l": 0,
       "beta_1": 0,
       "beta_2": 0,
       "tau": 0,
       "q_param": 0,
       "qffl_learning_rate": 0
     },
     "client_conf": [
       {
         "config_id": "string",
         "batch_size": 32,
         "steps_per_epoch": 3,
         "epochs": 0,
         "learning_rate": 0.05
       }
     ],
     "privacy-mechanisms": {
       "homomorphic": {
         "poly_modulus_degree": 8192,
         "coeff_mod_bit_sizes": [60, 40, 40],
         "scale_bits": 40,
         "scheme": "CKKS"
       },
       "dp-adaptive": {
         "num_sampled_clients": 0,
         "init_clip_norm": 0.1,
         "noise_multiplier": 1,
         "server_side_noising": true,
         "clip_count_stddev": 0,
         "clip_norm_target_quantile": 0.5,
         "clip_norm_lr": 0.2
       },
     },
     "configuration_id": 0,
     "stopping_flag": false,
     "stopping_target": {
       "metric": 0,
     }
   }

The definitions: - **strategy** The name that the strategy is stored
under in the FL Repository. - **model_name** The name of the model that
should be used in the training (as described in the FL Repository) -
**model_version** The version of the model that should be used in the
training (as described in the FL Repository) - **adapt_conf** The
parameter indicating whether the learning rate should be adapted on the
FL Training Collector. It is currently preferable to change this aspect
through the use of FL strategies. - **server_conf** The configuration
designated to be used by the underlying
`Flower <https://github.com/adap/flower>`__ server. - **num_rounds** For
how many rounds should run the FL training. - **timeout** Whether the FL
server should wait for the results of all of its configured clients or
stop after a timeout. Compatible with the server timeout in Flower. -
**strategy_conf** The parameters that allow for the flexible
configuration of one of the three aggregation strategies offered
out-of-the-box (other strategies can also be added to the FL Repository
and ran, but they should have already preconfigured the parameters that
are specific to them). More about the meaning of the specific fields can
be found in the Flower documentation. - **client_conf** The basic
parameters that can be sent to configure the client from the FL server.
Currently not used in the three default strategies, but preserved to be
used by the custom strategies if applicable. - **privacy-mechanisms**
The configuration indicating which privacy mechanisms should the FL
Training Collector employ (if any) and what should be their parameters.
This dictionary can have no keys (which indicates no privacy mechanisms
used), “homomorphic” which indicates the use of HE, “dp-adaptive” which
indicates the use of Differential Privacy with Adaptive Clipping or both
“homomorphic” and “dp-adaptive”, which indicates that both techniques
should be used. - **homomorphic** The parametres configurable to be used
for homomorphically encrypted federated averaging are used to specify
the context as described in the
`TenSEAL <https://github.com/OpenMined/TenSEAL>`__ documentation. -
**dp-adaptive** The parametres specifying the differentially private
Federated Averaging are taken from the Flower library and, by proxy,
from the `relevant paper <https://arxiv.org/pdf/1905.03871.pdf>`__. -
**configuration_id** This describes the id of the configuration the
results of this training will be stored under. - **stopping_flag** This
flag indicates whether the training should stop when one of the
aggregated evaluation metrics reaches a specific value. -
**stopping_target** This specifies the values of the aggregated metrics
that, if one of them is surpassed, will cause the whole training process
to stop gracefully (saving the results of the training process in the FL
Repository beforehand)

A sample test configuration can be seen here:

.. code:: json

   {
     "strategy": "avg",
     "model_name": "keras_test",
     "model_version": "version_1",
     "adapt_config": "custom",
     "server_conf": {
       "num_rounds": 3
     },
     "strategy_conf": {
       "min_fit_clients" : "1",
       "min_available_clients": "1",
       "min_evaluate_clients": "1"
     },
   "privacy-mechanisms":{
   },
     "client_conf": [
       {
         "config_id" : "min_effort",
         "batch_size": "64",
         "steps_per_epoch" : "32",
         "epochs" : "5",
         "learning_rate" : "0.001"
       }
     ],
     "configuration_id": "10",
     "stopping_flag":true,
     "stopping_target": {"accuracy":0.25}
   }

Other API endpoints
-------------------

**GET /job/status/{training_id}**

A GET request send to this specific endpoint along with the id of the
training which we are interested in will receive an information about
the status of the job. The status may show that the training is
``INACTIVE``, ``WAITING``, ``TRAINING``, ``INTERRUPTED`` or
``FINISHED``. Information about the round number may also be specified
if appropriate.

**POST /job/stop**

A POST request to this specific endpoint will cause of the active
training processes on the FL Training Collector to stop. The stopping
will not be graceful (with saving the results of the training as when
the ``stopping_target`` is archived), as we assume that this endpoint is
used when the FL Orchestrator can not find enough active FL Local
Operations instances to proceed with the training.

Prerequisities
==============

There are three possible ways to run the FL Local Operations. The first,
no longer supported mode of deployment necessitates a local installation
of Python 3.8+, along with all the packages located in
``requirements.txt`` files already preinstalled. A second, mode of
deployment uses Docker and docker-compose to locally create the
appropriate containers. The third and recommended mode of deployment
relies on the inclusion of the appropriate Helm charts. In order to use
this mode of deployment, the local machine needs a preinstalled version
of Kubernetes.

Helm chart
----------

The FL Training Collector enabler has been developed with the assumption
that it will be deployed on Kubernetes with a dedicated Helm chart. To
do so, just run
``helm install trainingcollectorlocal trainingcollector``. To make sure
that before that the enabler has been configured properly, check if the
values like ``REPOSITORY_ADDRESS`` (indicating the address under which
the FL Repository can be found in the Kubernetes cluster) or
``ORCHESTRATOR_ADDRESS`` (similar address, but for the FL Orchestrator)
in the ``training-collector-configmap`` have been properly set (to
change them, you can always modify the configmap with
``kubectl edit cm training-collector-configmap`` and then recreate the
FL Training Collector pod to propagate the changes).

By default, the chart also uses the host’s ports ``30800`` and ``30808``
as Node Ports. Other ports may also be used, but they will have to be
explicitely changed in the ``values.yaml`` file/ Kubernetes service.

If you’d like to see and experiment with the API, the recommended
approach is to go to the http://127.0.0.1:30800/docs URL (if the
NodePort for the first FL TC endpoint has been changes, it should be
also updated in the URL) and use the Swagger docs generated by the
FastAPI framework.

Docker image
------------

Run
``docker-compose -f docker-compose.yml up --force-recreate --build -d``
in the root of this repository to build a custom image to be used by the
FL Training Collector.

Developer guide
===============

Components
~~~~~~~~~~

The enabler provides a REST API to allow the input and output
communication to and from the FL Training Collector enabler. On the one
hand it is responsible of receiving FL local updates that are sent to
the FLC Combiner component. On the other hand, it is responsible of
communicating updates of the new FL model obtained in the FLC Component
to the FL Repository. The communication capabilities of this component
are designed so that it can conceptually deal with situations in which
more complex topologies are used.

The enabler will receive weight updates from a certain number (possibly
all) local nodes and combine them to generate an updated FL model. It
can include both homogeneous and heterogeneous FedAvg solutions for
e.g., logistic regression models, decision-tree models, or even neural
network models.

Additionally, the enabler allows for the usage of selected privacy
mechanisms. Here, it is important to mention that Homomorphic Encryption
can only be used currently with very small models, like Logistic
Regression.

Pluggability
~~~~~~~~~~~~

The FL Training Collector can be configured to use a wide array of FL
aggregation strategies. Those aggregation strategies should be instances
of the relevant classes from the ``flwr.server.strategy`` module. A
selected object can be then serialized using the code shown below and
uploaded to the FL Repository to the strategy collection, using the
relevant instructions formulated for the FL Repository. Then, the
strategy can be selected in the training configuration by specifying the
“strategy” field to be the name of the strategy as placed in the FL
Repository. As a special case of the most commonly used aggregation
strategy in the FL domain, FedAvg can also be instantiated using the
keyword “avg”.

.. code:: python

   import flwr as fl
   import pickle

   fedmedian = fl.server.strategy.FedMedian()
   with open('temp.pkl', 'wb') as f:
       pickle.dump(fedmedian, f) 

**Attention**: Make sure that the Python version of the environment
where you’re instantiating the object is the same as where you’re
instantiating it, so in the Docker image of the FL Training Collector
(by default it’s 3.8.3). Otherwise, you may notice problems with magic
numbers in pickle caused by that discrepancy.

In addition to the process described above, there are three aggregation
strategies that can be used out of the box (they either come
preprogrammed or should be already present in the FL Repository). Those
three aggregation strategies are
`FedAvg <https://github.com/adap/flower/blob/main/src/py/flwr/server/strategy/fedavg.py>`__,
`FedMedian <https://github.com/adap/flower/blob/main/src/py/flwr/server/strategy/fedmedian.py>`__
and a `fault-tolerant variant of the FedAvg
strategy <https://github.com/adap/flower/blob/main/src/py/flwr/server/strategy/fault_tolerant_fedavg.py>`__.

Storage
~~~~~~~

At the end of the training, aside from the pickled final weights of the
model the FL Training Collector sends to the FL Repository the metadata
of the given training results (in the form of a JSON), which includes:

-  **model_name** The name of the model used for the training (as stored
   in FL Repository)
-  **model_version** The version of the model used for the training (as
   stored in FL Repository)
-  **training_id** The id of the conducted training process
-  **results**

   -  **rounds** The number of rounds that have finally been conducted.
   -  **final_loss** The final aggregated loss achieved by the clients
      in their local evaluation
   -  …other aggregated metrics, depending on the clients’
      configuration…
   -  …the strategy configuration of the training…

-  **configuration_id** The id of the configuration that the training
   was conducted under.

Privacy
~~~~~~~

There are two privacy mechanisms implemented to be used by the FL
System. The FL Training Collector can be configured to work with either
of them, both or none of them through the use of the training
configuration.

Differential Privacy
^^^^^^^^^^^^^^^^^^^^

The mechanism of `Adaptive Differential
Privacy <https://github.com/adap/flower/blob/main/src/py/flwr/server/strategy/dpfedavg_adaptive.py>`__
modifies the selected strategy by introducing noise to the local model
parameters before they are sent by the client. This increases the
privacy of the data on the client by obfuscating the information about
its distribution. This specific implementation additionally uses
adaptive clipping to reduce the balance the influence of multiple
clients. The use of this privacy technique may lead to a degradation in
the performance of the final model, but introduces little to none
additional, computational cost.

The use of adaptive differential privacy and its specific parameters can
be specified in the training configuration under the
``privacy_mechanisms`` keyword. If we include ``dp-adaptive`` in this
dictionary, we can specify the parameters used by the Flower
implementation under the ``dp-adaptive`` key and configure the training
like this:

.. code:: json

   "privacy-mechanisms":{
     "dp-adaptive":{
       "num_sampled_clients":"1"
     }
   }

Homomorphic Encryption
^^^^^^^^^^^^^^^^^^^^^^

The mechanism of Federated Averaging with Homomorphic Encryption has
been implemented from scratch using the
`TenSEAL <https://github.com/OpenMined/TenSEAL>`__ library. As
Homomorphic Encryption allows for the encryption of numbers such that
the decrypted sum of encrypted numbers is the same as the sum of
encrypted numbers (and similarly for the subtraction and
multiplication). It therefore allows the FL clients to send their
encrypted weights, which can then be aggregated and return as the
averaged weights in the encrypted form. This ensures that in the event
of a malicious server (or a malicious eavesdropper) the privacy of the
clients’ data remains intact.

The current implementation encrypts the parameters as a CCKS tensor (as
implemented in TenSEAL), so if the user would like to generate and
serialize new keys and contexts, they should be compatible with this
method.

The current implementation of Homomorphic Encryption is only valid with
the use of Federated Averaging, so even if another aggregation strategy
was selected, it will be automatically changed to the Federated
Averaging by the FL Training Collector.

If a new public key is generated, the
``application/src/hm_keys/public.text`` file should be appropriately
changed (and potentially modified to be a Kubernetes secret).

Technologies
~~~~~~~~~~~~

Python
^^^^^^

Python is an interpreted high-level general-purpose programming language
with a set of libraries. Very popular for data analysis and ML
applications.

FastAPI
^^^^^^^

A popular web microframework written in Python, FastAPI is known for
being both robust and high performing. It is based on OpenAPI
(previously Swagger) standards.

Flower
^^^^^^

A federated learning framework designed to work with a large number of
clients. It is both compatible with a variety of ML frameworks and
supports a wide range of devices.

TenSEAL
^^^^^^^

A library that empowers users to easily conduct Homomorphic Encryption
operations on tensors, built on top of Microsoft SEAL. Since the
underlying implementation uses C++, the resulting methods consume as
little resources as possible.

Authors
=======

Karolina Bogacka

Licence
=======

The FL Training Collector is released under the Apache 2.0 license.

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



