.. _Automated Configuration enabler:

###############################
Automated Configuration enabler
###############################

.. contents::
  :local:
  :depth: 1

Automated configuration_enabler
===============================

***************
Introduction
***************

Automated Configuration Enabler keeps heterogenous devices and services
synchronised with their configurations. User can update configuration
and define fallback configurations in case of errors. Self-\* component
will be responsible for reacting to changing environment and updating
configura-tion as necessary

***************
Features
***************

Automated configuration
~~~~~~~~~~~~~~~~~~~~~~~

-  Enabler keeps heterogenous devices and services synchronised with
   their configurations.
-  User can update configuration and define its fallback versions in
   case of errors. Self-\* component will detect if fallback
   configuration should be used.
-  Self-\* component will be responsible for reacting to changes in the
   environment and updating configuration as necessary/required.

Connection of heterogenous devices
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

-  Various devices, groups of devices, services and other enablers will
   have uniform API to communicate with the Enabler.



***************
User guide
***************

What this Enabler is all about?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Detailed explanation of the Enabler is available within this document -
`self_config.pdf <uploads/e60e6c6fc2604348f691824fe7543df5/self_config.pdf>`__

HTTP interface - administration
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Requirements
^^^^^^^^^^^^

This interface consists of two endpoints for creating and deleting
requirements:

::

   DELETE {root}/requirements-model/{requirement_id}

::

   POST {root}/requirements-model

   {
     "id" : String,
     "labels" : LabelMap,
     "requirements" : [FunctionalityRequirement],
     "weight" : Number
   }

Sample:

::

   {
     "id" : "test1",
     "labels" : {
       "key1" : "value1"
     },
     "requirements" : [
       {
         "id" : "test2",
         "exclusive" : false
       },
       {
         "labelKey" : "key2",
         "labelValue" : "value2",
         "count" : 3,
         "exclusive" : true
       }
     ],
     "weight" : 3.0
   }

Requirements JSON entities
''''''''''''''''''''''''''

``LabelMap``
            

A ``LabelMap`` is a mapping of label names to their values, used to
verify requirements. It has the following format:

::

   {
     "label_name" : "label_value"
   }

``FunctionalityRequirement``
                            

This entity describes a requirement for specific functionality,
represented by a requirements model. There are two types of
requirements: id-based and label-based.

-  Id-based: Requires a resource with a specified id to be available.

::

   {
     "id" : "test2",
     "exclusive" : false
   }

-  Label-based: Requires a resource with a specific label key and value
   to be available. The count parameter specifies how many entities are
   needed.

::

   {
     "labelKey" : "key2",
     "labelValue" : "value2",
     "count" : 3,
     "exclusive" : true
   }

Both types include an exclusive parameter, which determines if the
resource or functionality can be shared with other requirements.

``RequirementsModel``
                     

::

   {
     "id" : String,
     "labels" : LabelMap,
     "requirements" : [FunctionalityRequirement],
     "weight" : Number
   }

-  id (String): A unique identifier for the requirements model. Needs to
   be unique across requirements and resources.
-  labels (LabelMap): A mapping of label names to their values, used for
   verifying the requirements. The format of a LabelMap is a JSON object
   with key-value pairs, where the key is the label name and the value
   is the label value.
-  requirements (Array of FunctionalityRequirement): An array of
   FunctionalityRequirement objects, which describe specific
   functionality requirements needed in the requirements model. Each
   FunctionalityRequirement can either be id-based or label-based, and
   includes an exclusive parameter to indicate if the resource or
   functionality can be shared with other requirements.
-  weight (Number): A numeric value representing the weight or priority
   of the requirements model.

Reactions
^^^^^^^^^

This interface consists of two endpoints for creating and deleting
reactions:

::

   DELETE {root}/reaction-model/{reaction_id}

::

   POST {root}/reaction-model

   {
     "reactionId": String,
     "filterExpression": FilterExpression,
     "action": ReactionAction
   }

Reaction JSON entities
''''''''''''''''''''''

``FilterExpression``
                    

Please note that *filtering* happens with messages that are incoming via
Kafka.

``FilterExpression`` dictates *when* (or under what conditions) reaction
should be triggered. There are six types in total: -
``ResourceIsAvailable`` reaction will be triggered when resource with a
specific id will be available.

::

   "filterExpression": {
     "messageType": "ResourceIsAvailable",
     "id": "element-id-1",
   }

-  ``ResourceIsNoLongerAvailable`` reaction will be triggered when
   resources with a specific id is no longer available.

::

   "filterExpression": {
     "messageType": "ResourceIsNoLongerAvailable",
     "id": "element-id-1",
   }

-  ``ResourceWithLabelIsAvailable`` reaction will be triggered when
   resource with specific label is available.

::

   {
     "messageType": "ResourceWithLabelIsAvailable",
     "labelKey": "configuration_step",
     "labelValue": "not_configured"
   }

-  ``ResourceWithLabelIsNoLongerAvailable`` reaction will be triggered
   when resource with specific label is no longer available.

::

   {
     "messageType": "ResourceWithLabelIsNoLongerAvailable",
     "labelKey": "configuration_step",
     "labelValue": "not_configured"
   }

-  ``AnyEvent`` any event will trigger a reaction

::

   {
     "messageType": "AnyEvent"
   }

-  ``CustomMessageContent`` only message with specific, predetermined
   content will be triggered.

::

   {
     "messageType": "CustomMessageContent",
     "content": "fire"
   }

Reaction will be triggered when following message will be sent via Kafka
topic:

::

   {
     "messageType": "RegisterResource",
     "content": "fire"
   }

``ReactionAction``
                  

This entity defines what *action* should be taken after an event was
positively filtered by ``FilterExpression``. There are six reactions
available: - ``SendSimpleKafkaMessage`` sends a message on specified
kafka topic:

::

   {
     "message": "message",
     "topic": "topic"
   }

Kafka message will have following format:

::

   {
     "trigger": String,
     "content": String
   }

-  ``ReplaceConfiguration`` completely replaces current set of
   ``RequirementsModel``.

::

   {
     "requirements": [RequirementsModel]
   }

-  ``UpsertConfiguration`` either updates and/or inserts non-existing
   requirements. If ``removeDangling`` is set to true, then it removes
   ``RequirementsModel`` that are not directly mentioned in the request
   (as requirement or dependency).

::

   {
     "requirements": [RequirementsModel],
     "removeDangling": Boolean
   }

-  ``ConditionalAction`` will either execute ``action`` if
   ``conditionalCheck`` is met, ``fallback`` otherwise.

::

   {
     "conditionalCheck": Condition,
     "action": ReactionAction,
     "fallback": ReactionAction
   }

-  ``KeepHighestWeightFunctionalities`` ensures that requirements with
   highest weight are met given available resources.

::

   "KeepHighestWeightFunctionalities"

-  ``NoAction`` self explanatory.

::

   "NoAction"

   ###### `ReactionModel`

{ “reactionId”: String, “filterExpression”: FilterExpression, “action”:
ReactionAction }

::


   ### Kafka interface - interaction

   Kafka interface is able to consumes three types of message. 

   #### `RegisterResource`

{ “messageType”: “RegisterResource”, “resource”: { “id”: String,
“labels”: LabelMap } }

::


   #### `RegisterResource`

{ “messageType”: “RegisterResource”, “resource”: { “id”: String,
“labels”: LabelMap } }

::


   #### `DeregisterResource`

{ “messageType”: “DeregisterResource”, “resource”: { “id”: String,
“labels”: LabelMap } }

::


   #### `CustomMessage`

| { “messageType”: “CustomMessage”, “content”: String }
| \``\`

Prerequisites
***************

Scala
~~~~~

`Scala <https://www.scala-lang.org/>`__ is a language of preference for
the SRIPAS group. Scala provides support for functional idioms and
static typing. Those two features and familiarity with the language are
arguments for Scala in the IoT environment, to support high reliability
demand of the business.

Akka
~~~~

`Akka <https://akka.io/>`__ is a Scala library supporting Actor
concurrency model. This library is a de facto standard for creating
concurrent and/or distributed systems in Scala. Among others, Akka
provides connectors for
`REST <https://doc.akka.io/docs/akka-http/current/introduction.html>`__,
`MQTT <https://doc.akka.io/docs/alpakka/current/mqtt.html>`__,
`Kafka <https://doc.akka.io/docs/alpakka-kafka/current/home.html>`__,
`gRPC <https://doc.akka.io/docs/akka-grpc/current/index.html>`__. Akka
seems like a natural fit for heterogenous and distributed environment of
IoT.

Kafka
~~~~~

`Kafka <https://kafka.apache.org/>`__ is an open-source, distributed
event streaming platform used by thousands of companies for
high-performance data pipelines, streaming analytics, data integration,
and mission-critical applications. Kafka’s high reliability seems like a
good fit for internal component communication. Its large number of
available connectors will also help with various analytical needs we
might have.

MQTT
~~~~

`MQTT <https://mqtt.org/>`__ is an
`OASIS <https://en.wikipedia.org/wiki/OASIS_(organization)>`__ standard
messaging protocol for the IoT. It is designed as an extremely
lightweight publish/subscribe messaging transport that is ideal for
connecting remote devices with a small code footprint and minimal
network bandwidth. Today, MQTT is used in a wide variety of industries,
such as automotive, manufacturing, telecommunications, oil and gas, etc.

MQTT provides IoT specific features like `Last Will and
Testament <https://www.hivemq.com/blog/mqtt-essentials-part-9-last-will-and-testament/>`__.
`PAHO <https://www.eclipse.org/paho/>`__ provides a broad range of MQTT
clients.

REST (Enabler’s API)
~~~~~~~~~~~~~~~~~~~~

Currently it is decided as project-wide standard. REST is overall a web
standard.

***************************
Version control and release
***************************

We will use gitlab as version control and release tooling.

***************
License
***************
Will be determined after the release of the enabler.



