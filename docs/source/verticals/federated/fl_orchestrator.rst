.. _FL Orchestrator:

############
FL Orchestrator
############

.. contents::
  :local:
  :depth: 1

***************
Introduction
***************
**FL Orchestrator** is one of the enablers developed in the context of the **FL Architecture** of the `ASSIST-IoT project

***************
Features
***************

FL Orchestrator is responsible of specifying details of FL workflow(s)/pipeline(s). Among these details or features are:

- FL job scheduling
- Manage the FL life cycle
- Selecting and delivering initial version(s) of the shared algorithm
- Delivering the version(s) of modules used in various stages of the process, such as training stopping criteria
- Handling the different “error conditions” that may occur during the FL process

*********************
Place in architecture
*********************
Next picture depicts the FL architecture

.. figure:: ./fl_architecture.png
   :alt: FL Architecture

It is in the centre of the image. It is the core element of the architecture and is responsible for initiating the different iterations of model training.

***************
User guide
***************

   **To be completed**

***************
Prerequisites
***************

The main prerequisites are the installation of
`Docker <https://docs.docker.com/get-started/overview/>`__ and `Docker-compose <https://docs.docker.com/compose/>`__.

The following links provide information on how to install `Docker <https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-20-04>`__
and `Docker-compose <https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-compose-on-ubuntu-20-04>`__.

These prerequisites are necessary in case of running the enabler as a container (**Docker**). However, it is also possible to run the component independently. In this case, it’s mandatory to have Python installed on the machine where the Orchestrator will be executed. At least version 3.8 is recommended (this is the version of the Python image being used). It is also necessary to install some additinal libraries or packages. These additional packages can be seen in the requirements.txt file (inside the orchestrator folder).

The following image illustrates the libraries needed for the orchestrator.

.. figure:: ./requirements.PNG
   :alt: Additional pacckages in the requirements.txt file

***************
Installation
***************
The first version of FL Orchestrator will be deployed with **docker-compose**. This file includes all the services needed to be able to deploy the FL Orchestrator API.

Next picture depicts the content of this docker-compose.

.. figure:: ./docker-compose.png
   :alt: Docker-compose file and their services

This version of docker-compose file includes 3 services:

- **orchestrator**. Core of the enabler. Includes the definition of the API, interaction with other enablers and their main features.
- **mongo**. Deploys a `MongoDB <https://en.wikipedia.org/wiki/MongoDB>`__ instance used by the orchestrator to retrieve the list of existing models. Once the orchestrator is integrated with the repository, the list of models will be retrieved from this component. However, the MongoDB instance can be shared between these two components.
- **mongo-seed-models**. Service developed to insert example models into MongoDB. Needed in development phase. Once the component is integrated with the rest of the elements, this service will not be necessary.
   
Verification
------------
FL Orchestrator and the other enablers have been conceived as APIs that will have methods that interact with each other. Therefore, the best to verify their correct deployment and operation is to test these APIs.

FL Orchestrator has a `Swagger <https://swagger.io/docs/specification/2-0/what-is-swagger/>`__ that allows to test all its methods. This swagger is deployed at the
following URL: http://localhost:5000/api/docs

Next picture shows the appearance of the swagger and some of its methods.

.. figure:: ./fl_orchestrator_swagger.PNG
   :alt: Swagger for the FL Orchestrator

Expanding the method area (/models) in our case. The Execute option appears. Clicking on this button and if the method has the required parameters, the result code is obtained (200, in case it has gone well). Also in the `curl <https://curl.se/>`__ area, it is possible to see the request that would be made to execute this method externally. In the Response body area it is possible to see the result, the list of the models that currently are stored in the FL Repository.

Next picture depicts what has been explained in the previous paragraph. The areas **code**, **curl** and **Response body** are highlight.

.. figure:: ./testing_swagger.png
   :alt: Testing models method of FL Orchestrator API
   
Building the Docker image
------------

The different Docker images needed to be able to deploy all the services are defined / created in files called `Dockerfile <https://docs.docker.com/engine/reference/builder/>`__.

These files are based on an initial image and the rest of the packages / libraries needed to execute the `Python <https://www.python.org/doc/essays/blurb/>`__ scripts (in our case) are installed on top of it.

Next picture depicts the content of one of this Dockerfile.

.. figure:: ./Dockerfile.PNG
   :alt: Dockerfile for building the image of the orchestrator


Deploying with Kubernetes and Helm3
------------

   **To be completed**

Verification the deployment
------------

   **To be completed**

*********************
Configuration options
*********************

   **To be completed**

***************
Developer guide
***************

   **To be completed**

***************************
Version control and release
***************************
The table of this section it is a software release overview of the different elements for the orchestrator’s enabler. The division has been made on the basis of the different files (or folders) needed to execute the component. This is shown in the following figure.

.. figure:: ./components.PNG
   :alt: Division of elements for executing the orchestrator

+-------------------------+-------------------------------+-----------+
| File Name / Folder      | Description                   | Language  |
+=========================+===============================+===========+
| docker-compose.yml      | Docker compose file           | `YAML <ht |
|                         | responsible for launching the | tps://en. |
|                         | services needed for the       | wikipedia |
|                         | orchestrator                  | .org/wiki |
|                         |                               | /YAML>`__ |
+-------------------------+-------------------------------+-----------+
| orchestrator            | Folder containing the scripts | Python,   |
|                         | needed to run the             | YAML,     |
|                         | orchestrator service. It also | `CSS <htt |
|                         | contains the files and        | ps://www. |
|                         | folders necessary to be able  | w3schools |
|                         | to deploy a swagger of the    | .com/css/ |
|                         | component                     | css_intro |
|                         |                               | .asp>`__, |
|                         |                               | `HT       |
|                         |                               | ML <https |
|                         |                               | ://www.w3 |
|                         |                               | schools.c |
|                         |                               | om/html/h |
|                         |                               | tml_intro |
|                         |                               | .asp>`__, |
|                         |                               | `         |
|                         |                               | JavaScrip |
|                         |                               | t <https: |
|                         |                               | //www.w3s |
|                         |                               | chools.co |
|                         |                               | m/whatis/ |
|                         |                               | whatis_js |
|                         |                               | .asp>`__, |
|                         |                               | `JS       |
|                         |                               | ON <https |
|                         |                               | ://www.w3 |
|                         |                               | schools.c |
|                         |                               | om/js/js_ |
|                         |                               | json_intr |
|                         |                               | o.asp>`__ |
+-------------------------+-------------------------------+-----------+
| mongo-seed-models       | Folder containing the scripts | YAML,     |
|                         | needed to do an initial load  | JSON      |
|                         | of the models into the        |           |
|                         | MongoDB instance              |           |
+-------------------------+-------------------------------+-----------+
***************
License
***************

   **To be completed**

********************
Notice(dependencies)
********************

   **To be completed**
