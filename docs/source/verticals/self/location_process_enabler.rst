.. _Location processing:

###########################
Location Processing Enabler
###########################

.. contents::
  :local:
  :depth: 1

Documentation for the Location Processing enabler of ASSIST-IoT.

***************
Introduction
***************

The Location Processing enabler aims to provide highly configurable and
flexible geofencing capabilities based on location data. The enabler
consists of a Scala application and a Postgres database.

The application is written with the Akka framework to provide
scalability and durability. It runs user-defined SQL queries against the
database. The incoming data is collected from input streams or HTTP
requests; it allows for streaming the query results. The transferred
data is in JSON format. The behavior of the application is configurable
through an HTTP interface. The application streaming capabilities are
compatible with the MQTT protocol.

The database is shipped with the Postgis extension. It stores the
geolocation data and the application configuration.

***************
Features
***************

The enabler is still under development. Missing functionalities are in
italics.

Input stream settings
^^^^^^^^^^^^^^^^^^^^^

-  Passing credentials
-  Setting input topics
-  *Providing MQTT connection URL*

Output stream settings
^^^^^^^^^^^^^^^^^^^^^^

-  Passing credentials
-  Setting parametrized1 output topics
-  Setting MQTT publish flags (at least once delivery, at most once
   delivery, exactly once delivery, *retain*)
-  *Providing MQTT connection URL*
-  *Custom output JSON format*

SQL queries
^^^^^^^^^^^

-  Access to a database with geolocation capabilities
-  Query parametrization1

HTTP interface
^^^^^^^^^^^^^^

-  Creating queries
-  Updating queries
-  Deleting queries
-  Retrieving queries
-  *Running queries manually*
-  *Authorization*

1 Parametrization refers to access to input or output data in JSON (with
`JSONPath <https://support.smartbear.com/alertsite/docs/monitors/api/endpoint/jsonpath.html>`__),
string, or byte string format. To do that, a special syntax is provided.
*********************
Place in architecture
*********************

For ASSIST-IoT Pilot it will be closely used with Location Trackin
EnBLER

***************
User guide
***************
The user-defined queries can be created via the HTTP interface. After
successful creation, a query is stored in the database. Then, it is run
inside the application, and it starts processing the data.

It is assumed that the spatial model will be specified inside the
database before starting the application. So that queries have access to
the required tables and data.



User guide HTTP interface
=========================

Definitions
-----------

Parametrized string (*parametrizedString*)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

String (optionally) containing parametrization syntax.

*Examples:*

``"topic_{output['id']}"``

``"positions"``

MQTT publish flag (publishFlag)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

One of the following strings: - QoSAtLeastOnceDelivery -
QoSAtMostOnceDelivery - QoSExactlyOnceDelivery

*Examples:*

``"QoSAtLeastOnceDelivery"``

Input settings (*inputSettings*)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

MQTT input settings.

=================== ======================== =============
Name                Description              Type
=================== ======================== =============
username *optional* Client credentials       string
password *optional* Client credentials       string
topics *optional*   MQTT topics to subscribe array[string]
=================== ======================== =============

*Examples:*

.. code:: json

   {
     "username": "jared",
     "password": "dunn",
     "topics": ["vehicles/excavators", "cats"]
   }

Output settings (*outputSettings*)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

MQTT output settings.

======================= ====================== =========================
Name                    Description            Type
======================= ====================== =========================
username *optional*     Client credentials     string
password *optional*     Client credentials     string
topics *optional*       MQTT topics to publish array[parametrizedString]
publishFlags *optional* MQTT publish flags     array[publishFlag]
======================= ====================== =========================

*Examples:*

.. code:: json

   {
     "username": "bob",
     "password": "builder",
     "topics": ["danger/{output['id']}"],
     "publishFlags": ["QoSExactlyOnceDelivery", "Retain"]
   }

Query (*query*)
~~~~~~~~~~~~~~~

Query configuration.

========================= ================= ==================
Name                      Description       Type
========================= ================= ==================
name *required*           Unique query name string
inputSettings *optional*  Input settings    inputSettings
outputSettings *optional* Output settings   outputSettings
sql *required*            SQL query         parametrizedString
========================= ================= ==================

.. code:: json

   {
     "name": "dangerous",
     "inputSettings": {
       "username": "jared",
       "password": "dunn",
       "topics": ["vehicles/excavators", "cats"]
     },
     "outputSettings": {
       "username": "bob",
       "password": "builder",
       "topics": ["danger/{output['id']}"],
       "publishFlags": ["QoSExactlyOnceDelivery", "Retain"]
     },
     "sql": "select id, x, y from worker_positions where st_distance(st_makepoint(x, y), st_makepoint({input['x']}, {input['y']})) < 50;"
   }

Endpoints
---------

GET ``v1/queries``
~~~~~~~~~~~~~~~~~~

Retrieves all queries.

Parameters: *none*.

Body: *none*.

Returns: - Status code 200, body:

.. code:: json

   {
     "queries": [
       {...},
       {...}
     ]
   }

GET ``v1/queries/{name}``
~~~~~~~~~~~~~~~~~~~~~~~~~

Retrieves the query with ``name``.

Parameters: - ``name``: query name

Body: *none*.

Returns: - On success - status code 200, body:

.. code:: json

   {
     "query": {
       ...
     }
   }

-  If query does not exist - status code 404, body:

.. code:: json

   {
     "description: "..."
   }

POST ``v1/queries``
~~~~~~~~~~~~~~~~~~~

Creates a query.

Parameters: *none*.

Body: - query

.. code:: json

   {
     "name": ...,
     "inputSettings": ...,
     "outputSettings": ...,
     "sql": ...

Returns: - On success - status code 201, body:

.. code:: json

   {
     "query": {
       ...
     }
   }

-  On error - status code 400, body:

.. code:: json

   {
     "description: "..."
   }

PUT ``v1/queries/{name}``
~~~~~~~~~~~~~~~~~~~~~~~~~

Updates the query with ``name``.

Parameters: - ``name``: query name

Body: - query

.. code:: json

   {
     "name": ...,
     "inputSettings": ...,
     "outputSettings": ...,
     "sql": ...
   }

Returns: - On success - status code 200, body:

.. code:: json

   {
     "query": {
       ...
     }
   }

-  On error - status code 400, body:

.. code:: json

   {
     "description: "..."
   }

DELETE ``v1/queries/{name}``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Deletes the query with ``name``.

Parameters: - ``name``: query name

Body: *none*.

Returns: - On success - status code 200, empty body



User guide parametrization
==========================

Parametrization is a feature that gives access to the incoming data and
the results of running queries. For defining SQL queries, input data is
available. Output MQTT topics have access to input and output data.

Input data
~~~~~~~~~~

-  ``input`` JSON data
-  ``strInput`` JSON data in string format
-  ``byteStrInput`` JSON data in byte string format

Output data
~~~~~~~~~~~

-  ``output`` JSON data
-  ``strOutput`` JSON data in string format
-  ``byteStrOutput`` JSON data in byte string format

To access JSON data (``input`` or ``output``) one may use
`JSONPath <https://support.smartbear.com/alertsite/docs/monitors/api/endpoint/jsonpath.html>`__
syntax.

A valid expression must be inside curly braces ``{...}``.

*Examples:*

``"select {strInput}::json->>2;"``

``"topic/{output..temperature.max()}"``

***************
Prerequisites
***************
-  `Docker <https://www.docker.com/>`__
-  `Docker compose <https://docs.docker.com/compose/>`__



Scala
~~~~~

`Scala <https://www.scala-lang.org/>`__ is a language of preference for
the SRIPAS group. Scala provides support for functional idioms and
static typing. Those two features and familiarity with the language are
arguments for Scala in the IoT environment, to support high reliability
demand of the business.

PostGIS
~~~~~~~

PostGIS is a spatial database extender for PostgreSQL object-relational
database.

REST (Enabler’s API)
~~~~~~~~~~~~~~~~~~~~

Currently it is decided as project-wide standard. REST is overall a web
standard.

***************
Installation
***************
Will be determined after the release of the enabler.

*********************
Configuration options
*********************
Will be determined after the release of the enabler.

***************
Developer guide
***************
Will be determined after the release of the enabler.

***************************
Version control and release
***************************

We will use gitlab as version control and release tooling.

***************
License
***************
The Location Processing is licensed under the **Apache License, Version
2.0** (the “License”).

One may obtain a copy of the License at
http://www.apache.org/licenses/LICENSE-2.0
***************
Notice (dependencies)
***************
Dependency list and licensing information will be provided before the
first major release.



