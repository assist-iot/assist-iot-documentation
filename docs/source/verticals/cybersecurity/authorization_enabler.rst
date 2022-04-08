.. _Authorization_enabler:

#####################
Authorization_enabler
#####################

.. contents::
  :local:
  :depth: 1

***************
Introduction
***************

Authorization server offers a decision-making service based on XACML policies. It has different modules that interact and can be deployed independently such as, PEP (Policy Decision Point), PAP (Policy Administration Point), PIP (Policy Information Point) and PDP (Policy Decision Point). Server will present a Rest interface and will respond to an external authorization request. The decision may be accompanied by a set of action to be launched, in the form of external requests.

***************
Features
***************

- PAP. Edit and publish policy
- PIP. Serve context information
- PEP. Validate identity and request validation
- PDP. Make decision and launch related actions

*********************
Place in architecture
*********************

PEP
  Policy Enforcement Point is the responsible of requesting a decision to the PDP.

-	Validate identity against third party IS
-	Launch request to PDP

PAP
  Policy Administration Point offers a web interface to edit the policy and publish it in XACML format to the location where the PDP will use it.

-	Present a web interface to build a policy
-	Transform to XACML and place it in the PDPs repository

PIP
  Policy Information Point presents a Rest interface to publish context data to be used by the PDP when resolving the decision. It will also offer another interface (Rest and web) to add data.

-	Present an interface to add data to the storage
-	Serve context information in a Rest interface

PDP
  Policy Decision Point is the module responsible of making the actual decision based on the context information compiled and the policy available.

-	Receive a who / what / where question in a Rest interface for validation
-	Obtain context information from external sources
-	Build a request compiling all the available data
-	Validate against the policy
-	Return Permit or Deny response
-	Launch related post decision actions

***************
User guide
***************

Authorization server offers a Rest interface for decision making. The url should include the resource, action and requester id. The response will include the decision to be implemented in the enforcer (Permit or Deny).

+--------+------------------------------------------------------------------+-----------------------+---------------------+----------------------------------------------------------------------------------------------------------------------+
| Method |             Endpoint                                             | Description           | Payload (if needed) | Response format                                                                                                      |
+========+==================================================================+=======================+=====================+======================================================================================================================+
|  GET   | /evaluate?resource=<domain>@<resource>&action=<action>&code=<id> | Evaluation request    |                     | { "retcode": "0", "resource":"<domain>@<res>", "action": <action>", "code": "<id>", "response": "Permit","msg": ""}  |
+--------+------------------------------------------------------------------+-----------------------+---------------------+----------------------------------------------------------------------------------------------------------------------+

The policy that provides this decision can be configured in the graphic UI provided by de server.

***************
Prerequisites
***************

The enabler is prepared to run in a K8S environment. The creation is prepared to be autonomous in such a working environment.

The service consumer will be required to communicate with the server using the described Rest interface.

***************
Installation
***************

Enabler is provided as a Helm chart. Refer to specific deployment instructions.

*********************
Configuration options
*********************

The Authorization server options for the rest API to connect are available in the **lib\config.py** file.

::

    remote_address: str = "auth_server"
    remote_port: str = "9000"
    remote_username: str = "admin"
    remote_password: str = "xxxx"

***************
Developer guide
***************

Not applicable.

***************************
Version control and release
***************************

Version 0.1. Under development.

***************
License
***************

Authorization server is is propriety of S21Sec.

MySQL is free and open-source software under the terms of the GNU General Public License.

Apache Tomcat is licensed under Apache License Version 2.0.

********************
Notice(dependencies)
********************

Not applicable.
