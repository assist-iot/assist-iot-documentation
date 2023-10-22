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
update proposals of the ML algorithm are shared with others. An
inference engine can also provide inference based on the final model.
Both operations (model training and model inference) involve access to
private data. This means that it is crucial to “encapsulate” local
processes within a single “node” (that is controlled by data owner).
However, it should be noticed that the data that is being used in both
FL training processes has to be in the same format, which is imposed by
the ML model that is being employed. In order to carry out with all
these local operations, the FL Local Operation enabler is proposed. It
consists of a few different modules: a data transformation module (the
module handles the process of negotiating a suitable transformation
pipeline for a given data format in order to allow for the training or
inference of a specific model, and will be further extended in future
works), a component encapsulated in a web application and responsible
for model training, a component equipped with gRPC services and
responsible for model inference, as well as a privacy module providing
two selected privacy mechanisms for the FL training process (adaptive
differential privacy and homomorphic encryption).

It was developed as a part of an FL system along with the FL
Orchestrator, FL Local Operations and FL Repository and should ideally
be deployed with those enablers in order to use its full functionality
(although it is possible to conduct an FL training process without using
the FL Orchestrator which serves as a GUI, configuring the enabler
throught the use of its dedicated REST API). It encapsulates the
functionalities of a federated learning (FL) client by maintaining a
connection with the FL Orchestrator (GUI and monitoring), connecting to
the training initiated by the FL server (FL Training Collector),
periodically providing it with local weights and obtaining new global
weights, as well as downloading any necessary components from the FL
Repository (database).

Beyond the classic functionality of an FL client, however, FL Local
Operations also enables the local inference deployment of a selected
model (that can function as a standalone container), the use of flexible
configurations, basic format verification and pluggable components, as
well as selected privacy mechanisms. FL Local Operations is compatible
with Prometheus metric monitoring.

Features
========

-  Enabler embedded in each FL involved party performing local training.
-  The possibility of conducting such training using PyTorch and Keras
   libraries, additionally allowing for the detailed configuration of
   appropriate optimizers, schedulers and callbacks.
-  Verification of local data formats compatibility with data formats
   required by FL through the use of format, model and data
   transformations configurations.
-  Transformation of local data formats to the format required by the ML
   system by specifying a chain of atomic transformations along with the
   appropriate parameters.
-  Custom clients, data loaders and services can also be constructed.
-  Local storage of models for training process optimization purposes is
   allowed.
-  The local results are sent to the FL Training Collector in order to
   carry out the appropriate aggregation methodology over the common
   shared model.
-  There are multiple aggregation algorithms provided, with an added
   possibility to implement and include an additional one.
-  The inference module allows for placing models in the TFLite format
   on inference. Combined with the inclusion of gRPC for inference
   module communication, it provides a particularly lightweight
   inference solution.
-  The inference module can be deployed as a standalone.
-  Communication of model updates via encryption mechanisms. Homomorphic
   encryption will not permit outsiders to see the output model of each
   device/party (MITM attacks), whereas methods for creating
   differentially private noise will guarantee that Malicious Aggregator
   cannot be allowed to infer which records are actual models and which
   not.
-  Unit tests are included which can be ran using ``pytest``.

Place in architecture
=====================

FL Local Operations enabler is one of the Federated Learning enablers
that together enable to deploy a Federated Learning environment.
Functionally, it operates on scalability and manageability verticals in
the Assist-IoT architecture.

User guide
==========

FL Local Operations: Training Module
------------------------------------

Interactions with the training module of this enabler are done through a
REST API. In the FL environment the FL Orchestrator enabler sends
appropriate configuration to FL Local Operations that later on
communicate with FL Training Collector and FL Repository if required.

The enabler exposes REST API (see endpoints below) to communicate with
external enablers/applications but also uses gRPC to communicate with FL
Training Collector during model training processes.

+-----------------+----------------------+-----------------------------+
| Method          | Endpoint             | Description                 |
+=================+======================+=============================+
| POST            | /job/config/{id}     | Receive configuration for a |
|                 |                      | training job                |
+-----------------+----------------------+-----------------------------+
| POST            | /model/              | Receive the configuration   |
|                 |                      | of a new model for local    |
|                 |                      | storage                     |
+-----------------+----------------------+-----------------------------+
| PUT             | /model/{model_name}/ | Receive the zipped data of  |
|                 | {model_version}      | a given model               |
+-----------------+----------------------+-----------------------------+
| GET             | /status              | Get current status of the   |
|                 |                      | enabler                     |
+-----------------+----------------------+-----------------------------+
| GET             | /capabilities        | Get information about the   |
|                 |                      | capabilities (available     |
|                 |                      | dependencies, GPU etc) of   |
|                 |                      | the local machine           |
+-----------------+----------------------+-----------------------------+
| GET             | /format              | Get information about the   |
|                 |                      | format of the data          |
|                 |                      | available on the local      |
|                 |                      | machine                     |
+-----------------+----------------------+-----------------------------+

Additionally, the configuration of the final, Kubernetes deployment of
the FL LO Training Module can be modified through the manipulation of
files located in the ``pvc-data-lo`` Persistent Volume. Those files
clarify the format of the local data (``format.json``), as well as which
transformations in what order should be applied to this data
(``transformation_pipeline.json``). Specific environmental variables,
important for the deployment, such as the address of the FL Repository
enabler, address of the FL Orchestrator enabler etc. may also be
adjusted in a the suitable ConfigMaps.

FL Local Operations: Inference Module
-------------------------------------

In order to create a component capable of truly fast and lightweight
inference, a choice was made to use gRPC instead of REST in order to
communicate with the inference model. The resulting specification of
input and output messages looks as follows: \` syntax = “proto3”;

package basic_inference;

message Tensor32 { repeated float array = 1; repeated int32 shape = 2; }

message BasicInferenceRequest{ int32 id = 1; Tensor32 tensor = 2; }

message BasicInferenceResponse{ int32 id = 1; Tensor32 tensor = 2; }

service BasicInferenceService{ rpc predict(stream BasicInferenceRequest)
returns (stream BasicInferenceResponse) {} } \` Here, the
BasicInferenceRequest encapsulates the unique id of the request (which
will later allow to easily match the predictions with the necessary
input data), as well as the data necessary for inference. In order to
create as application independent (and therefore as suitable for later
reuse) as possible gRPC service, the input data is specified just a
series of floats with a dynamic shape. The process uses bidirectional
streaming for maximal speed and flexibility.

Prerequisities
==============

There are three possible ways to run the FL Local Operations. The first,
no longer supported mode of deployment necessitates a local installation
of Python 3.8+, along with all the packages located in
``requirements.txt`` files already preinstalled. A second, much more
strongly encouraged mode of deployment uses Docker and docker-compose to
locally create the appropriate containers. The third and final mode of
deployment relies on the inclusion of the appropriate Helm charts. In
order to use this mode of deployment, the local machine needs a
preinstalled version of Kubernetes.

Helm chart
----------

The FL Local Operations enabler has been developed with the assumption
that it will be deployed on a Kubernetes cluster with a dedicated Helm
chart. To do so, just run
``helm install fllocaloperationslocal fllocaloperations``. If you want
to deploy multiple FL Local Operations in one Kubernetes cluster, just
choose different names for all of the deployments. If you want to deploy
only the inference component, run
``helm install fllocaloperationslocal fllocaloperations --set inferenceapp.fullDeployment.enabled=false``.

To make sure that before that the enabler has been configured properly,
check the 3 ConfigMaps that are deployed alongside the enabler. Their
names change depending on the name od the deployment (to allow for
multiple Local Operations instances to coexist in a Kubernetes cluster
while having slightly different configurations).

The first, which name starts with ``flinference-config-map``, serves to
flexibly set and change the configuration for the inference component,
including the data format received by the gRPC service (as
``format.json``), the name, version and input format of the model (as
``model.json``), the configuration of the data transformation pipeline
(as ``transformation_pipeline.json``) and the data about both the
serialized gRPC service and the specific inferencer to be used (as
``setup.json``).

The second config map, which name begins with ``fllocalops-config-map``
contains the environmental variables necessary to deploy the FL Local
Operations instance. Check especially the fields of
``REPOSITORY_ADDRESS`` (the address of the nearest FL Repository
instance), ``ORCHESTRATOR_SVR_ADDRESS`` (the address of the FL
Orchestrator’s main service), ``ORCHESTRATOR_WS_ADDRESS`` (the address
that the websocket should use to connect to the FL Orchestrator) and
``SERVER_ADDRESS`` (the address of the FL Training Collector). If you
change something in the ConfigMap when the enabler is already deployed,
destroy the inferenceapp and trainingapp pods to let them recreate with
the updated configuration.

Finally, the ConfigMap beginning with ``fltraining-config-map``
describes the configuration necessary to run the trainingapp component
with pluggable transformations. This includes the data format that the
data loader has access to (as ``format.json``), the input format of the
model (as ``model.json``), the configuration of the train data
transformation pipeline (as ``transformation_pipeline_train.json``) as
well as test data transformation pipleine
(``transformation_pipeline_test.json``) and the data about both the
specific data loader and training client that will need to be used (as
``setup.json``).

If you’d like to see and experiment with the API, the recommended
approach is to go to the http://127.0.0.1:XXXXX/docs URL (if the
NodePort for the first FL Local Operations endpoint has been changes, it
should be also updated in the URL) and use the Swagger docs generated by
the FastAPI framework.

Docker image
------------

You can run
``USER_INDEX=1 FL_LOCAL_OP_DATA_FOLDER="./data" docker compose up --force-recreate --build -d``
in your terminal to build a new Docker image or use the
``start-local.sh`` script to do it automatically (for instance, by
running the command ``./start-local.sh 1``).

Configuration options
=====================

In order to initiate the training, a JSON encompassing the following
configuration should be sent to the endpoint shown below. The most
important available keys and their meaning will be explained further
down.

**POST /job/config/{training_id}/**

.. code:: json

   {
     "client_type_id": "string",
     "server_address": "string",
     "eval_metrics": [
       "string"
     ],
     "eval_func": "string",
     "num_classes": 0,
     "num_rounds": 0,
     "shape": [
       0
     ],
     "training_id": 0,
     "model_name": "string",
     "model_version": "string",
     "config": [
       {
         "config_id": "string",
         "batch_size": 0,
         "steps_per_epoch": 0,
         "epochs": 0,
         "learning_rate": 0
       }
     ],
     "optimizer_config": {
       "optimizer": "string",
       "lr": 0,
       "rho": 0,
       "eps": 0,
       "foreach": true,
       "maximize": true,
       "lr_decay": 0,
       "betas": [
         "string",
         "string"
       ],
       "etas": [
         "string",
         "string"
       ],
       "step_sizes": [
         "string",
         "string"
       ],
       "lambd": 0,
       "alpha": 0,
       "t0": 0,
       "max_iter": 0,
       "max_eval": 0,
       "tolerance_grad": 0,
       "tolerance_change": 0,
       "history_size": 0,
       "line_search_fn": "string",
       "momentum_decay": 0,
       "dampening": 0,
       "centered": true,
       "nesterov": true,
       "momentum": 0,
       "weight_decay": 0,
       "amsgrad": true,
       "learning_rate": 0,
       "name": "string",
       "clipnorm": 0,
       "global_clipnorm": 0,
       "use_ema": true,
       "ema_momentum": 0,
       "ema_overwrite_frequency": 0,
       "jit_compile": true,
       "epsilon": 0,
       "clipvalue": 0,
       "initial_accumulator_value": 0,
       "beta_1": 0,
       "beta_2": 0,
       "beta_2_decay": 0,
       "epsilon_1": 0,
       "epsilon_2": 0,
       "learning_rate_power": 0,
       "l1_regularization_strength": 0,
       "l2_regularization_strength": 0,
       "l2_shrinkage_regularization_strength": 0,
       "beta": 0
     },
     "scheduler_config": {
       "scheduler": "string",
       "step_size": 0,
       "gamma": 0,
       "last_epoch": 0,
       "verbose": true,
       "milestones": [
         0
       ],
       "factor": 0,
       "total_iters": 0,
       "start_factor": 0,
       "end_factor": 0,
       "monitor": "string",
       "min_delta": 0,
       "patience": 0,
       "mode": "string",
       "baseline": 0,
       "restore_best_weights": true,
       "start_from_epoch": 0,
       "cooldown": 0,
       "min_lr": 0
     },
     "warmup_config": {
       "scheduler": "string",
       "warmup_iters": 0,
       "warmup_epochs": 0,
       "warmup_factor": 0,
       "scheduler_conf": {
         "scheduler": "string",
         "step_size": 0,
         "gamma": 0,
         "last_epoch": 0,
         "verbose": true,
         "milestones": [
           0
         ],
         "factor": 0,
         "total_iters": 0,
         "start_factor": 0,
         "end_factor": 0,
         "monitor": "string",
         "min_delta": 0,
         "patience": 0,
         "mode": "string",
         "baseline": 0,
         "restore_best_weights": true,
         "start_from_epoch": 0,
         "cooldown": 0,
         "min_lr": 0
       }
     },
     "privacy-mechanisms": {
       "homomorphic": {
         "poly_modulus_degree": 8192,
         "coeff_mod_bit_sizes": [
           60,
           40,
           40
         ],
         "scale_bits": 40,
         "scheme": "CKKS"
       },
       "dp-adaptive":{
         "num_sampled_clients": 0,
         "init_clip_norm": 0.1,
         "noise_multiplier": 1,
         "server_side_noising": true,
         "clip_count_stddev": null,
         "clip_norm_target_quantile": 0.5,
         "clip_norm_lr": 0.2
       }
     }
   }

The definitions: - **client_type_id** Specifies the ID of the client.
Allows to bypass the plugability modules for the Pytorch builder with
the keyword “base” for testing purposes. - **server_address** The
address of the Flower server that the FL client should try to connect
to. - **eval_metrics** The evaluation metrics which will be gathered
through the evaluation process by the FL client. - **eval_func** The
evaluation function that the model will use as the loss throughout the
training process. - **num_classes** The number of classes in
classification problems. - **num_rounds** The number of rounds that the
training should run for. - **shape** The shape of the data. Currently,
this parameter is recommended to be changed through the ConfigMaps
instead. - **training_id** The id of the training process being
conducted. - **model_name** The name of the model that will be used in
the training. The name should be the same as the one stored in FL
Repository. - **model_version** The version of the model that will be
used in the training. The name should be the same as the one stored in
the FL Repository. - **config** The configuration specifying how the FL
training process will be conducted on the client, containing important
terms such as the batch_size or learning rate. - **optimizer_config**
The configuration of the optimizer. - **optimizer** For the Keras model
and client, the optimizer can be one of:
``python     "sgd": tf.keras.optimizers.SGD,     "rmsprop": tf.keras.optimizers.RMSprop,     "adam": tf.keras.optimizers.Adam,     "adadelta": tf.keras.optimizers.Adadelta,     "adagrad": tf.keras.optimizers.Adagrad,     "adamax": tf.keras.optimizers.Adamax,     "nadam": tf.keras.optimizers.Nadam,     "ftrl": tf.keras.optimizers.Ftrl``
For the PyTorch model and client, the optimizer can be one of:
``python     "adadelta": torch.optim.Adadelta,     "adagrad": torch.optim.Adagrad,     "adam": torch.optim.Adam,     "adamw": torch.optim.AdamW,     "sparseadam": torch.optim.SparseAdam,     "adamax": torch.optim.Adamax,     "asgd": torch.optim.ASGD,     "lbfgs": torch.optim.LBFGS,     "nadam": torch.optim.NAdam,     "radam": torch.optim.RAdam,     "rmsprop": torch.optim.RMSprop,     "rprop": torch.optim.Rprop,     "sgd": torch.optim.SGD``
Other fields indicate the arguments that should be passed to the
optimizer. - **scheduler_config** The configuration of the scheduler. -
**scheduler** For the Keras model and client, the scheduler (or here, a
more appropriate name would be a Keras callback) can be one of:
``python     "earlystopping": tf.keras.callbacks.EarlyStopping,     "reducelronplateau": tf.keras.callbacks.ReduceLROnPlateau,     "terminateonnan": tf.keras.callbacks.TerminateOnNaN``
For the Pytorch model and client, the scheduler can be one of:
``python     "lambdalr": torch.optim.lr_scheduler.LambdaLR,     "multiplicativelr": torch.optim.lr_scheduler.MultiplicativeLR,     "steplr": torch.optim.lr_scheduler.StepLR,     "multisteplr": torch.optim.lr_scheduler.MultiStepLR,     "constantlr": torch.optim.lr_scheduler.ConstantLR,     "linearlr": torch.optim.lr_scheduler.LinearLR,     "exponentiallr": torch.optim.lr_scheduler.ExponentialLR,     "cosineannealinglr": torch.optim.lr_scheduler.CosineAnnealingLR,     "chainedscheduler": torch.optim.lr_scheduler.ChainedScheduler,     "sequentiallr": torch.optim.lr_scheduler.SequentialLR,     "reducelronplateau": torch.optim.lr_scheduler.ReduceLROnPlateau,     "cycliclr": torch.optim.lr_scheduler.CyclicLR,     "onecyclelr": torch.optim.lr_scheduler.OneCycleLR,     "cosineannealingwarmrestarts": torch.optim.lr_scheduler.CosineAnnealingWarmRestarts``
Other fields indicate the arguments that should be passed to the
scheduler. - **warmup_config** The configuration of an (optional)
warmup. This configuration is valid only for the PyTorch builder. It
specifies a special scheduler, which can be used only for a selected
number of epochs to provide warmup throughout the process. -
**scheduler** The name of the scheduler. Other fields indicate the
arguments that should be passed to the scheduler.

-  **privacy-mechanisms** The configuration indicating which privacy
   mechanisms should the FL Training Collector employ (if any) and what
   should be their parameters. This dictionary can have no keys (which
   indicates no privacy mechanisms used), “homomorphic” which indicates
   the use of HE, “dp-adaptive” which indicates the use of Differential
   Privacy with Adaptive Clipping or both “homomorphic” and
   “dp-adaptive”, which indicates that both techniques should be used.

   -  **homomorphic** The parametres configurable to be used for
      homomorphically encrypted federated averaging are used to specify
      the context as described in the
      `TenSEAL <https://github.com/OpenMined/TenSEAL>`__ documentation.
   -  **dp-adaptive** The parametres specifying the differentially
      private Federated Averaging are taken from the Flower library and,
      by proxy, from the `relevant
      paper <https://arxiv.org/pdf/1905.03871.pdf>`__.

A sample test configuration can be seen here:

.. code:: json

   {"client_type_id": "local1",
     "server_address": "trainingcollectorlocal-trainingmain-svc2",
     "eval_metrics": [
       "accuracy"
     ],
     "eval_func": "categorical_crossentropy",
     "num_classes": 10,
     "num_rounds": 15,
     "shape": [
       32, 32, 3
     ],
     "training_id": "10",
     "model_name": "keras_test",
     "model_version": "version_1",
     "config": [
       {"config_id": "min_effort",
      "batch_size": "64",
      "steps_per_epoch": "32",
      "epochs": "1",
      "learning_rate": "0.001"}
     ],
     "optimizer_config": {
       "optimizer": "adam",
       "learning_rate":"0.005",
       "amsgrad":"True"
     },
     "scheduler_config": {
       "scheduler": "reducelronplateau",
       "factor":"0.5",
       "min_delta":"0.0003"
     },
     "privacy-mechanisms":{}}

Developer guide
===============

Components
~~~~~~~~~~

Training Module
^^^^^^^^^^^^^^^

The Local Model Training component is responsible for local model
training. During configuration it instantiates appropriate ML training
libraries and, if this is the beginning of the process, initial version
of the shared model. This step can be completed locally by the node
owner, but this is unlikely. The main priority lies in assuring
uniformity of training methods across nodes belonging to different
owner. The necessary modules (ML algorithm libraries and the initial
version of the shared model) will be downloaded from the FL Repository.

Websockets
''''''''''

A websocket client is running in the background of the trainingapp pod.
Its purpose is to provide a continuous means of communication with the
FL Orchestrator, so that the Orchestrator knows exactly which FL Local
Operations are active and can participate in training. It will try to
connect with the FL Orchestrator server via the
``ORCHESTRATOR_WS_ADDRESS`` address configured in the
``fllocalops-config-map`` ConfigMap. To appropriately change it is then
enough to modify this address with ``kubectl edit cm`` and recreate the
trainingapp pod.

Inference Module
^^^^^^^^^^^^^^^^

The inference component corresponds to the inferenceapp pod and can
function as a standalone. It uses gRPC for lightweight communication. It
allows for the configuration setup through the modification of
configuration files located in the ``configurations`` directory (which
can also be modified on the fly by changing the values in the
``flinference-config-map`` and restarting the pod), as well as the
addition and subtraction of serialized objects from the (they can be
accessed and changed as a Kubernetes volume or downloaded on the fly
from the FL Repository in the case of data transformations and models).
By default, the inference component accepts data in the form of
numerical arrays of any shape and uses a TFLite model to provide
lightweight and fast inference. However, it is possible to change the
input shape and further details with the use of pluggability.

The inference component is, by default, installed with the rest of the
Helm chart. Then it can be accessed through service
``fllocaloperationslocal-inferenceapp`` on port ``50051`` according to
the specification located in
``inference_application/code/proto/basic-inference.proto``.

Data Transformation module
^^^^^^^^^^^^^^^^^^^^^^^^^^

In IoT ecosystems, each partner may (and is likely to) store data in its
own (private/local) format. Use of FL requires transformation of
appropriate parts of local data into the correct format. This format has
to be described as part of the FL configuration, and all participating
nodes have to oblige. This may be achieved by node owner providing a set
of the appropriate transformation components, that applied in a certain
order may allow for data format unification. However, such components
have to be flexibly downloaded from the FL Repository enabler.

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

In order to generate a new set of keys, you can use the file
``application/generate_homomorphic_keys.py``. If a new set of keys is
generated, the ``application/src/custom_clients/hm_keys/public.text``
and ``application/src/custom_clients/hm_keys/secret.text`` files should
be appropriately changed (and potentially modified to be a Kubernetes
secret).

**Attention**: As an extremely computationally expensive method, it can
usually be used only for the simplest of methods and datasets. Therefore
it is not recommended in this implementation to use it for models more
complicated than a simple Linear Regression.

Pluggable modules
-----------------

The trainingapp component suports FL training with the use of Keras and
Pytorch libraries out of the box. Similarly, the inferenceapp component
supports the inference with the TFLite inferencer. However, it is
possible to develop custom components for: - in the case of trainingapp:
- FL client - FL model - FL data loader - FL data transformations - in
the case of inferenceapp: - gRPC service along with the proto and
protocompiled files - inferencer - model.

In order to deploy the image with your custom components through the use
of Kubernetes volume, change the ``custom_setup`` field in
``values.yaml`` to ``True``. ### Tutorial

Model
^^^^^

1. Uploading a new FL model.

A new FL model can be saved either in a format ready for FL Training in
Keras, Pytorch, or FL inference in TFLite. For Keras, the method used
should be:

.. code:: python

   model.save('model')

Then, the file should be compressed to a ZIP format in order to save
space, for example using this snippet of code:

.. code:: python

   with zipfile.ZipFile('keras_test_model.zip', 'w') as f:
       upper_dir = pathlib.Path("model/")
       for file in upper_dir.rglob("*"):
           f.write(file)

A model for the Pytorch pipeline should be saved using this snippet
(preferably with the same file name):

.. code:: python

   torch.jit.save(m, 'scripted_model,pt')

And a model for TFLite inference needs to be served in a TFLite format.
Both Pytorch and TFLite models should be compressed before uploading
them to the FL Repository, similarly to the Keras model. They can be
uploaded using the Swagger API of the FL Repository, by first creating
the metadata of the model and then uploading a file by updating the
object for a given metadata.

2. Loading the weights from the training results for a given FL model.

I will demonstrate it on a toy Keras example.

First, we should download from the FL Repository the underlying model
(if you have saved the model elsewhere the step can be skipped).

.. code:: python

   with requests.get(f"http://{REPOSITORY_URL}/model"
                                 f"/keras_test/version_1",
                                 stream=True) as r:
       with open(f'temp.zip', 'wb') as f:
               shutil.copyfileobj(r.raw, f)
   with ZipFile(f'temp.zip', 'r') as zipObj:
       # Extract all the contents of zip file in current directory
       zipObj.extractall(f'temp')

Then, the model has to be loaded. In order to deal with different levels
of nesting from the downloaded ZIP files, I’m using a helpful script:

.. code:: python

   def check_loading_path(temp):
       '''Checks how nested was the zipped file in order to load it correctly'''
       nested_files = os.listdir(temp)
       if len(nested_files) == 1 and os.path.isdir(os.path.join(temp, nested_files[0])):
           return check_loading_path(os.path.join(temp, nested_files[0]))
       else:
           return temp

   load_path = check_loading_path('temp')
   model = keras.models.load_model(load_path)

Finally, we have to download the selected weights. **Attention**: Make
sure that the Python version of the environment you’re loading the
pickle file in is compatible with the FL Training Collector, which means
Python 3.8.3.

.. code:: python

   with requests.get(f"http://{REPOSITORY_URL}/training-results/weights"
                                 f"/keras_test/version_1/13",
                                 stream=True) as r:
       with open(f'temp2.pkl', 'wb') as f:
               shutil.copyfileobj(r.raw, f)
   with open('temp2.pkl', 'rb') as pickle_file:
       weights = pickle.load(pickle_file)

After unpickling we’re ready to set the weights.

.. code:: python

   model.set_weights(weights)

Data transformation
^^^^^^^^^^^^^^^^^^^

We will be demonstrating how to construct and configure the loading of a
data transformation for the inference module.

**Attention**: To do so, first make sure that the environment you’re
using has a Python version compatible with the inference module, that
is, 3.11.4. Otherwise, you may encounter problems related to pickle
magic numbers.

First, let’s design the transformation. Here is a sample data
transformation:

.. code:: python

   from data_transformation.transformation import DataTransformation
   from datamodels.models import MachineCapabilities


   import numpy as np

   class BasicDimensionExpansionTransformation(DataTransformation):
       import numpy as np

       id = "basic-expand-dimensions"
       description = """Basically a wrapper around numpy.expand_dims. 
       Expands the shape of the array by inserting a new axis, that will appear at the axis position in expanded array shape"""
       parameter_types = {"axis": int}
       default_values = {"axis": 0}
       outputs = [np.ndarray]
       needs = MachineCapabilities(preinstalled_libraries={"numpy": "1.23.5"})

       def set_parameters(self, parameters):
           self.params = parameters

       def get_parameters(self):
           return self.params

       def transform_data(self, data):
           data = np.array(data)
           return np.expand_dims(data, axis=self.params["axis"])

       def transform_format(self, format):
           if "numerical" in format["data_types"]:
               axis = self.params["axis"]
               format["data_types"]["numerical"]["size"].insert(axis, 1)
           return format

The new data transformation class should be a subclass of the abstract
DataTransformation class from the data_transformation module. It should
have a unique id, a description of purpose, a dictionary of parameter
types, a dictionary of default values, a list of output types and a
MachineCapabilities object that expresses what needs to be present in
the Docker container/on the machine to run this transformation.

If you have this transformation ready, you should put it, for example,
in the ``inference_application/custom`` directory in the FL Local
Operations repository and use a different file to properly serialize the
modules. Like this:

.. code:: python

   with zipfile.PyZipFile("inference_application.custom.expansion.zip", mode="w") as zip_pkg:
        zip_pkg.writepy("inference_application/custom/expansion.py")

   with open('inference_application.custom.expansion.pkl', 'wb') as f:
       dill.dump(BasicDimensionExpansionTransformation,f)

For serializing this data, both zipimport and dill were used to make
sure that even the most complicated transformations will be possible to
load. Just remember to name the files according to the paths to the
modules you would like to serialize (just replace the “/” with the “.”).

Then, you can either zip the two resulting files and upload them to the
FL Repository as a transformation, or place the files in the
``inference_application/local_cache/transformations`` directory, either
by building a new image or deploying the Helm chart with the
``customSetup`` field marked to true in ``values.yaml`` file for the
inference application and using ``kubectl cp`` to place the files.

Finally, you can apprioprately change the inference application
configuration to use that specific transformation with selected
parameters. You can do it by modifying the appropriate ConfigMap.

.. code:: json

   [
       {
           "id": "inference_application.custom.basic_norm",
           "parameters": {

           }
       },
       {
           "id": "inference_application.custom.expansion",
           "parameters": {
               "axis": 0

           }
       }
   ]

If you just want to reuse an existing transformation, it’s enough to
only modify the configuration. The serialization of data transformations
for the FL Training Collector is very similar, but necessitates the use
of Python 3.8.3

For the extended documentation on how to develop other pluggable modules
based on some examples, please send me an
`email <mailto:bogacka@ibspan.waw.pl>`__

Technologies
~~~~~~~~~~~~

scikit-learn
^^^^^^^^^^^^

A popular machine learning library often used for data preprocessing and
transformation, for example encoding labels. It is open source and
widely used in the industry.

pyTorch
^^^^^^^

An open source machine learning framework based on the Torch library,
used for applications such as computer vision and natural language
processing, primarily developed by Facebook’s AI Research lab (FAIR).

Python
^^^^^^

Python is an interpreted high-level general-purpose programming language
with a set of libraries. Very popular for data analysis and ML
applications.

TensorFlow
^^^^^^^^^^

A free and open-source software library for machine learning and
artificial intelligence. It can be used across a range of tasks but has
a particular focus on training and inference of deep neural networks.

Tensorflow Lite
^^^^^^^^^^^^^^^

A mobile library allowing for easy, lightweight deployment of ML models
on mobile, microcontrollers and edge device. It employs, for example,
quantization in order to decrease the resources consumed by the model
during inference.

Flower
^^^^^^

A federated learning framework designed to work with a large number of
clients. It is both compatible with a variety of ML frameworks and
supports a wide range of devices.

OpenCV
^^^^^^

A real-time computer vision library providing already optimized models.
It is cross-platform and open-source.

TenSEAL
^^^^^^^

A library that empowers users to easily conduct Homomorphic Encryption
operations on tensors, built on top of Microsoft SEAL. Since the
underlying implementation uses C++, the resulting methods consume as
little resources as possible.

gRPC
^^^^

A modern open source, high performance Remote Procedure Call (RPC)
framework. gRPC works across many languages and platforms, is
exceptionally efficient and scalable.

FastAPI
^^^^^^^

A popular web microframework written in Python, FastAPI is known for
being both robust and high performing. It is based on OpenAPI
(previously Swagger) standards.

Prometheus metric monitoring
============================

The Prometheus metrics are available for scraping on the the port
``9050`` under url ``/metrics`` on the trainingapp, and on the port
``9000`` without any additional url path changes in the inferenceapp.

Licence
=======

The FL Local Operations is released under the Apache 2.0 license, as we
have internally concluded that we are not “offering the functionality of
MongoDB, or modified versions of MongoDB, to third parties as a
service”. However, potential future commercial adopters should be aware
that our project uses MongoDB in order to be able to accurately
determine the license most applicable to their projects.

You may obtain a copy of the License at:
http://www.apache.org/licenses/LICENSE-2.0

Authors
=======

-  Karolina Bogacka
-  Piotr Sowiński
-  Jose Antonio Clemente Perez

Notice (dependencies)
=====================

The information about the dependencies needed to run a specific part of
the application can be found described in the appropriate
``requirements.txt`` files located. However, since they are downloaded
automatically during the construction of the appropriate Docker images,
the local dependencies needed to deploy the application include only a
local Docker along with Docker Compose or Kubernetes installation.



