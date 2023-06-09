.. _Composite services manager:

###########################
Composite services manager
###########################

.. contents::
  :local:
  :depth: 1

***************
Introduction
***************
Integrated in the tactile dashboard, this enabler presents a graphical environment where ASSIST-IoT administrators can connect previously deployed enablers
to compose a composite service (i.e., a workflow or a pipeline). Having information about the physical topology and available K8s nodes/clusters, 
it allows the user to decide whether to select the proper node or cluster for deploying an enabler, or let the system decide based on pre-defined architectural rules.

***************
Features
***************
Users can define flows among ASSIST-IoT enablers (previously defined as nodes) to move data among them, facilitating the translation between different communication protocols. 
For instance, published messages on an MQTT topic of the EDBE are needed to be stored in the LTSE, or some data available through an HTTP REST API needs to be published
in an MQTT topic to be available for the subscribers.

List of available nodes:

- EDBE
- LTSE
- HTTP ENDPOINT
- MQTT-HTTP
- HTTP-MQTT

List of available translation agents:

- MQTT-HTTP
- HTTP-MQTT

*********************
Place in architecture
*********************
The Composite services manager is part of the vertical plane manageability enablers. Moreover, the frontend component of this enabler will be part of the Tactile dashboard enabler.

.. figure:: ./composite-service-manager-architecture.png
  :alt: Composite services manager architecture
  :align: center


***************
User guide
***************

REST API endpoints
*******************
This enabler will be included in the Tactile Dashboard of the project, so a logged user with the right permissions will be able to access to it by clicking its menu entry.

+--------+-----------------------------+--------------------------------------------------+---------------------+-----------------+
| Method | Endpoint                    | Description                                      | Payload (if needed) | Response format |
+========+=============================+==================================================+=====================+=================+
| GET    | /composite-services-manager | Composite services manager view of the dashboard |                     | Web page        |
+--------+-----------------------------+--------------------------------------------------+---------------------+-----------------+

Endpoints of the Backend component:

+--------+----------------------+-----------------------------------------------+-------------------------------+-----------------------------------------------+
| Method | Endpoint             | Description                                   | Payload (if needed)           | Response format                               |
+========+======================+===============================================+===============================+===============================================+
| GET    | /version             | Get the enabler version                       |                               | { "version": String }                         |
+--------+----------------------+-----------------------------------------------+-------------------------------+-----------------------------------------------+
| GET    | /health              | Get the enabler's health status               |                               |                                               |
+--------+----------------------+-----------------------------------------------+-------------------------------+-----------------------------------------------+
| GET    | /metrics             | Obtain some enabler metrics                   |                               | { "flows": Number, "deployedAgents": Number } |
+--------+----------------------+-----------------------------------------------+-------------------------------+-----------------------------------------------+
| GET    | /api-export/open-api | Get the OpenAPI specification in JSON         |                               | OpenAPI specification in JSON                 |
+--------+----------------------+-----------------------------------------------+-------------------------------+-----------------------------------------------+
| POST   | /                    | Update flows as defined in the front endpoint | Node-RED flows format in JSON | { "message": String }                         |
+--------+----------------------+-----------------------------------------------+-------------------------------+-----------------------------------------------+

Frontend dashboard
*******************
.. figure:: ./composite-service-manager-dashboard.png
  :alt: Composite services manager dashboard
  :align: center


Create a flow
****************
1. Drag a node of an enabler from the ASSIST-IoT group from the left side menu and drop it onto the dashboard.
2. Double-click on the enabler node to configure it and save the configuration.

.. figure:: ./composite-service-manager-edit-node.png
  :alt: Composite services manager: edit node
  :align: center

3. Drag an agent node, drop it on the dashboard and connect the two nodes by clicking on the edge of the node.
4. Double-click on the agent node to configure it and save the configuration.
5. Drag a node of another enabler, drop it on the dashboard and connect it to the agent by clicking on the node border.
6. Double-click on the enabler node to configure it and save the configuration.
7. Click on the *Deploy* button at the top right of the dashboard.
8. A JSON with the response of the Backend API will be displayed in the *Debug* section.
9. The Smart Orchestrator will deploy the configured agents in the flows in the corresponding K8s cluster.


Example of working flows:

.. figure:: ./composite-service-manager-example-flows.png
  :alt: Composite services manager: example flows
  :align: center


Delete a flow
****************
1. Select and delete the flows from the dashboard.
2. Click on the *Deploy* button at the top right of the dashboard.
3. A JSON with the response of the Backend API will be displayed in the *Debug* section.
4. The Smart Orchestrator will deploy the configured agents in the flows in the corresponding K8s cluster.


.. note:: 
  It's better to click on the *Deploy* button after the creation and deletion of all the flows.


***************
Prerequisites
***************
The Smart Orchestrator and the LTSE must be previously installed.

.. warning::
  This enabler has some prerequisites regarding the Smart Orchestrator:
  - At least the *cloud* K8s cluster must be registered
  - The ASSIST-IoT enabler's Helm chart public repository must be resgistered

***************
Installation
***************
The enabler can be installed using its Helm chart, but in future releases it will be installed along with the Smart Orchestrator in the latter's installation script.

1. Add the Helm chart repository:

   ``helm repo add assist-public-repo https://gitlab.assist-iot.eu/api/v4/projects/85/packages/helm/stable``

2. Install the last version of the enabler:

   ``helm install assist-public-repo/composite-services``

*********************
Configuration options
*********************
The backend of the enabler can be configured using the following environment variables in the Helm chart:

- **smartOrchestratorUrl**: complete URL of the Smart Orchestrator.
- **validNodes**: list of valid nodes (Node-RED nodes) to be used to define the flows in the frontend dashboard.
- **helmChartRepository**: name of the Helm chart repository which contains the charts of the agents.
- **ltseUrl**: complete URL of the LTSE API.
- **ltseIndex**: name of the Elasticsearch index to store the defined flows.

***************
Developer guide
***************
The intention of this enabler is to be open to the development of `new Node-RED nodes <https://nodered.org/docs/creating-nodes/>`_ and translation agents. Please, use the developed `nodes <https://gitlab.assist-iot.eu/wp5/t55/composite-services/-/tree/master/node-red>`_ 
and `agents <https://gitlab.assist-iot.eu/wp5/t55/composite-services/-/tree/master/agents>`_  as a reference.

***************************
Version control and release
***************************
Version 1.0.0 fully functional, but it is open to the addition of more agents, nodes and features. Furthermore, it is aligned with the version 3.0.0 of the Smart Orchestrator enabler.

***************
License
***************
Apache 2.0.

*********************
Notice (dependencies)
*********************
This enabler depends on the Smart Orchestrator enabler and the Long Term data Storage Enabler (LTSE). Furthermore, is part of the Tactile dashboard enabler as an iframe.

Furthermore, this enabler uses Node-RED for its frontend component, which is also under an Apache 2.0 license.