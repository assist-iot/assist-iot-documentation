.. _Data integrity verification enabler:

###################################
Data integrity verification enabler
###################################

.. contents::
  :local:
  :depth: 1

***************
Introduction
***************
This is an enabler responsible for providing DLT-based data integrity verification mechanisms that allow data consumers to verify the integrity of any data at question.

***************
Features
***************
Network peers host smart con-tract (chaincode) which includes the data integrity business logic. It stores hashed data in a data structure and it compares it with the hashed data of the queries made by clients in order to verify their integrity.
 
*********************
Place in architecture
*********************
The Integrity Verification enabler is part of the vertical plane DLT enablers.

***************
User guide
***************
The user guide will be determined after the release of the enabler.

***************
Prerequisites
***************
Hyperledger Fabric 2.2, Hyperledger Fabric CA 1.4

***************
Installation
***************
The installation procedure is under development.

*********************
Configuration options
*********************
The enabler is prepared to run in a K8S environment. The creation is prepared to be autonomous in such a working environment.
The service consumer will be required to communicate with the server using the described Rest interface.

***************
Developer guide
***************
The Integrity Verification enabler is build using  Hyperledger Fabric Framework. Smart contracts are written in Go.

***************************
Version control and release
***************************
Gitlab will be used as a version control and release tool.

***************
License
***************
Will be determined after the release of the enabler.

********************
Notice(dependencies)
********************
Dependency list and licensing information will be provided
