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
+--------+-----------------+-----------------------------------------------------------------------+---------------------------------------------+-------------------------------------------------------------------------------------------------------------------------------+
| Method | Endpoint        | Description                                                           | Payload (if needed)                         | Response format                                                                                                               |
+========+=================+=======================================================================+=============================================+===============================================================================================================================+
| GET    | /SQL/DATABASES  | Creates a databasename in the LTSE SQL cluster                        | /:databasename                              | WireGuard output command in plain text                                                                                        |
+--------+-----------------+-----------------------------------------------------------------------+---------------------------------------------+-------------------------------------------------------------------------------------------------------------------------------+
| GET    | /info/conf      | Get the configuration file of the WireGuard network interface         |                                             | WireGuard configuration file in plain text                                                                                    |
+--------+-----------------+-----------------------------------------------------------------------+---------------------------------------------+-------------------------------------------------------------------------------------------------------------------------------+
| GET    | /keys           | Obtain the public, private and pre-shared keys to create a new client |                                             | {"public":String, "private":String, "preshared":String}                                                                       |
+--------+-----------------+-----------------------------------------------------------------------+---------------------------------------------+-------------------------------------------------------------------------------------------------------------------------------+
| POST   | /client         | Create a new client                                                   | {"publicKey":String, "presharedKey":String} | {"serverPublicKey":String, "serverIP":String, "serverPort":Integer, "clientIP":String, "allowedIPs":String, "message":String} |
+--------+-----------------+-----------------------------------------------------------------------+---------------------------------------------+-------------------------------------------------------------------------------------------------------------------------------+
| DELETE | /client         | Delete a client                                                       | {"publicKey":String}                        |                                                                                                                               |
+--------+-----------------+-----------------------------------------------------------------------+---------------------------------------------+-------------------------------------------------------------------------------------------------------------------------------+
| PUT    | /client/enable  | Enable a client                                                       | {"publicKey":String}                        |                                                                                                                               |
+--------+-----------------+-----------------------------------------------------------------------+---------------------------------------------+-------------------------------------------------------------------------------------------------------------------------------+
| PUT    | /client/disable | Disable a client                                                      | {"publicKey":String}                        |                                                                                                                               |
+--------+-----------------+-----------------------------------------------------------------------+---------------------------------------------+-------------------------------------------------------------------------------------------------------------------------------+


***************
Prerequisites
***************

***************
Installation
***************
The enabler is provided as a Helm chart.

*********************
Configuration options
*********************

***************
Developer guide
***************

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
