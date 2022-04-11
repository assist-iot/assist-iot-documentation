.. _Semantic Annotation Enabler:

###########################
Semantic Annotation Enabler
###########################

.. contents::
  :local:
  :depth: 1

Home
====

ASSIST-IoT Semantic Annotation Enabler Repository Enabler.



introduction
============

This enabler offers a service of syntactic transformation of JSON, CSV
and XML data formats into RML, also known as semantic lifting, or
semantic annotation.

Two methods of annotation are supported: one-time through a REST API,
and message-based through a persistent stream.

Annotations are configured using the `RML <https://rml.io/specs/rml/>`__
language.

In the first release, the REST API, with (optional) helper web GUI is
supported, as well as tentative streaming infrastructure on Apache
Flink. Final version will include a streaming processor for Kafka/MQTT
with persistent annotation channels.



features
========

Features



place in architecture
=====================

Place in architecture



user guide
==========

User guide



prerequisites
=============

The Semantic Annotator Enabler has no particular requirements to run,
but practical usage requires familiarity with the
`RML <https://rml.io/specs/rml/>`__ language.



installation
============

Current version requires `docker <https://www.docker.com/>`__ and
`docker-compose <https://docs.docker.com/compose/>`__, and is installed
by running the ASSIST_RML/docker-compose.yml file.

Build and run:

``cd ASSIST_RML``

``docker-compose up --build``

This creates the following services:

-  RML Mapper REST - Swagger at http://localhost:4000/
-  Matery YARRML helper editor at http://localhost:5000/
-  Apache Flink - Web interface at http://localhost:8081/

   -  Use RMLStreamer jar from `this
      link <https://github.com/RMLio/RMLStreamer/releases/download/v2.2.2/RMLStreamer-2.2.2.jar>`__

-  Kafka broker at localhost:9093

Note, that streaming with Apache Flink is set up temporarily, and will
be substituted with a custom Kafka/MQTT streaming solution in the
future.



configuration
=============

Currently configuration of the enabler is limited to setting environment
variables in the docker-compose.yml file. If necessary, exposed ports
may be configured there.



developer guide
===============

The Semantic Annotator Enabler is a combination of software written in
different technologies.

The one-time translation depends on: - `RML
Mapper <https://github.com/RMLio/rmlmapper-java>`__ - `RML
webapi <https://github.com/RMLio/rmlmapper-webapi-js>`__ -
`Matey <https://github.com/RMLio/matey>`__

Please, refer to the documentation for individual software to learn more
about development.

The streaming component is built with
`Scala <https://www.scala-lang.org/>`__ using `Akka
Streams <https://doc.akka.io/docs/akka/current/stream/index.html>`__ and
`Akka Http <https://doc.akka.io/docs/akka-http/current/index.html>`__ -
parts of the `Akka <https://akka.io/>`__ framework, and depends
primarily on `Carml <https://github.com/carml/carml>`__ to process RML
files.



version control and releases
============================

0.25 (Mar 2022) - added documentation and examples 0.20 (Mar 2022) -
added GUI editor 0.10 (Feb 2022) - initial release with REST API



license
=======

The Semantic Annotator is licensed under the Apache License, Version 2.0
(the “License”).

You may obtain a copy of the License at: `Apache License
2.0 <http://www.apache.org/licenses/LICENSE-2.0>`__

RML Language and all relevant software, documentation, and reference
examples are licensed under MIT License.

You may obtain a copy of the License at: `MIT
License <https://mit-license.org/>`__



notice (dependencies)
=====================

The Semantic Annotator Enabler is packaged to be available for use
without any external dependencies. However, depending on configuration,
it may use components outside of what is packaged. This pertains in
particular to streaming brokers for Kafka and MQTT. A broker is required
for the Enabler to support streaming annotation. To use a broker
different, than the ones provided in the package, simply configure the
relevant ports to point to Kafka or MQTT brokers already configured in
your network. Note, that the streaming annotation with Kafka/MQTT is
supported in the final release and missing from the initial release.

Included in the Enabler are RML software and libraries, including `RML
Mapper <https://github.com/RMLio/rmlmapper-java>`__, `RML
webapi <https://github.com/RMLio/rmlmapper-webapi-js>`__, and
`Matey <https://github.com/RMLio/matey>`__ for one-time translation, and
`Carml <https://github.com/carml/carml>`__ for streaming translation.

For more information about development libraries dependencies, see
`Developer guide <developer-guide>`__.



