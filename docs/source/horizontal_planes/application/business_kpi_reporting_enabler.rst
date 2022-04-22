.. _Business KPI reporting enabler:

##############################
Business KPI reporting enabler
##############################

.. contents::
  :local:
  :depth: 1

***************
Introduction
***************
All valuable for log and time-series analytics or Key Performance Indicators (KPIs) desired by the end-user should be available for representation in graphs, charts, pies, etc. The Business KPI enabler will allow to embed them as User Interfaces (UIs) within the tactile dashboard. It will facilitate the visualization and combination of charts, tables, and other visualization graphs in order to search for hidden insights. 

The enabler is a simplified version of `Kibana <https://www.elastic.co/kibana/>`__ . Therefore, it follows the similar architecture. To sum up, it is composed of a server component containing the business logic engine, accompanied with a UI component that defines the graphical UI that users interact with, and a Command Line Interface (CLI) tool especially designed for developers.

***************
Features
***************
The following figure presents the architectural diagram of video augmentation enabler and inside components.

.. figure:: ./BusinessKPI.png
   :alt: Business KPI reporting enabler
 
As it can be seen, it will be mainly formed by four components:

- **Business KPI Server**: Collects data from data collectors (e.g., tactile dashboard PUI9 database, LTSE, or EDBE enablers) into a dedicated database and provides access to it to the UI and CLI components via an internal REST API. 
- **Plugins**: Business KPI functionalities are implemented through modular plugins (Discover, Tag, Lens, Maps, etc.), which contain the business logic and communicate with the UI and CLI components, based on the data collected in the Business KPI server. Furthermore, if will, custom plugins can also be easily integrated if needed, thanks to having a modular approach.
- **Business KPI UI**: When the end-user accesses the Business KPI enabler via the Tactile Dashboard webpage, the UI component loads all server plugins that comprise the core functionalities of the Business KPI enabler. Hence, the UI component provides an editor to create and explore interactive visualizations and a set of functionalities to arrange the visualizations according to ASSIST-IoT end-user goals.
- **Business KPI CLI**: The CLI component enables custom plugins built by 3rd party developers to interact with the Business KPI Server, so that it is reachable from the UI to e.g., provide new data aggregation methods, or to visualize new chart types, colour palettes, etc.

*********************
Place in architecture
*********************

Business KPI reporting enabler is located in the Application and Service layer of the ASSIST-IoT architecture that provides application logic, including data visualisation and user interaction services, data analytics capabilities, various kinds of data protection support, and data management logic. 

***************
User guide
***************

REST API endpoints
*******************
The currently supported REST API endpoints are listed below:

+---------+--------------------------------+------------------------------------------------------+----------------------+------------------+
| Method  | Endpoint                       | Description                                          | Payload (if needed)  | Response format  |
+=========+================================+======================================================+======================+==================+
| POST    | /api/spaces/                   | Create a Business KPI space_name                     | <space_name>         |                  |
+---------+--------------------------------+------------------------------------------------------+----------------------+------------------+
| GET     | /api/spaces/                   | Retrieve a Business KPI space_name                   | <space_name>         |                  |
+---------+--------------------------------+------------------------------------------------------+----------------------+------------------+
| DELETE  | /api/spaces/                   | Delete a Business KPI space_name                     | <space_name>         |                  |
+---------+--------------------------------+------------------------------------------------------+----------------------+------------------+
| POST    | /api/data_views/               | Create a data view with a custom title (JSON file)   | <data_view>          |                  |
+---------+--------------------------------+------------------------------------------------------+----------------------+------------------+
| POST    | /api/saved_objects/data-view/  | Update <my-view> data view (JSON file)               | <my-view>            |                  |
+---------+--------------------------------+------------------------------------------------------+----------------------+------------------+
| GET     | /api/data_views/data_view/     | Retrieve the data view <my-view>                     | <my-view>            |                  |
+---------+--------------------------------+------------------------------------------------------+----------------------+------------------+
| DELETE  | /api/data_views/data_view/     | Delete a data view <my-view>                         | <my-view>            |                  |
+---------+--------------------------------+------------------------------------------------------+----------------------+------------------+


***************
Prerequisites
***************

- Kubernetes >= 1.14
- Helm >= 2.17.0
- `ElasticSearch Helm chart <https://artifacthub.io/packages/helm/elastic/elasticsearch>`__ 

***************
Installation
***************

Installing the chart
*******************
The enabler is provided as a Helm chart. To install the chart with the release name ``my-BKPI``:

``helm install my-BKPI BKPI``

The command deploys a Kibana helm chart on the Kubernetes cluster in the default configuration. The Configuration section lists the parameters that can be configured during installation.

Alternatively, a YAML file that specifies the values for the parameters can be provided while installing the chart. For example,

``helm install my-BKPI -f values.yaml BKPI``



Verification / Visualization
*******************
List all releases using ``helm list``

Uninstalling the Chart
*******************
To uninstall/delete the ``my-BKPI`` deployment:

``helm delete my-BKPI``

*********************
Configuration options
*********************

***************
Developer guide
***************

***************************
Version control and release
***************************
Version 1.0

***************
License
***************
Elastic License and Server Side Public License (SSPL)

********************
Notice(dependencies)
********************
Not applicable
