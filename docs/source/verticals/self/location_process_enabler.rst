.. _Location processing:

###################
Location processing
###################

.. contents::
  :local:
  :depth: 1

Documentation for the Location Processing enabler of ASSIST-IoT.



Introduction
============

The Location Processing enabler aims to provide highly configurable and
flexible geofencing capabilities based on location data. The enabler
consists of a Scala application and a Postgres database.

The application is written with the Akka framework. It runs user-defined
SQL queries against the database. The incoming data is collected from
input streams or HTTP requests; it allows for streaming the query
results. The transferred data is in JSON format. The behavior of the
application is configurable through an HTTP interface. The application
streaming capabilities are compatible with the MQTT protocol.

The database is shipped with the Postgis extension. It stores the
geolocation data and the application configuration.



Features
========

Input stream settings
^^^^^^^^^^^^^^^^^^^^^

-  Passing credentials
-  Setting input topics
-  Providing MQTT connection URL

Output stream settings
^^^^^^^^^^^^^^^^^^^^^^

-  Passing credentials
-  Setting parametrized1 output topics
-  Setting MQTT publish flags
-  Providing MQTT connection URL
-  Custom output JSON format

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
-  Running queries manually

1 Parametrization refers to access to input or output data in JSON (with
`JSONPath <https://support.smartbear.com/alertsite/docs/monitors/api/endpoint/jsonpath.html>`__),
string, or byte string format. To do that, a special syntax is provided.



Place in architecture
=====================

The data management plane.



User guide
==========

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

MQTT publish flag (*publishFlag*)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

One of the following strings:

-  QoSAtLeastOnceDelivery
-  QoSAtMostOnceDelivery
-  QoSExactlyOnceDelivery
-  Retain

*Examples:*

``"QoSAtLeastOnceDelivery"``

When to publish (*publishWhen*)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Determines when to publish the produced output.

One of the following strings: - success - failure - always

``failure`` refers to the situation if an error has occured during
processing the stream.

*Examples:*

``"always"``

Record format (*recordFormat*)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Determines the records formatting. Two styles are enabled – ``array``
and ``object``.

``array`` formatting:

.. code:: python

   {
     "fields": [
       {"name": "field_1", "type", "type_1"},
       ...
     ],
     "records": [
       [value_1_1, value_1_2, ..., value_1_n],
       [value_2_1, value_2_2, ..., value_2, n],
       ...
     ]
   }

``object`` formatting:

.. code:: python

   {
     "fields": [
       {"name": "field_1", "type", "type_1"},
       ...
     ],
     "records": [
       {"field_1": value_1_1, "field_2": value_1_2, ..., "field_n": value_1_n},
       {"field_1": value_2_1, "field_2": value_2_2, ..., "field_n": value_2_n},
       ...
     ]
   }

*Examples:*

``"array"``

Output JSON format (*jsonFormat*)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

JSON format for the output data.

================ ========================================= ============
Name             Description                               Type
================ ========================================= ============
recordFormat     Determines the records formatting         recordFormat
showHeader       Whether to show the header                boolean
wrapSingleColumn Whether a single column should be wrapped boolean
================ ========================================= ============

*Examples:*

.. code:: python

   {
     "recordFormat": "object",
     "showHeader": true,
     "wrapSingleColumn": true
   }

Input topic (*inputTopic*)
~~~~~~~~~~~~~~~~~~~~~~~~~~

Topic to subscribe to.

==== =========== ======
Name Description Type
==== =========== ======
name Topic name  string
==== =========== ======

*Examples:*

.. code:: python

   {
     "name": "vehicles/excavators"
   }

Output topic (*outputTopic*)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Topic where the output is published.

=============================== =============================== ==================
Name                            Description                     Type
=============================== =============================== ==================
name                            Topic name                      string
publishEmptyOutput \ *optional* Whether to publish empty output boolean
publishWhen \ *optional*        When to publish                 publishWhen
publishFlags \ *optional*       Publish flags                   array[publishFlag]
=============================== =============================== ==================

.. code:: python

   {
     "name": "cats",
     "publishFlags": ["QoSExactlyOnceDelivery", "Retain"],
     "publishWhen": "success",
     "publishEmptyOutput": false
   }

Input settings (*inputSettings*)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

MQTT Input Settings
===================

+---------+---------------------+------------+
| Name    | Description         | Type       |
+=========+=====================+============+
| host    | MQTT host           | string     |
+---------+---------------------+------------+
| port    | MQTT port           | number     |
+---------+---------------------+------------+
| username| Client credentials  | string     |
|         | (optional)          |            |
+---------+---------------------+------------+
| password| Client credentials  | string     |
|         | (optional)          |            |
+---------+---------------------+------------+
| topics  | MQTT topics to      | array[inpu |
|         | subscribe           | tTopic]    |
|         | (optional)          |            |
+---------+---------------------+------------+


*Examples:*

.. code:: python

   {
     "host": "pilot1",
     "port": 1883,
     "username": "jared",
     "password": "dunn",
     "topics": [
       {"name": "vehicles/excavators"},
       {"name": "cats"}
     ]
   }

Output settings (*outputSettings*)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

MQTT Input Settings
===================

+---------+---------------------+------------+
| Name    | Description         | Type       |
+=========+=====================+============+
| host    | MQTT host           | string     |
+---------+---------------------+------------+
| port    | MQTT port           | number     |
+---------+---------------------+------------+
| username| Client credentials  | string     |
|         | (optional)          |            |
+---------+---------------------+------------+
| password| Client credentials  | string     |
|         | (optional)          |            |
+---------+---------------------+------------+
| topics  | MQTT topics to      | array[inp  |
|         | subscribe           | utTopic]   |
|         | (optional)          |            |
+---------+---------------------+------------+


*Examples:*

.. code:: python

   {
     "host": "pilot2",
     "port": 1883,
     "username": "bob",
     "password": "builder",
     "topics": [
       {
         "name": "danger/{output['id']}",
         "publishFlags": [
           "QoSExactlyOnceDelivery",
           "Retain"
         ],
         "publishWhen": "always",
         "publishEmptyOutput": true
       }
     ],
     "format": {
       "recordFormat": "object",
       "showHeader": true,
       "wrapSingleColumn": true
     }
   }

Query (*query*)
~~~~~~~~~~~~~~~

Query Configuration
===================

+--------------+------------------------+----------------------+
| Name         | Description            | Type                 |
+==============+========================+======================+
| name         | Unique query name      | string               |
|              | (required)             |                      |
+--------------+------------------------+----------------------+
| inputSettings| Input settings         | inputSettings        |
|              | (optional)             |                      |
+--------------+------------------------+----------------------+
| outputSet    | Output settings        | outputSettings       |
| tings        | (optional)             |                      |
+--------------+------------------------+----------------------+
| sql          | SQL query              | parametrizedString   |
|              | (required)             |                      |
+--------------+------------------------+----------------------+


.. code:: python

   {
     "name": "dangerous",
     "inputSettings": {
       "host": "pilot1",
       "port": 1883,
       "username": "jared",
       "password": "dunn",
       "topics": [
         {"name": "vehicles/excavators"},
         {"name": "cats"}
       ]
     },
     "outputSettings": {
       "host": "pilot2",
       "port": 1883,
       "username": "bob",
       "password": "builder",
       "topics": [
         {
           "name": "danger/{output['id']}",
           "publishFlags": [
             "QoSExactlyOnceDelivery",
             "Retain"
           ],
           "publishWhen": "always",
           "publishEmptyOutput": true
         }
       ],
      "format": {
        "recordFormat": "object",
        "showHeader": true,
        "wrapSingleColumn": true
      }
     },
     "sql": "select id, x, y from worker_positions where st_distance(st_makepoint(x, y), st_makepoint({input['x']}, {input['y']})) < 50;"
   }

Examples
--------

Creating queries
~~~~~~~~~~~~~~~~

To create a query, use the POST method on the ``v1/queries`` endpoint.
The request’s body is expected to be a complete definition of a query.

.. code:: python

   {
     "name": "dangerous",
     "inputSettings": {
       "host": "pilot1",
       "port": 1883,
       "username": "jared",
       "password": "dunn",
       "topics": [
         {"name": "vehicles/excavators"},
         {"name": "cats"}
       ]
     },
     "outputSettings": {
       "host": "pilot2",
       "port": 1883,
       "username": "bob",
       "password": "builder",
       "topics": [
         {
           "name": "danger/{output['id']}",
           "publishFlags": [
             "QoSExactlyOnceDelivery",
             "Retain"
           ],
           "publishWhen": "always",
           "publishEmptyOutput": true
         }
       ],
      "format": {
        "recordFormat": "object",
        "showHeader": true,
        "wrapSingleColumn": true
      }
     },
     "sql": "select id, x, y from worker_positions where st_distance(st_makepoint(x, y), st_makepoint({input['x']}, {input['y']})) < 50;"
   }

The query’s ``name`` is its unique identifier which will be later
referenced to use the query. The ``inputSettings`` and
``outputSettings`` refer to the MQTT input and output configuration. In
both cases, ``host``, ``port``, ``username``, and ``password`` are used
to connect to brokers. The client subscribes to the list of topic names
provided in the ``topics`` inside the input settings. The ``topics``
from the output settings are slightly different. Their names can be
parametrized (see the dedicated section for more explanation on that
matter), and they represent the topics to which the output messages will
be sent. In this example, the message would be sent to the topic, which
part would be determined after getting some specific field (in this case
– ``id``) from the generated output (from running the SQL query).

::

   "name": "danger/{output['id']}"

The part with ``publishFlags`` refers to the list of MQTT flags set
while sending the message. The next part of the ``outputSettings`` is
``publishWhen``. This option can control when the publish action is
triggered – for instance, only if there are no errors. This modifier is
practical as the output from running without errors can differ from the
output of a failed query. The option ``publishEmptyOutput`` should be
self-explanatory. Then there is ``format`` that controls how the output
is formatted (see the definitions section to see the examples). Finally
– the ``sql`` query. It is a parametrized string where one can use the
received input values. The query will be run against the database
included in the enabler. After creating the query, the response will
confirm the operation returning the created query.

Updating queries
~~~~~~~~~~~~~~~~

The queries can be updated by sending a PUT request (``v1/queries``)
with the body describing the query the same as while creating a new
query.

Deleting queries
~~~~~~~~~~~~~~~~

To delete a query, send a DELETE request to ``v1/queries/{name}``, where
``name`` is the query name.

Triggering queries
~~~~~~~~~~~~~~~~~~

If one provides the input and output MQTT settings, then the queries are
typically triggered by the MQTT events. However, every query can be run
from the HTTP interface by calling its name and passing the input it
expects from the MQTT broker – the request body must be a valid JSON
with the input data. The endpoint format is ``v1/queries/{name}/input``
(POST request). After running the query, the output is sent as the
response.

Endpoints
---------

GET ``/v1/queries``
~~~~~~~~~~~~~~~~~~~

Retrieves all queries.

Parameters: *none*.

Body: *none*.

Returns:

-  On success - status code 200, body:

.. code:: python

   {
     "queries": [
       {...},
       {...}
     ]
   }

-  On failure - status code 500, body:

.. code:: python

   {
     "description": "..."
   }

GET ``/v1/queries/{name}``
~~~~~~~~~~~~~~~~~~~~~~~~~~

Retrieves the query with ``name``.

Parameters:

-  ``name``: query name

Body: *none*.

Returns:

-  On success - status code 200, body:

.. code:: python

   {
     "query": {
       ...
     }
   }

-  If query does not exist - status code 404, body:

.. code:: python

   {
     "description: "..."
   }

-  On failure - status code 500, body:

.. code:: python

   {
     "description": "..."
   }

POST ``/v1/queries``
~~~~~~~~~~~~~~~~~~~~

Creates a query.

Parameters: *none*.

Body:

-  query to be created

Returns:

-  On success - status code 201, body:

.. code:: python

   {
     "info": "...",
     "query": {
       ...
     }
   }

-  On error - status code 400, body:

.. code:: python

   {
     "description: "..."
   }

PUT ``/v1/queries/{name}``
~~~~~~~~~~~~~~~~~~~~~~~~~~

Updates the query with ``name``.

Parameters:

-  ``name``: query name

Body:

-  query to be updated

Returns:

-  On success - status code 200, body:

.. code:: python

   {
     "info": "...",
     "query": {
       ...
     }
   }

-  On error - status code 400, body:

.. code:: python

   {
     "description: "..."
   }

DELETE ``/v1/queries/{name}``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Deletes the query with ``name``.

Parameters:

-  ``name``: query name

Body: *none*.

Returns:

-  On success - status code 200, body:

.. code:: python

   {
     "info": "...",
     "deletedQueriesCount": ...
   }

-  On failure - status code 400, body:

.. code:: python

   {
     "description": "..."
   }

POST ``/v1/queries/{name}/input?topic={topic}``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Runs the query with ``name``. The ``topic`` parameters is optional.
Later, it can be one can refer to it as the input topic. If the input
topic is not specified the default one will be used – “http”.

Parameters:

-  ``name``: query name
-  ``topic``: input topic name (optional)

Body: JSON data to be inserted.

Returns:

-  On success - status code 200, body:

.. code:: python

   {
     "..."
   }

The returned body can be any output specified in the query settings.

-  On failure - status code 500, body:

.. code:: python

   {
     "description": "..."
   }

GET ``/metrics``
~~~~~~~~~~~~~~~~

Returns the metrics of the enabler in the Prometheus format.



User guide parametrization
==========================

Parametrization is a feature that gives access to the incoming data and
the results of running queries. For defining SQL queries, input data is
available. Output MQTT topics have access to input and output data.

Input data
~~~~~~~~~~

-  ``input`` input payload as a parsed JSON
-  ``inputTopic`` MQTT topic on which the data arrived, as string
-  ``strInput`` input payload as string

Output data
~~~~~~~~~~~

-  ``output`` output payload as a parsed JSON
-  ``strOutput`` output payload as string

All expressions must be inside curly braces ``{...}``.

To access JSON data (``input`` or ``output``) use
`JSONPath <https://support.smartbear.com/alertsite/docs/monitors/api/endpoint/jsonpath.html>`__
syntax. - JSON strings will yield SQL string literals. - JSON integers
will yield SQL integer literals. - JSON nulls will yield SQL NULL. -
Unmatched paths will yield SQL NULL.

Matching other types of JSON values will result in an error.

*Example – accessing the input value in PostgreSQL*

``"select {strInput}::json->>2;"``

*Example – JSON Path queries*

``"topic/{output..temperature.max()}"``



Prerequisites
=============

-  `Docker <https://www.docker.com/>`__
-  `Docker Compose <https://docs.docker.com/compose/>`__



Installation
============

Development environment (docker-compose)
----------------------------------------

For development, run the following scripts:

.. code:: bash

   # first terminal

   ./scripts/dev-env.sh

The ``dev-env.sh`` script starts the Postgres database (with a pgAdmin
instance) and the MQTT broker (with a MQTT explorer instance). The
database is accessible at ``localhost:5432``. The pgAdmin instance is
accessible at ``localhost:5433``. The MQTT broker is accessible at
``localhost:1883``. The MQTT explorer instance is accessible at
``localhost:4000``. Additionally, one can run the ``qgis.sh`` script to
start a QGIS instance to visualize the geolocation data.

.. code:: bash

   # second terminal

   ./scripts/dev-app.sh

The ``dev-app.sh`` script starts the application. The application is
accessible at ``localhost:8080``.

Production environment (docker-compose)
---------------------------------------

To simulate the production environment, run the following scripts:

.. code:: bash

   # first terminal

   ./scripts/prod-env.sh

The ``prod-env.sh`` script starts the Postgres database.

.. code:: bash

   # second terminal

   ./scripts/prod-app.sh

The ``prod-app.sh`` script starts the application. The application is
accessible at ``localhost:8080``.

Production environment (helm)
-----------------------------

Use the provided helm charts in the ``helm`` directory.

.. code:: bash

   helm install lp helm



Configuration
=============

Application
-----------

The app can be configured via environment variables. - ``HTTP_PORT``:
port at which the API is accessible, i.e. \ *8080* - ``DB_ADMIN_PORT``:
i.e. \ *5432* - ``DB_ADMIN_NAME``: i.e. \ *postgres* -
``DB_ADMIN_USER``: i.e. \ *postgres* - ``DB_ADMIN_PASSWORD``:
i.e. \ *postgres* - ``DB_QUERIES_SERVER_NAME``: i.e. \ *postgres* -
``DB_QUERIES_PORT``: i.e. \ *5432* - ``DB_QUERIES_NAME``:
i.e. \ *queries* - ``DB_QUERIES_USER``: i.e. \ *queries_user* -
``DB_QUERIES_PASSWORD``: i.e. \ *postgres123* -
``DB_GEOLOCATION_SERVER_NAME``: i.e. \ *postgres* -
``DB_GEOLOCATION_PORT``: i.e. \ *5432* - ``DB_GEOLOCATION_NAME``:
i.e. \ *geolocation* - ``DB_GEOLOCATION_USER``:
i.e. \ *geolocation_user* - ``DB_GEOLOCATION_PASSWORD``:
i.e. \ *postgres123*

Database
--------

The database can be configured via environment variables. -
``POSTGRES_DB``: i.e. \ *postgres* - ``POSTGRES_USER``:
i.e. \ *postgres* - ``POSTGRES_PASSWORD``: i.e. \ *postgres*



Developer guide
===============

Environment
-----------

Refer to the `installation
guide <https://magnetic-fields.ibspan.waw.pl/assist-iot/wp5/location-processing/-/wikis/installation>`__
to setup the environment.

Scripts
-------

The development scripts are located in ``scripts`` directory. -
``check.sh`` runs linter (in check mode) and tests - ``clean.sh`` cleans
docker data - ``fix.sh`` runs linter - ``sql-formatter.sh`` formats sql
files

Dependencies
------------

Refer to the ``build.sbt`` file.

Code style
----------

Configs for ``scalafmt``, ``scalafix``, and ``scalastyle`` can be found
in the ``configs`` directory.



Version control and releases
============================

The latest version is 1.0.0.



License
=======

The Location Processing is licensed under the **Apache License, Version
2.0** (the “License”).

One may obtain a copy of the License at
http://www.apache.org/licenses/LICENSE-2.0



Notice (dependencies)
=====================

The enabler can run as a standalone application.



