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

- **PAP -> Edit and publish policy.**
    
  Policy Administration Point offers a web interface to edit the policy and publish it in XACML format to the location where the PDP will use it.

  -	Present a web interface to build a policy
  -	Transform to XACML and place it in the PDPs repository


- **PIP -> Serve context information.**
  
  Policy Information Point presents a Rest interface to publish context data to be used by the PDP when resolving the decision. It will also offer another interface
  (Rest and web) to add data.

  -	Present an interface to add data to the storage
  -	Serve context information in a Rest interface
  
  
- **PEP -> Validate identity and request validation.**
  
  Policy Enforcement Point is the responsible of requesting a decision to the PDP.

  -	Validate identity against third party IS
  -	Launch request to PDP
  
 
- **PDP -> Make decision and launch related actions.**

  Policy Decision Point is the module responsible of making the actual decision based on the context information compiled and the policy available.

  -	Receive a who / what / where question in a Rest interface for validation
  -	Obtain context information from external sources
  -	Build a request compiling all the available data
  -	Validate against the policy
  -	Return Permit or Deny response
  -	Launch related post decision actions

PIP
  Policy Information Point presents a Rest interface to publish context data to be used by the PDP when resolving the decision. It will also offer another interface (Rest and web) to add data.

*********************
Place in architecture
*********************
.. figure:: ./PlaceInArchitecture_CyberSecurity.png
   :width: 1200
   :alt: "CyberSecurity"

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

+--------+---------------------------------------------------------------------------------------+-----------------------+---------------------+------------------------------------------------------------------------------------------------------------------------------------------------+
| Method |             Endpoint                                                                  | Description           | Payload (if needed) | Response format                                                                                                                                |
+========+=======================================================================================+=======================+=====================+================================================================================================================================================+
|  GET   | /evaluate?resource=<domain>@<sourceOfId>&action=<actionName>&code=<idCode>            | Evaluation request    |                     | { "retcode": "0", "resource":"<domain>@<sourceOfId>", "action": <actionName>", "code": "<idCode>", "response": "Permit","msg": ""}             |
+--------+---------------------------------------------------------------------------------------+-----------------------+---------------------+------------------------------------------------------------------------------------------------------------------------------------------------+
|  GET   | /evaluate?resource=<domain>@<sourceOfId>&action=<actionName>&code=<idCode>@<userRole> | Evaluation request    |                     | { "retcode": "0", "resource":"<domain>@<sourceOfId>", "action": <actionName>", "code": "<idCode>@<userRole>", "response": "Deny","msg": ""}    |
+--------+---------------------------------------------------------------------------------------+-----------------------+---------------------+------------------------------------------------------------------------------------------------------------------------------------------------+

The required parameters are:

-	Resource: resource=domain@sourceOfId
  - domain: Security domain of the policy in Authzserver
  - sourceOfId: Name of the source of identification of the Authzserver user for the code provided.

-	Action: action=actionName
  - actionName: Name of the action, must match in the policy conditions.

-	Identification code: code=idCode@userRole
  - idCode: Identification code registered in Authzserver for the user.
  - userRole (Optional): Role of the user in IDM for the client app.


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

The AuthServer enabler exchanges data with the client application via GET call to the request evaluation endpoint with the required parameters, as it is shown in previous section.
They way this exchange data works is at follows:

1- The app sends a Request to the authserver with all the needed data to evaluate it.
The required parameters are described before, in the User Guide section.

2- If it is needed external data, such as temperature, humidity, distance between two obejtcs,.. this request will be perfomanced by the Authserver to the PiP REST API server previously configured in the policy.

3- Once the Authserver has all the need data evaluates if the user can perform the action and answers with a “Permit” if it can be done or a “Deny” if not.

Example permit response: {"retcode":"0","resource":"domain@sourceOfId","action":"actionName","code":"idCode@admin","response":"Permit","msg":""}

Example deny response: {"retcode":"0","resource":"domain@sourceOfId","action":"actionName","code":"idCode","response":"Deny","msg":""}


***************************
Version control and release
***************************

Version 2.4

- Policy rule condition editor: Added support for the following comparission operators <, <=, >, >=, appart of the ==. Can be used in string, int and double values.

Version 2.3

- Enhances in the rule editor GUI

Version 2.2

- Added UserRole support in evaluation, receiving in code=idCode@userRole parameter of the request

Version 2.1.

- Added support for evaluation logging to Elasticsearch. 
- MQTT and Elasticsearch configuration made via new enviroment variables

Version 2.0.

- GUI Remake with addition of Variable Catalog, for use in PIP configuration and Condition edition. 
- Fixed GUI and code errors in Obligations Execution (fixed https support)
- Simplified User GUI for rule and PIP edition, removing redundant fields.

Version 1.5.

- Fixes and enhancements in policy exporting to federated PDPs.

Version 1.0. First stable version. 

- PIP configuration and variable definition via GUI using XACML syntax.
- MQTT publication of evaluation results
- Obligation execotion in Premit/Deny evaluations
- Federation supported.

***************
License
***************

Authorization server is is propriety of S21Sec.

MySQL is free and open-source software under the terms of the GNU General Public License.

Apache Tomcat is licensed under Apache License Version 2.0.

********************
Notice(dependencies)
********************
Will be determined after the release of the enabler.
