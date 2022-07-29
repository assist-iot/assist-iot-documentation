.. _Management of services and enablers' workflow:

#############################################
Management of services and enablers' workflow
#############################################

.. contents::
  :local:
  :depth: 1

***************
Introduction
***************
Integrated in the tactile dashboard, this enabler will present a graphical environment where ASSIST-IoT administrators can instantiate the enablers required to work, and also to connect them to compose a composite service (i.e., a workflow). Having information about the physical topology and available k8s nodes/clusters, it will allow the user to decide whether to select the proper node or cluster for deploying an enabler, or let the system decide based on pre-defined architectural rules.

***************
Features
***************
The component is in an early development stage, as it greatly depends on its interaction with other enablers (and hence, need to have their APIs and environment variables in place). 
At the moment, it is not possible to describe concise features, therefore for the sake of avoiding adding content that might be likely modified, features are not indicated yet.

*********************
Place in architecture
*********************
The Management of services and enablers' workflow enabler is part of the vertical plane manageability enablers. Moreover, this enabler is a user interface that is part of the Tactile dashboard enabler.

.. figure:: ./dashboard-manageability-architecture.png
  :alt: Dashboard architecture
  :align: center

***************
User guide
***************
This enabler will be included in the Tactile Dashboard of the project, so a logged user with the right permissions can access to it by clicking its menu entry.

+--------+-----------+-------------------------------------------------------+---------------------+-----------------+
| Method | Endpoint  | Description                                           | Payload (if needed) | Response format |
+========+===========+=======================================================+=====================+=================+
| GET    | /workflow | Services and enablers' workflow view of the dashboard |                     | Web page        |
+--------+-----------+-------------------------------------------------------+---------------------+-----------------+

***************
Prerequisites
***************
The Smart Orchestrator must be previously installed.

***************
Installation
***************
This enabler will be part of the Tactile dashboard enabler, so see the installation section of the Tactile dashboard enabler entry.

*********************
Configuration options
*********************
Not applicable.

***************
Developer guide
***************
Not Applicable.

***************************
Version control and release
***************************
Not Applicable. Any version has been released yet, the enabler is in an early development stage.

***************
License
***************
Not Applicable. Any code or binary has been released yet.

********************
Notice(dependencies)
********************
This enabler will depend on the Smart Orchestrator enabler and will be part of the Tactile dashboard enabler.