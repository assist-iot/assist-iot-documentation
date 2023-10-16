.. _WAN acceleration enabler:

.. image:: ./images/wan_acceleration_enabler/assist-IoT-logo.png
   :alt: assist-IoT-logo

########################
WAN-Acceleration enabler
########################

.. contents::
  :local:
  :depth: 1

***************
Introduction
***************
The WAN acceleration enabler will incorporate features that will improve the connections among the clusters and/or sites managed by ASSIST-IoT, and towards the Internet. 
It will work jointly with the SD-WAN enabler to establish scalable, private tunnels and introduce optimisation features such as traffic prioritisation.

***************
Features
***************
This enabler will be in charge of implementing features to support multiple WAN links, firewalling, tunnelling setups and traffic control, including traffic  shaping. Depending on its configuration (via the SD-WAN enabler), it can act as:

- An SD-WAN Edge component, present in each K8s cluster, with a dedicated K8s controller and a Containerised Network function (CNF) through which traffic goes through it. The CNF will embed functions to setup aspects such related to IPSec, firewalling, DNS, DHCP and WAN link management, whereas a Custom Definition Resource (CRD) controller contains all the sub-controllers to create, query and configure these features.
- A SD-WAN hub, which will act as a middleware among clusters and/or between them and the Internet, enabling the introduction of additional CNFs related to security, filtering, traffic shaping, etc. Once the basic features are implemented, the incorporation of additional ones (as CNFs) will be evaluated.

*********************
Place in architecture
*********************
The WAN Acceleration enabler is located in the Smart Network and Control plane of the ASSIST-IoT 
architecture. In particular, it belongs to the building block related to VNFs, specifically
(i) for provisioning private networks over public ones, jointly with the SD-WAN enabler, and
(ii) for supporting VNFs chaining (containerised, thus CNFs).

.. figure:: ./images/wan_acceleration_enabler/place-in-architecture.png  
   :alt: Place of the WAN Acceleration enabler within the Smart Network and Control Plance architecture
   :align: center
   
   Place of the WAN Acceleration enabler within the Smart Network and Control Plance architecture

The following diagram aims at describing the global operation of the SD-WAN architecture,
including the SD-WAN enabler and instances of the WAN Acceleration enabler (each of them composed by an SD-WAN
custom k8s controller and an SD-WAN CNF).

.. figure:: ./images/wan_acceleration_enabler/place-in-architecture2.png
   :alt: SD-WAN overall architecture
   :align: center
   
   SD-WAN overall architecture

This overall SD-WAN architecture is guided by the following logic:

1. With the SD-WAN enabler, a user can define overlays, which are abstract groups of K8s clusters whose connections will be managed by the SD-WAN enabler.
2. Through this enabler, the user can define IPSec policies and IP ranges to later on establish tunnels among those clusters, which should have previously deployed an instance of the WAN acceleration enabler.
3. These clusters can act as edges or hubs. Hubs are particular instances of the WAN acceleration enabler that allow chaining network functions that will process the traffic among clusters and before navigating from/towards the Internet.
4. Besides, interacting with the K8s API (not directly with a WAN Acceleration's CNF), a user can define firewall, wan and traffic optimisation policies in the edge clusters.

As aforementioned, the enabler is composed of three main elements, as one can see in the figure below:

- **CRD Controller**: Component that will receive API calls from the K8s API of the cluster to configure the CNF component.
- **SD-WAN CNF**: The CNF will embed functions to setup aspects such related to IPSec, firewalling, DNS, DHCP and WAN link management, exposing an API to be controlled/queried.
- **API**: The API component contains an easy-to-use interface to create, list or delete all configuration related to internal management, such as firewall rules or mwan3 policies. This component interacts directly with the K8S API server rather than with other components.

.. figure:: ./images/wan_acceleration_enabler/wan_acc_arch.png  
   :alt: WAN Acceleration enabler architecture
   :align: center

   WAN Acceleration enabler architecture

***************
User guide
***************

In the following table are presented the endpoint ready to use:

**Firewall**
------------
Define internal firewall configuration. This functionality uses groups to manage general behavior and can define rules, access permissions and source, forward or destination NAT rules.

**Zones**

+------------+-----------------------------------+---------------------------+----------------------------------------------------------------------------+
| **Method** | **Endpoint**                      | **Description**           | **Payload (if need)**                                                      |
+============+===================================+===========================+============================================================================+
| POST       | api/v1/firewall/zones             | Zone Registration         | {"metadata": {"name": "ovn-network"},"spec": {"network": ["ovn-network"]}} |
+------------+-----------------------------------+---------------------------+----------------------------------------------------------------------------+
| GET        | api/v1/firewall/zones             | Get all firewall zones    |                                                                            |
+------------+-----------------------------------+---------------------------+----------------------------------------------------------------------------+
| GET        | api/v1/firewall/zones/{zone-name} | Get firewall zone by name |                                                                            |
+------------+-----------------------------------+---------------------------+----------------------------------------------------------------------------+
| DELETE     | api/v1/firewall/zones/{zone-name} | Delete firewall zone      |                                                                            |
+------------+-----------------------------------+---------------------------+----------------------------------------------------------------------------+

**SNAT**

+------------+-----------------------------------+---------------------------+-----------------------------------------------------------------------+
| **Method** | **Endpoint**                      | **Description**           | **Payload (if need)**                                                 |
+============+===================================+===========================+=======================================================================+
| POST       | api/v1/firewall/snats             | SNAT Registration         | {"metadata": {"name": "firewallsnat"},"spec": {"src": "ovn-network"}} |
+------------+-----------------------------------+---------------------------+-----------------------------------------------------------------------+
| GET        | api/v1/firewall/snats             | Get all firewall snats    |                                                                       |
+------------+-----------------------------------+---------------------------+-----------------------------------------------------------------------+
| GET        | api/v1/firewall/snats/{snat-name} | Get firewall snat by name |                                                                       |
+------------+-----------------------------------+---------------------------+-----------------------------------------------------------------------+
| DELETE     | api/v1/firewall/snats/{snat-name} | Delete firewall snat      |                                                                       |
+------------+-----------------------------------+---------------------------+-----------------------------------------------------------------------+

**DNAT**

+------------+-----------------------------------+---------------------------+--------------------------------------------------------------------+
| **Method** | **Endpoint**                      | **Description**           | **Payload (if need)**                                              |
+============+===================================+===========================+====================================================================+
| POST       | api/v1/firewall/dnats             | DNAT Registration         | {"metadata": {"name": "firewalldnat"},"spec": {"src": "pnetwork"}} |
+------------+-----------------------------------+---------------------------+--------------------------------------------------------------------+
| GET        | api/v1/firewall/dnats             | Get all firewall dnats    |                                                                    |
+------------+-----------------------------------+---------------------------+--------------------------------------------------------------------+
| GET        | api/v1/firewall/dnats/{dnat-name} | Get firewall dnat by name |                                                                    |
+------------+-----------------------------------+---------------------------+--------------------------------------------------------------------+
| DELETE     | api/v1/firewall/dnats/{dnat-name} | Delete firewall dnat      |                                                                    |
+------------+-----------------------------------+---------------------------+--------------------------------------------------------------------+

**Forwarding**

+------------+-----------------------------------------------+---------------------------------+-----------------------------------------------------------------------------+
| **Method** | **Endpoint**                                  | **Description**                 | **Payload (if need)**                                                       |
+============+===============================================+=================================+=============================================================================+
| POST       | api/v1/firewall/forwardings                   | Forwarding Registration         | {"metadata": {"name": "firewallforwarding"},"spec": {"src": "ovn-network"}} |
+------------+-----------------------------------------------+---------------------------------+-----------------------------------------------------------------------------+
| GET        | api/v1/firewall/forwardings                   | Get all firewall forwardings    |                                                                             |
+------------+-----------------------------------------------+---------------------------------+-----------------------------------------------------------------------------+
| GET        | api/v1/firewall/forwardings/{forwarding-name} | Get firewall forwarding by name |                                                                             |
+------------+-----------------------------------------------+---------------------------------+-----------------------------------------------------------------------------+
| DELETE     | api/v1/firewall/forwardings/{forwarding-name} | Delete firewall forwarding      |                                                                             |
+------------+-----------------------------------------------+---------------------------------+-----------------------------------------------------------------------------+

**Rules**

+------------+------------------------------------+----------------------------+-----------------------------------------------------------------------+
| **Method** | **Endpoint**                       | **Description**            | **Payload (if need)**                                                 |
+============+====================================+============================+=======================================================================+
| POST       | api/v1/firewall/rules              | Firewall Rule Registration | {"metadata": {"name": "firewallrule"},"spec": {"src": "ovn-network"}} |
+------------+------------------------------------+----------------------------+-----------------------------------------------------------------------+
| GET        | api/v1/firewall/rules              | Get all firewall rules     |                                                                       |
+------------+------------------------------------+----------------------------+-----------------------------------------------------------------------+
| GET        | api/v1/firewall/rules/{rule-name}  | Get firewall rule by name  |                                                                       |
+------------+------------------------------------+----------------------------+-----------------------------------------------------------------------+
| DELETE     | api/v1/firewall/ruless/{rule-name} | Delete firewall rule       |                                                                       |
+------------+------------------------------------+----------------------------+-----------------------------------------------------------------------+

**MWAN3**
------------
Define internal mwan3 configuration. Define policies and rules to manage balancing and failover for each edge cluster.

**Policies**

+------------+-------------------------------------+---------------------------+-----------------------------------------------------------+
| **Method** | **Endpoint**                        | **Description**           | **Payload (if need)**                                     |
+============+=====================================+===========================+===========================================================+
| POST       | api/v1/mwan3/policies               | MWAN3 Policy Registration | {"metadata": {"name": "mwan3policy"},"spec": {"members"}} |
+------------+-------------------------------------+---------------------------+-----------------------------------------------------------+
| GET        | api/v1/mwan3/policies               | Get all mwan3 policies    |                                                           |
+------------+-------------------------------------+---------------------------+-----------------------------------------------------------+
| GET        | api/v1/mwan3/policies/{policy-name} | Get mwan3 policy by name  |                                                           |
+------------+-------------------------------------+---------------------------+-----------------------------------------------------------+
| DELETE     | api/v1/mwan3/policies/{policy-name} | Delete firewall policy    |                                                           |
+------------+-------------------------------------+---------------------------+-----------------------------------------------------------+

**Rules**

+--------------+----------------------------------+---------------------------+------------------------------------------------------------+
| ### Rules    |                                  |                           |                                                            |
+==============+==================================+===========================+============================================================+
| **Method**   | **Endpoint**                     | **Description**           | **Payload (if need)**                                      |
+--------------+----------------------------------+---------------------------+------------------------------------------------------------+
| ------------ | -------------------------------- | ------------------------- | ---------------------------------------------------------- |
+--------------+----------------------------------+---------------------------+------------------------------------------------------------+
| POST         | api/v1/mwan3/rules               | MWAN3 Rule Registration   | {"metadata": {"name": "mwan3rule"},"spec": {"family"}}     |
+--------------+----------------------------------+---------------------------+------------------------------------------------------------+
| GET          | api/v1/mwan3/rules               | Get all mwan3 rules       |                                                            |
+--------------+----------------------------------+---------------------------+------------------------------------------------------------+
| GET          | api/v1/mwan3/rules/{rule-name}   | Get mwan3 rule by name    |                                                            |
+--------------+----------------------------------+---------------------------+------------------------------------------------------------+
| DELETE       | api/v1/mwan3/rules/{rule-name}   | Delete firewall rule      |                                                            |
+--------------+----------------------------------+---------------------------+------------------------------------------------------------+


***************
Prerequisites
***************
In this case, the enabler required some CNI plugins for K8s:

* Calico.
* Multus daemonset.
* OVN daemonset.
* OVN networks.
* Cert manager to manage connection between networks.

In addition, the enabler will require provisioning the *kubeconfig* files of the clusters to manage and  information about the involved certificates.

***************
Installation
***************
Prerrequisites are available to install in shell bash script named "kubernetes.sh". Rest of installation are done implemented by k8s manifests. In future releases, the installation will be by helm charts.

Steps of installation are avaible in gitlab repository.

*********************
Configuration options
*********************
An analysis of the configurations to be modifiable by a user is under assessment.
The exposed port for accessing the API will be one of the available options.

***************
Developer guide
***************
Will be determined after the release of the enabler.

***************************
Version control and release
***************************
Version 1.0. First release.

***************
License
***************
Copyright 2023 Raúl Reinosa Simón (Universitat Politècnica de València)

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License.
You may obtain a copy of the License at 

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

*********************
Notice (dependencies)
*********************
This enabler can work in an standalone fashion to offer network-related features
related mostly to firewalling. It will be fully functional if it works jointly with
a SD-WAN enabler, enabling the setup of secured tunnels between clusters.
