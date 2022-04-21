.. _Long term data storage enabler:

##############################
Long term data storage enabler
##############################

.. contents::
  :local:
  :depth: 1

***************
Introduction
***************
The role of the Long-Term Storage Enabler is to serve as a secure and resilient storage, offering different storage sizes and individual storage space for other enablers (which could request back when they are being initialising in Kubernetes pods). Therefore, it is considered as one of the ASSIST-IoT enablers envisioned to be deployed on the cloud rather than the edge. Next figure depicts the high-level overview of the LTSE components.

.. figure:: ./LTSE_Architecture.png
   :alt: LTSE Architecture

As it can be seen, it will be mainly formed by three components:

- **LTSE Gateway**: The entrance gate to the LTSE, acting as a proxy from ASSIST-IoT enablers and external services, whose data should be collected either at SQL server databases or noSQL cluster nodes. To do so, the LTSE Gateway is based on restAPI request, with append SQL/noSQL endpoints, respectively. Furthermore, the LTSE gateway also guarantees that the data will be kept safe, in face of various kinds of unauthorised access requests, or hardware failures, by only allowing access to the data once the Identity Manager and the Authorisation enablers have confirmed their access rights.

- **LTSE noSQL cluster**: A group of one or more LTSE NoSQL nodes instances that are connected together, and carries out the distribution of tasks, searching and indexing, across all the noSQL nodes. Every NoSQl node in the NoSQL cluster can handle HTTP and transport traffic by default with the external enablers through the LTSE gateway. The transport layer is used exclusively for communication between nodes; the HTTP layer is used by REST clients. The full hierarchy would be therefore, noSQL_Cluster > noSQL_Node > noSQL_Index > noSQL_document. For High Availability (HA), noSQL_document in LTSE_noSQL_Index may be distributed across multiple shards, which in turn are distributed across multiple nodes, if configured.

- **LTSE SQL server**: It manages the SQL databases, formed by different enablers data tables. It performs, hence, backup database actions on behalf of the enablers. The SQL_Server can handle multiple concurrent connections from external enablers via the LTSE Gateway. In general, the full hierarchy is: SQL_Cluster > SQL_Database > SQL_schema > SQL_table > SQL_row. For High Availability, a master database with one or more standby servers can be setup. 

***************
Features
***************
The following image illustrates the different frameworks used for the implementation of the three main LTSE components.

.. figure:: ./LTSE_components.png
   :alt: LTSE components

As it can be see, the main structure is the following:

- SQL server -->  `PostGreSQL 14.2.0 version <https://artifacthub.io/packages/helm/bitnami/postgresql>`__ 

- NoSQL cluster --> `ElasticSearch 7.16.3 <https://artifacthub.io/packages/helm/elastic/elasticsearch>`__ 

- LTSE gateway --> `Custom HTTP web framework (Gin) written in Go <https://github.com/gin-gonic/gin>`__  

*********************
Place in architecture
*********************
The Long Term data Storage enabler is part of the Data Management Plane of ASSIST-IoT. The Data Management plane encompasses any process, in which data is processed to deliver features concerning data interoperability, annotation, security, acquisition, provenance, aggregation, fusion, etc. This enabler serve as a secure and resilient storage of any ASSIST-IoT deployment.

***************
User guide
***************
REST API endpoints
*******************
+---------+------------------------------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+----------------------+------------------+
| Method  | Endpoint                                             | Description                                                                                                                                                                        | Payload (if needed)  | Response format  |
+=========+======================================================+====================================================================================================================================================================================+======================+==================+
| POST    | /sql/databases                                       | Creates a databasename in the ltse sql cluster                                                                                                                                     | databasename         |                  |
+---------+------------------------------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+----------------------+------------------+
| POST    | /sql/databases/:databasename/tables/                 | Creates a tablename in the databasename of ltse sql server                                                                                                                         | tablename            |                  |
+---------+------------------------------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+----------------------+------------------+
| POST    | /sql/databases/:databasename/tables/:tablename/data  | Inserts data into the tablename on the databasename of ltse sql server                                                                                                             | data                 |                  |
+---------+------------------------------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+----------------------+------------------+
| GET     | /sql/databases/:databasename/tables/                 | Obtains all the data contained within the tablename of the databasename of ltse sql server                                                                                         | tablename            |                  |
+---------+------------------------------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+----------------------+------------------+
| PUT     | /nosql/index/                                        | Creates a new index indexname in the ltse nosql cluster. when creating an index, you can specify the settings for the index, mappings for fields in the index, and index aliases   | indexname            |                  |
+---------+------------------------------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+----------------------+------------------+
| GET     | /nosql/index/                                        | Returns information about indexname index from the ltse nosql cluster                                                                                                              | indexname            |                  |
+---------+------------------------------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+----------------------+------------------+
| PUT     | /nosql/index/<indexname>/document/                   | Adds a json document to the specified <indexname > index of the ltse nosql cluster and makes it searchable with an <_id>                                                           | _id                  |                  |
+---------+------------------------------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+----------------------+------------------+
| GET     | /nosql/index/<indexname>/_doc/                       | Retrieves the specified json document <_id> from the indexname of the ltse nosql cluster.                                                                                          | _id                  |                  |
+---------+------------------------------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+----------------------+------------------+

***************
Prerequisites
***************
- Kubernetes 1.19+
- Helm 3.2.0+
- PV provisioner support in the underlying infrastructure

***************
Installation
***************

Installing the chart
*******************
The enabler is provided as a Helm chart. To install the chart with the release name ``my-ltse``:

``helm install my-ltse ltse``

The command deploys PostgreSQL on the Kubernetes cluster in the default configuration. The Parameters section lists the parameters that can be configured during installation.

    **Tip**: List all releases using ``helm list``

Uninstalling the Chart
*******************
To uninstall/delete the ``my-ltse`` deployment:

``helm delete my-ltse``

The command removes all the Kubernetes components but PVC's associated with the chart and deletes the release.

To delete the PVC's associated with ``my-ltse``:

``kubectl delete pvc -l release=my-ltse``

    **Note**: Deleting the PVC's will delete postgresql data as well. Please be cautious before doing it.

*********************
Configuration options
*********************
TBD

***************
Developer guide
***************
TBD

***************************
Version control and release
***************************
- Version 1.0. - Currently LTSE does not communicate with Cybersecurity enablers. In addition, API is only able to create DBs and tables, but the rest of API functionalities are still not supported

- Improvements and new functionalities will be added in future versions.

***************
License
***************
TBD

********************
Notice(dependencies)
********************
TBD
