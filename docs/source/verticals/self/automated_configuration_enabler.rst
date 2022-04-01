.. _Automated Configuration enabler:

###############################
Automated Configuration enabler
###############################

.. contents::
  :local:
  :depth: 1

Automated configuration_enabler
===============================

Introduction
------------

Automated Configuration Enabler keeps heterogenous devices and services
synchronised with their configurations. User can update configuration
and define fallback configurations in case of errors. Self-\* component
will be responsible for reacting to changing environment and updating
configura-tion as necessary

Features
--------

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

Place in architecture
---------------------

User guide
----------

TBD

Prerequisites
-------------

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

Installation
------------

TBD

Configuration options
---------------------

TBD

Developer guide
---------------

TBD

Version control and release
---------------------------

We will use gitlab as version control and release tooling.

License
-------

TBD



