.. _Tactile dashboard enabler:

#########################
Tactile dashboard enabler
#########################

.. contents::
  :local:
  :depth: 1

***************
Introduction
***************
The Tactile Dashboard enabler has the capability of representing data through meaningful combined visualizations in real time. It also provides (aggregates and homogenizes) all the User Interfaces (UIs) for the configuration of the different ASSIST-IoT enablers, and associated components.

***************
Features
***************
The tactile dashboard allows the creation of fully reusable web components that can be used to create web pages (SPA) or complex web APPs. The tactile dashboard makes use of Prodevelop's `PUI9 framework <https://mvnrepository.com/artifact/es.prodevelop/es.prodevelop.pui9>`__, which in turn, is based on the `VueJS framework <https://vuejs.org/>`__. It In addition, new applications using the tactile dashboard framework have a basic layout with a login screen and a fully configurable menu. The main advantages of the tactile dashboard framework are:

- Modern, responsive and in some cases adaptive design.
- Very good performance
- Based on web components
- Responsive components
- Each component has its own HTML template, internal Javascript code, styles, and translations
- VueJS has a very gentle learning curve, so it is very easy and quick to start being productive.

Hence, each pilot will implement its own tactile dashboard according to their requirements, but all of them should be based on this framework, which will have in common that they are divided into three main components: Frontend, Backend, and PUI9 database. 

The following figure sketches the architectural diagram of tactile dashboard components.

.. figure:: ./Dashboard_Architecture.png
   :alt: Tactile dashboard

*********************
Place in architecture
*********************
Tactile dashboard is located in the Application and Service layer of the ASSIST-IoT architecture. As the rest of enablers of this horizontal plane, it is designed for for providing data visualisation and user interaction services.

***************
User guide
***************

***************
Prerequisites
***************

***************
Installation
***************

*********************
Configuration options
*********************

***************
Developer guide
***************

***************************
Version control and release
***************************

***************
License
***************
Apache License Version 2.0

********************
Notice(dependencies)
********************
    **NOTE:** It should be noticed that the tactile dashboard is a general GUI generation framework based on PRO own PUI9 framework. 
