.. _Cybersecurity Monitoring agent enabler:

######################################
Cybersecurity Monitoring agent enabler
######################################

.. contents::
  :local:
  :depth: 1

***************
Introduction
***************
Perform functions of an endpoint detection and response system, monitoring and collecting activity from end points that could indicate a threat. Security agent runs at a host-level, combining anomaly and signature-based technologies to detect intrusions or software misuse.

***************
Features
***************


All agent modules have different purposes and settings. Here is a brief description of what they do:


- **Log collector:**

    This agent component can read flat log files and Windows events, collecting operating system and application log messages. It does support XPath filters for
    Windows events and recognizes multi-line formats (e.g. Linux Audit logs). It can also enrich JSON events with additional metadata.


- **Command execution:**

    Agents can run authorized commands periodically, collecting their output and reporting it back to the Wazuh server for further analysis. This module can be used to
    meet different purposes (e.g. monitoring hard disk space left, getting a list of last logged in users, etc.).


- **File integrity monitoring (FIM):**


    This module monitors the file system, reporting when files are created, deleted, or modified. It keeps track of file attributes, permissions, ownership, and
    content. When an event occurs, it captures who, what, and when details in real time. Additionally, this module builds and maintains a database with the state of
    the monitored files, allowing queries to be run remotely.


- **Security configuration assessment (SCA):**


    This component provides continuous configuration assessment, utilizing out-of-the-box checks based on the Center of Internet Security (CIS) benchmarks. Users can
    also create their own SCA checks to monitor and enforce their security policies.


- **System inventory:**

    This agent module periodically runs scans, collecting inventory data such as operating system version, network interfaces, running processes, installed
    applications, and a list of open ports. Scan results are stored into local SQLite databases that can be queried remotely.


- **Malware detection:**

    Using a non-signature based approach, this component is capable of detecting anomalies and possible presence of rootkits. Monitoring system calls, it looks for
    hidden processes, hidden files, and hidden ports.


- **Active response:**

    This module runs automatic actions when threats are detected. Among other things, it can block a network connection, stop a running process, or delete a malicious
    file. Custom responses can also be created by users when necessary (e.g. run a binary in a sandbox, capture a network connection traffic, scan a file with an
    antivirus, etc.).


- **Containers security monitoring:**

    This agent module is integrated with the Docker Engine API in order to monitor changes in a containerized environment. For example, it detects changes to container
    images, network configuration, or data volumes. Besides, it alerts on containers running in privileged mode and on users executing commands in a running container.


- **Cloud security monitoring:**


    This component monitors cloud providers such as Amazon AWS, Microsoft Azure, or Google GCP. It natively communicates with their APIs. It is capable of detecting
    changes to the cloud infrastructure (e.g. a new user is created, a security group is modified, a cloud instance is stopped, etc.), and collecting cloud services
    log data (e.g. AWS Cloudtrail, AWS Macie, AWS GuardDuty, Azure Active Directory, etc.)




*********************
Place in architecture
*********************

.. figure:: ./PlaceInArchitecture_CyberSecurity.png
   :width: 1200
   :alt: "CyberSecurity"



***************
User guide
***************


+--------+------------------------------------------------------------------+------------------------------------------------------------------------+
| METHOD |                            ENDPOINT                              |          DESCRIPTION                                                   |
+========+==================================================================+========================================================================+
|  PUT   | {SIEM}/agents/restart                                            | Restart all agents or a list of them                                   |
+--------+------------------------------------------------------------------+------------------------------------------------------------------------+
|  PUT   | {SIEM}/agents/{agent_id}/restart                                 | Restart the specified agent                                            |
+--------+------------------------------------------------------------------+------------------------------------------------------------------------+
|        |                                                                  | Add an agent specifying its name, ID and IP. If an agent with          |
|  POST  | {SIEM}/agents/insert                                             | the same ID already exists, replace it using 'force' parameter         |
+--------+------------------------------------------------------------------+------------------------------------------------------------------------+
|  POST  | {SIEM}/agents                                                    | Add a new agent with basic info                                        |
+--------+------------------------------------------------------------------+------------------------------------------------------------------------+
| DELETE | {SIEM}/agents                                                    | Delete all agents or a list of them based on optional criteria         |
+--------+------------------------------------------------------------------+------------------------------------------------------------------------+
|  GET   | {SIEM}/agents                                                    | Obtain a list with information of the available agents                 |
+--------+------------------------------------------------------------------+------------------------------------------------------------------------+


***************
Prerequisites
***************


There is a recomended hardware requeriments for the Agent:

- 1CPU
 
- 35MB RAM

The enabler is build to run in a K8S environment and the creation is prepared to be autonomous in such a working system.

The service consumer will be required to communicate with the server using the described Rest API interface, and also all the communications between enablers will be provided by K8S API.

***************
Installation
***************

Enabler is provided as a Helm chart, including requieremenst and enviroment.
Refer to specific deployment instructions.

*********************
Configuration options
*********************


+------------------------------------------------------------------+------------------------------------------------------------------------+
|                            OPTION                                |          DESCRIPTION                                                   |
+==================================================================+========================================================================+
| WAZUH_MANAGER                                                    | Specifies the manager IP address or hostname. In case you want to      |
|                                                                  | specify multiple managers, you can add them separated by commas.       |
+------------------------------------------------------------------+------------------------------------------------------------------------+
| WAZUH_MANAGER_PORT                                               | Specifies the manager’s connection port.                               |
+------------------------------------------------------------------+------------------------------------------------------------------------+
| WAZUH_PROTOCOL                                                   | Sets the communication protocol between the manager and the agent.     |
|                                                                  | Accepts UDP and TCP. Default is TCP.                                   |
+------------------------------------------------------------------+------------------------------------------------------------------------+
| WAZUH_REGISTRATION_SERVER                                        | Specifies the Wazuh registration server, used for the agent            |
|                                                                  | registration. If empty, the value set in WAZUH_MANAGER will be used.   |
+------------------------------------------------------------------+------------------------------------------------------------------------+
| WAZUH_REGISTRATION_PORT                                          | Specifies the port used by the Wazuh registration server.              |
+------------------------------------------------------------------+------------------------------------------------------------------------+
| WAZUH_REGISTRATION_PASSWORD                                      | Sets the Wazuh registration server. See agent-auth options.            |
+------------------------------------------------------------------+------------------------------------------------------------------------+
| WAZUH_KEEP_ALIVE_INTERVAL                                        | Sets the time between agent checks for manager connection.             |
+------------------------------------------------------------------+------------------------------------------------------------------------+
| WAZUH_TIME_RECONNECT                                             | Sets the time interval for the agent to reconnect with the Wazuh       |
|                                                                  | manager when connectivity is lost.                                     |
+------------------------------------------------------------------+------------------------------------------------------------------------+
| WAZUH_REGISTRATION_CA                                            | Host SSL validation need of Certificate of Authority.                  |
|                                                                  | This option specifies the CA path.                                     |
+------------------------------------------------------------------+------------------------------------------------------------------------+
| WAZUH_REGISTRATION_CERTIFICATE                                   | The SSL agent verification needs a CA signed certificate and the       |
|                                                                  | respective key. This option specifies the certificate path.            |
+------------------------------------------------------------------+------------------------------------------------------------------------+
| WAZUH_REGISTRATION_KEY                                           | Specifies the key path completing the required variables with          |
|                                                                  | WAZUH_REGISTRATION_CERTIFICATE for the SSL agent verification process. |
+------------------------------------------------------------------+------------------------------------------------------------------------+	
| WAZUH_AGENT_NAME                                                 | Designates the agent’s name. By default it will be the computer name.  |
+------------------------------------------------------------------+------------------------------------------------------------------------+
| WAZUH_AGENT_GROUP                                                | Assigns the agent to one or more existing groups (separated by commas).|
+------------------------------------------------------------------+------------------------------------------------------------------------+


***************
Developer guide
***************
Will be determined after the release of the enabler.

***************************
Version control and release
***************************

Version 0.1. Under development.

***************
License
***************

*The entire configuration, communication, preparation and start-up system is owned by* **© Copyright - S21Sec, All rights reserved.**

- **Wazuh**  (License under GPLv2).


********************
Notice(dependencies)
********************
Will be determined after the release of the enabler.
