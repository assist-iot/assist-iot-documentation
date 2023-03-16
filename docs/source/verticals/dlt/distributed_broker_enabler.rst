.. _Distributed broker enabler:

##########################
Distributed broker enabler
##########################

.. contents::
  :local:
  :depth: 1

***************
Introduction
***************
This enabler will provide a mechanism that will facilitate data sharing between different heterogene-ous IoT devices belonging to various edge domains and/or between different enablers of the archi-tecture. In coordination with other enablers that will ensure trust between data sources (i.e. Identity and Authorisation providers), it will deal with data source metadata management and provide trust-able, findable, and retrievable metadata for the data sources.

***************
Features
***************
It will serve as a trusted registry of all the IoT domains/devices and/or ASSIST-IoT enablers that act as data producers. Indexing and querying services will facilitate the efficient retrievability of the stored metadata of the registered producers by consumers in compliance with the FAIR principles.

*********************
Place in architecture
*********************
The Distributed Broker enabler is part of the vertical plane DLT enablers.

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
The Distributed Broker enabler is build using  Hyperledger Fabric Framework. Smart contracts are written in Go.

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
