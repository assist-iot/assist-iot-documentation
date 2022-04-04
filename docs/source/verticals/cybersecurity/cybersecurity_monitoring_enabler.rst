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

- Security Analytics
- Intrusion Detection.
- Log Data Analysis.
- File Integrity Monitoring.
- Vulnerability Detection.
- Configuration Assessment.
- Insident Response.
- Regulatory Compliance.
- Cloud Security Monitoring.
- Containers Security.

*********************
Place in architecture
*********************


*Security Analytics*

  Is used to collect, aggregate, index and analyze security data, helping organizations detect intrusions, threats and behavioral anomalies.
  As cyber threats are becoming more sophisticated, real-time monitoring and security analysis are needed for fast threat detection and remediation.The server
  component provides the security intelligence and performs data analysis.


*Intrusion Detection*

  Agents scan the monitored systems looking for malware, rootkits and suspicious anomalies. They can detect hidden files, cloaked processes or unregistered
  network listeners, as well as inconsistencies in system call responses.
  In addition to agent capabilities, the server component uses a signature-based approach to intrusion detection, using its regular expression engine to analyze
  collected log data and look for indicators of compromise.


*Log Data Analysis*

  Agents read operating system and application logs, and securely forward them to a central manager for rule-based analysis and storage.
  The rules help the user to notice application or system errors, misconfigurations, attempted and/or successful malicious activities, policy violations, and other
  security and operational issues.


*File Integrity Monitoring*

  It monitors the file system, identifying changes in content, permissions, ownership and attributes of files that need attention. It also natively identifies users
  and applications used to create or modify files.
  File integrity monitoring capabilities can be used in combination with threat intelligence to identify threats or compromised hosts. In addition, several regulatory
  compliance standards, such as PCI DSS, require it.


*Vulnerability Detection*

  Agents pull software inventory data and send this information to the server, where it is correlated with continuously updated CVE (Common Vulnerabilities and
  Exposure) databases, in order to identify well-known vulnerable software.
  Automated vulnerability assessment helps the user to identify the weak spots of their critical assets and take action before being exploited by attackers.


*Configuration Assessment*
  
  Monitoring system and application configuration settings to ensure they are compliant with your security policies, standards and/or hardening guides. Agents
  perform periodic scans to detect applications that are known to be vulnerable, unpatched, or insecurely configured.
  Additionally, configuration checks can be customized, tailoring them to properly align with your organization. Alerts include recommendations for better
  configuration, references and mapping with regulatory compliance.


*Insident Response*

  Provides an active responses to perform various countermeasures to address active threats, such as blocking access to a system from the threat
  source when certain criteria are met.
  In addition, can be used to remotely run commands or system queries, identifying indicators of compromise (IOCs) and helping perform other live forensics or
  incident response tasks.


*Regulatory Compliance*

  The necessary security controls to become compliant with industry standards and regulations. These features, combined with its scalability and
  multi-platform support help organizations meet technical compliance requirements.
  Provides reports and dashboards that can help with this and other regulations such as GDPR, NIST 800-53, GPG13, TSC SOC2, and HIPAA.


*Cloud Security Monitoring*

  Helps monitor cloud infrastructure at an API level, using integration modules that are able to pull security data from well known cloud providers like Amazon
  AWS, Azure, or Google Cloud. In addition, provides rules to assess the configuration of your cloud environment, easily spotting weaknesses.
  Furthermore, light-weight and multi-platform agents are commonly used to monitor cloud environments at the instance level.


*Containers Security*

  Security visibility into hosts and Docker containers, monitoring their behavior and detecting threats, vulnerabilities, and anomalies. The agent
  has native integration with the Docker engine that allows users to monitor images, volumes, network configurations, and running containers.
  Continuously collects and analyzes detailed runtime information. For example, alerting for containers running in privileged mode, vulnerable applications, a
  shell running in a container, changes to persistent volumes or images, and other possible threats.


***************
User guide
***************

Manager server offers a Rest interface for agent communication. The url should include the resource, action and requester id. The response will include the decision to be implemented in the enforcer (Permit or Deny).

+--------+------------------------------------------------------------------+-----------------------+---------------------+----------------------------------------------------------------------------------------------------------------------+
| Method |             Endpoint                                             | Description           | Payload (if needed) | Response format                                                                                                      |
+========+==================================================================+=======================+=====================+======================================================================================================================+
|  GET   | /evaluate?resource=<domain>@<resource>&action=<action>&code=<id> | Evaluation request    |                     | { "retcode": "0", "resource":"<domain>@<res>", "action": <action>", "code": "<id>", "response": "Permit","msg": ""}  |
+--------+------------------------------------------------------------------+-----------------------+---------------------+----------------------------------------------------------------------------------------------------------------------+


***************
Prerequisites
***************

There is a recomended hardware requeriments as follows:

- 2Cpu
- 16Gb Ram
- 1TB Storage

The enabler is build to run in a K8S environment and the creation is prepared to be autonomous in such a working system.

The service consumer will be required to communicate with the server using the described Rest API interface, and also all the communications between enablers will be provided by K8S API.

***************
Installation
***************

Enabler is provided as a Helm chart. Refer to specific deployment instructions.

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

Version 0.1. Under development.

***************
License
***************

*The entire configuration, communication, preparation and start-up system owned by S21Sec.*

- Wazuh Copyright (C) 2015-2022 Wazuh Inc. (License GPLv2).

-	The Hive 4.1.0-1 (latest) Open Source and free software released under the AGPL (Affero General Public License).

-	Cassandra 3.11 is licensed under Apache License Version 2.0.

-	Cortex 3.1.0-1 (latest) Open Source and free software released under the AGPL (Affero General Public License).

-	Elasticsearch 7.11.1 

-	Kibana 7.11.1

-	MISP 2.4.134 (core-latest)

-	Mysql 8.0.22 (latest)

-	Redis 6.0.9 (latest)

-	Shuffle 0.8.64

-	Shuffle-Backend 0.8.64

-	Shuffle-Database

-	Shuffle-Orborus 0.8.63


********************
Notice(dependencies)
********************

TBD
