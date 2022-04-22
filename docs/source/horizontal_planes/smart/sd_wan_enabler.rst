.. _SD-WAN enabler:

##############
SD-WAN enabler
##############

.. contents::
  :local:
  :depth: 1

***************
Introduction
***************
The objective of this enabler is to provide access between nodes from different 
sites based on SD-WAN technology. It will work jointly with the WAN acceleration 
enabler to establish scalable, private tunnels within the managed K8s clusters.
 
***************
Features
***************
This enabler will implement mechanisms to connect K8s clusters via private tunnels,
facilitating (i) the deployment and chaining of virtual functions to secure 
connections between them and/or towards the Internet and (ii) the implementation 
of functions to optimise WAN traffic (via WAN Acceleration enabler), enabling
the chaining of (network) functions.

.. note:: 
  This enabler is stil under develoment, being subject to modifications of its scope.

*********************
Place in architecture
*********************
The SD-WAN enabler is located in the Smart Network and Control plane of the ASSIST-IoT 
architecture. In particular, it belongs to the building block related to self-contained networks,
which are the ones used for provisioning private networks over public ones.

.. figure:: ./sdwan_place.PNG 
   :alt: Place of the SD-WAN enabler within the Smart Network and Control Plance architecture
   :align: center
   
   Place of the SD-WAN enabler within the Smart Network and Control Plance architecture


The following diagram aims at describing the global operation of the SD-WAN architecture,
including the SD-WAN enabler and instances of WAN Acceleration enabler (each of them composed by an SD-WAN
custom k8s controller and an SD-WAN CNF).

.. figure:: ./global_sdwan.PNG
   :alt: SD-WAN overall architecture
   :align: center
   
   SD-WAN overall architecture

This overall SD-WAN architecture is guided by the following logic:

1. With the SD-WAN enabler, a user can define overlays, which are abstract groups of K8s clusters whose connections will be managed by the SD-WAN enabler.
2. Through this enabler, the user can define IPSec policies and IP ranges to later on establish tunnels among those clusters, which should have previously deployed an instance of the WAN acceleration enabler.
3. These clusters can act as edges or hubs. Hubs are particular instances of the WAN acceleration enabler that allow chaining network functions that will process the traffic among clusters and before navigating from/towards the Internet.
4. Besides, interacting with the K8s API (not directly with a WAN Acceleration's CNF), a user can define firewall, wan and traffic optimisation policies in the edge clusters.

Particularly, the SD-WAN enabler is composed of four main elements, as one can see in the figure below:

- **SD-WAN Controller**: Component in charge of managing the aspects related to SD-WAN communication, including overlays, IP provisioning, tunnels, hub registration, connection and observation, and cluster addition to be managed by it. Provides a REST API to interact with it.
- **Rsync component**: Service that receives requests from the controller and dispatch K8s resources to the WAN acceleration enablers and K8s resources of the involved clusters to setup the dedicated tunnels. 
- **Database**: Stores key information regarding managed clusters, hubs, overlays, IP ranges, etc.
- **Etcd**: Internal metadata database used to exchange configuration between the controller and rsync component.

.. figure:: ./sdwan_arch.PNG 
   :alt: SD-WAN enabler architecture
   :align: center

   SD-WAN enabler architecture

***************
User guide
***************

REST API endpoints
*******************
The API has not been implemented yet, in the following table are presented the expected endpoints:

+---------------------+---------------------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------+
| Method              | Endpoint                              | Description                                                                                                                                     |
+=====================+=======================================+=================================================================================================================================================+
| GET/POST/PUT/DELETE | /overlays                             | Endpoint in charge of creating, modifying, deleting and getting information regarding a set of edge clusters (and hubs) managed by the enabler. |
+---------------------+---------------------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------+
| GET/POST/PUT/DELETE | /overlays/{id}/proposal               | Endpoint in charge of defining IPSec proposals that can be used for tunnels in an overlay.                                                      |
+---------------------+---------------------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------+
| GET/POST/PUT/DELETE | /overlays/{id}/hubs                   | Define a traffic hub in an overlay. Requires certificate and kubeconfig file to be able to manage it.                                           |
+---------------------+---------------------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------+
| GET/POST/PUT/DELETE | /overlays/{id}/ipranges               | Defines the overlay IP range used for the edge clusters.                                                                                        |
+---------------------+---------------------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------+
| GET/POST/PUT/DELETE | /overlays/{id}/devices                | Define an edge cluster location (with SD-WAN acceleration enabler). Among other input, it required kubeconfig file and certificate information. |
+---------------------+---------------------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------+
| GET/POST/PUT/DELETE | /overlays/{id}/hubs/{id}/devices/{id} | Define a connection between a hub and an edge cluster.                                                                                          |
+---------------------+---------------------------------------+-------------------------------------------------------------------------------------------------------------------------------------------------+

***************
Prerequisites
***************
An analysis of the prerequisites is still under develoment. In this case, the enabler
will require provisioning the *kubeconfig* files of the clusters to manage and 
information about the involved certificates. Additional CNI plugins for K8s such
as Multus might be needed.

***************
Installation
***************
Any Helm chart, dedicated K8s manifests or Docker compose file for deploying the enabler
has been developed yet, as it is still under development.

*********************
Configuration options
*********************
An analysis of the configurations to be modifiable by a user is under assessment.
The exposed port for accessing the API will be one of the available options, as well
as the needed configurations for having execution rights over the involved K8s API endpoints.

***************
Developer guide
***************
Not Applicable.

***************************
Version control and release
***************************
Not Applicable. Any version has been released yet.

***************
License
***************
Not Applicable. Any code or binary has been released yet.

*********************
Notice (dependencies)
*********************
Although it can be deployed standalone, this enabler does not have any sense without
having WAN acceleration enablers deployed in the clusters to manage (as hubs or as edge nodes).
