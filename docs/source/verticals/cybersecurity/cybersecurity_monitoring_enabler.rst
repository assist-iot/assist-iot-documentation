.. _Cybersecurity Monitoring enabler:

################################
Cybersecurity Monitoring enabler
################################

.. contents::
  :local:
  :depth: 1

***************
Introduction
***************
Provides security awareness and visibility and infrastructure monitoring. Having raw data as input, the enabler will set a series of processing steps that will enable the discovery of cybersecurity threats, going through a sequence step: (i) collecting, parsing, and normalizing input events, (ii) enriching normalized events, (iii) correlating events for detecting cybersecurity threats.

***************
Features
***************


- **Security Analytics**

    Is used to collect, aggregate, index and analyze security data, helping organizations detect intrusions, threats and behavioral anomalies.
    As cyber threats are becoming more sophisticated, real-time monitoring and security analysis are needed for fast threat detection and remediation.The server
    component provides the security intelligence and performs data analysis.


- **Intrusion Detection**

    Agents scan the monitored systems looking for malware, rootkits and suspicious anomalies. They can detect hidden files, cloaked processes or unregistered
    network listeners, as well as inconsistencies in system call responses.
    In addition to agent capabilities, the server component uses a signature-based approach to intrusion detection, using its regular expression engine to analyze
    collected log data and look for indicators of compromise.


- **Log Data Analysis**

    Agents read operating system and application logs, and securely forward them to a central manager for rule-based analysis and storage.
    The rules help the user to notice application or system errors, misconfigurations, attempted and/or successful malicious activities, policy violations, and other
    security and operational issues.


- **File Integrity Monitoring**

    It monitors the file system, identifying changes in content, permissions, ownership and attributes of files that need attention. It also natively identifies users
    and applications used to create or modify files.
    File integrity monitoring capabilities can be used in combination with threat intelligence to identify threats or compromised hosts. In addition, several regulatory
    compliance standards, such as PCI DSS, require it.


- **Vulnerability Detection**

    Agents pull software inventory data and send this information to the server, where it is correlated with continuously updated CVE (Common Vulnerabilities and
    Exposure) databases, in order to identify well-known vulnerable software.
    Automated vulnerability assessment helps the user to identify the weak spots of their critical assets and take action before being exploited by attackers.


- **Configuration Assessment**
  
    Monitoring system and application configuration settings to ensure they are compliant with your security policies, standards and/or hardening guides. Agents
    perform periodic scans to detect applications that are known to be vulnerable, unpatched, or insecurely configured.
    Additionally, configuration checks can be customized, tailoring them to properly align with your organization. Alerts include recommendations for better
    configuration, references and mapping with regulatory compliance.


- **Insident Response**

    Provides an active responses to perform various countermeasures to address active threats, such as blocking access to a system from the threat
    source when certain criteria are met.
    In addition, can be used to remotely run commands or system queries, identifying indicators of compromise (IOCs) and helping perform other live forensics or
    incident response tasks.


- **Regulatory Compliance**

    The necessary security controls to become compliant with industry standards and regulations. These features, combined with its scalability and
    multi-platform support help organizations meet technical compliance requirements.
    Provides reports and dashboards that can help with this and other regulations such as GDPR, NIST 800-53, GPG13, TSC SOC2, and HIPAA.


- **Cloud Security Monitoring**

    Helps monitor cloud infrastructure at an API level, using integration modules that are able to pull security data from well known cloud providers like Amazon
    AWS, Azure, or Google Cloud. In addition, provides rules to assess the configuration of your cloud environment, easily spotting weaknesses.
    Furthermore, light-weight and multi-platform agents are commonly used to monitor cloud environments at the instance level.


- **Containers Security**

    Security visibility into hosts and Docker containers, monitoring their behavior and detecting threats, vulnerabilities, and anomalies. The agent
    has native integration with the Docker engine that allows users to monitor images, volumes, network configurations, and running containers.
    Continuously collects and analyzes detailed runtime information. For example, alerting for containers running in privileged mode, vulnerable applications, a
    shell running in a container, changes to persistent volumes or images, and other possible threats.


- **Flexible integrations**

    The entire SOAR system is created under different services which connect with API Keys between them and in turn can be consulted using python or bash scripting and very flexible to adapt into different eviroments.
    

- **Process workflows**

    These workflows are made using some of the frameworks, and are designed to help get started with the automation using your own tools.
    Handle email header analysis, search SIEM for alerts on schedule, enrich ticket based on SIEM, ransomware eradication with EDR, malware Eradication from host,
    Block hash in EDR.


- **Incident management**

    The platform based on system that assists and automates incident response services that provide three key major capabilities among others, supporting analyst
    workflows, helping  security analysts collaborate around a security incident, providing alert, case, observable and other techniques used to increase the
    flexibility to the automated security process.


- **Threat intelligence**

    Cortex, with MISP allows security analysts and threat hunters to analyze and enrich observables (IP addresses, hashes, domains, etc) collected with the SIEM. 

*********************
Place in architecture
*********************
.. figure:: ./PlaceInArchitecture_CyberSecurity.png
   :width: 1200
   :alt: "CyberSecurity"


***************
User guide
***************

Cybersecurity monitoring **SIEM** (Security information and event management) server will implement a restful API to manage monitoring server basic configuration and cybersecurity agents connected.

+--------+------------------------------------------------------------------+------------------------------------------------------------------------+
| METHOD |                            ENDPOINT                              |          DESCRIPTION                                                   |
+========+==================================================================+========================================================================+
|  PUT   | {SIEM}/active-response                                           | Run an Active Response command on all agents or a list of them         |
+--------+------------------------------------------------------------------+------------------------------------------------------------------------+
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
|  PUT   | {SIEM}/manager/restart                                           | Restart the manager                                                    |
+--------+------------------------------------------------------------------+------------------------------------------------------------------------+
|  GET   | {SIEM}/manager/stats                                             | Return statistical information for the current or specified date       |
+--------+------------------------------------------------------------------+------------------------------------------------------------------------+
|  PUT   | {SIEM}/manager/configuration                                     | Replace configuration with the data contained in the API request       |
+--------+------------------------------------------------------------------+------------------------------------------------------------------------+
|  GET   | {SIEM}/manager/configuration                                     | Return enabler configuration used                                      |
+--------+------------------------------------------------------------------+------------------------------------------------------------------------+
|  GET   | {SIEM}/manager/info                                              | Basic information such as version, compilation date, installation path |
+--------+------------------------------------------------------------------+------------------------------------------------------------------------+
|  GET   | {SIEM}/manager/status                                            | Return the status of the monitoring server                             |
+--------+------------------------------------------------------------------+------------------------------------------------------------------------+

Cybersecurity monitoring **SOAR** (Security Orchestration and Automation Response) server will implement a restful API to manage monitoring server
basic configuration and cybersecurity features.
 
+--------+------------------------------------------------------------------+------------------------------------------------------------------------+
| METHOD |                            ENDPOINT                              |          DESCRIPTION                                                   |
+========+==================================================================+========================================================================+
|  POST  | {SOAR}/api/v1/login                                              | Authenticate an user and get session cookie                            |
+--------+------------------------------------------------------------------+------------------------------------------------------------------------+
|  POST  | {SOAR}/api/v1/organisation                                       | Create an organisation                                                 |
+--------+------------------------------------------------------------------+------------------------------------------------------------------------+
|  GET   | {SOAR}/api/v0/profile                                            | List all user profiles                                                 |
+--------+------------------------------------------------------------------+------------------------------------------------------------------------+
|  POST  | {SOAR}/api/v0/profile                                            | Create a new profile                                                   |
+--------+------------------------------------------------------------------+------------------------------------------------------------------------+
|  GET   | {SOAR}/api/v0/profile/{profile}                                  | Get information of the given profile                                   |
+--------+------------------------------------------------------------------+------------------------------------------------------------------------+
| PATCH  | {SOAR}/api/v0/profile/{profile}                                  | Update profile                                                         |
+--------+------------------------------------------------------------------+------------------------------------------------------------------------+
| DELETE | {SOAR}/api/v0/profile/{profile}                                  | Remove the profile                                                     |
+--------+------------------------------------------------------------------+------------------------------------------------------------------------+
|  POST  | {SOAR}/api/v1/user                                               | Create a new user                                                      |
+--------+------------------------------------------------------------------+------------------------------------------------------------------------+
|  GET   | {SOAR}/api/v1/user/current                                       | Show information of the current user                                   |
+--------+------------------------------------------------------------------+------------------------------------------------------------------------+
|  GET   | {SOAR}/api/v1/user/{user}                                        | Show information of the given user                                     |
+--------+------------------------------------------------------------------+------------------------------------------------------------------------+
| PATCH  | {SOAR}/api/v1/user/{user}                                        | Update information of the given user                                   |
+--------+------------------------------------------------------------------+------------------------------------------------------------------------+
| DELETE | {SOAR}/api/v1/user/{user}/force                                  | Remove an user                                                         |
+--------+------------------------------------------------------------------+------------------------------------------------------------------------+
|  POST  | {SOAR}/api/v1/user/{user}/password/set                           | Set the user password                                                  |
+--------+------------------------------------------------------------------+------------------------------------------------------------------------+
|  POST  | {SOAR}/api/v1/user/{user}/password/change                        | Change the user password                                               |
+--------+------------------------------------------------------------------+------------------------------------------------------------------------+
|  GET   | {SOAR}/api/v1/user/{user}/key                                    | Get the user API key                                                   |
+--------+------------------------------------------------------------------+------------------------------------------------------------------------+
| DELETE | {SOAR}/api/v1/user/{user}/key                                    | Remove the user API key                                                |
+--------+------------------------------------------------------------------+------------------------------------------------------------------------+
|  POST  | {SOAR}/api/v1/user/{user}/key/renew                              | Renew the user API key                                                 |
+--------+------------------------------------------------------------------+------------------------------------------------------------------------+


***************
Prerequisites
***************


There is a recomended hardware requeriments for the SIEM:

- 2CPU
- 8Gb RAM
- 1TB SSD

and the recomended hardware requeriments for the SOAR as follows:

- 2CPU
- 16GB RAM
- 1TB SSD


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

The configuration listed is for the SIEM, related to data volumes for the integration to the webhooks and placing the source code or executable.

**Add this to ossec.conf configuration: attached to ossec_etc volume for manage the webhook and integrations**


::

    └── ossec_integrations:
      └── custom-shuffle
      |     - handler for custom-shuffle.py
      └── custom-shuffle.py
      |     - integration code for the automation response with the workflow

    
::

    ossec_etc:
      <integration>
        <name>custom-shuffle</name>
        <hook_url>http://<IP>:<PORT>/<REPLACE FOR THE WEBHOOK URL></hook_url>
        <level>3</level>
        <alert_format>json</alert_format>
      </integration>

::

    Add the cortex API into thehive application.conf
    ├── thehive
    │   └── application.conf
    |       └── cortex → servers → auth → key
                # cortex configuration
                play.modules.enabled += org.thp.thehive.connector.cortex.CortexModule
                cortex {
                  servers = [
                    {
                      name = local
                      url = "http://cortex:9001"
                      auth {
                        type = "bearer"
                        key = "Wfsc+3NVCki5xtuFFlvURDGkod5pPBGL"       # cortex API key
                      }
                     }
                  ]
                  refreshDelay = 5 seconds
                  maxRetryOnError = 3
                  statusCheckInterval = 1 minute
                }
    |       └── cortex → servers → auth → key
                # MISP configuration
                play.modules.enabled += org.thp.thehive.connector.misp.MispModule
                misp {
                  interval: 5 min
                  servers: [
                    {
                      name = "MISP THP"            # MISP name
                      url = "https://misp/" # URL or MISP
                      auth {
                        type = key
                        key = "w6RjLh7V9MVWA2yvgeurJWjwEAPkkn8d2L8K1qkW"        # MISP API key
                      }
                      wsConfig { ssl { loose { acceptAnyCertificate: true } } }
                    }
                  ]
                }


***************
Developer guide
***************

The Cybersecurity monitoring enabler only interacts with the cybersecurity monitoring Agent. 

The Cybersecurity monitoring enabler, gets the info from the agent and checks what entries are considered as real attacks and what no. With those that are considered a real attack it can, for example, perform a reaction blocking temporarily the source of the attack.

***************************
Version control and release
***************************

Version 0.1. Under development.

***************
License
***************

*The entire configuration, communication, preparation and start-up system is owned by* **© Copyright - S21Sec, All rights reserved.**

- **Wazuh**  (License under GPLv2).

-	**The Hive**  v-4.1.0-1  (License under GNU AGPLv3).

-	**Cassandra**  v-3.11  (License under Apache Version 2.0).

-	**Cortex**  v-3.1.0-1  (License under GNU AGPLv3).

-	**Elasticsearch**  v-7.11.1  (License under Apache Version 2.0).

-	**Kibana**  v-7.11.1  (License under Elastic Version 2.0).

-	**MISP** v-2.4.134  (License under GNU AGPLv3).

-	**Mysql**  v-8.0.22  (License under GPLv2).

-	**Redis**  v-6.0.9  (Lincense The 3-Clause BSD License).

-	**Shuffle**  v-0.8.64  (License under GNU AGPLv3).

-	**Shuffle-Backend**  v-0.8.64  (License under GNU AGPLv3).

-	**Shuffle-Database**  (License under GNU AGPLv3).

-	**Shuffle-Orborus**  v-0.8.63  (License under GNU AGPLv3).


********************
Notice(dependencies)
********************
Will be determined after the release of the enabler.
