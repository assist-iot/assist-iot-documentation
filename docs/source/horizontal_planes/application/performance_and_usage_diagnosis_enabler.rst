.. _Performance and Usage Diagnosis enabler:

#######################################
Performance and Usage Diagnosis enabler
#######################################

.. contents::
  :local:
  :depth: 1

***************
Introduction
***************
Performance and Usage Diagnosis (PUD) enabler aims at collecting performance metrics from monitored targets by scraping metrics HTTP endpoints on them and highlighting potential problems in the ASSIST-IoT platform, so that it could autonomously act in accordance or to notify to the platform administrator to fine tuning machine resources. For this purpose we use **Prometheus**, an open-source software that collects metrics from targets by "scraping" metrics HTTP endpoints. Supported "targets" include infrastructure platforms (e.g. Kubernetes), applications, and services (e.g. database management systems). Together with its companion Alertmanager service, Prometheus is a flexible metrics collection and alerting tool.

***************
Features
***************
Prometheus is an open-source monitoring framework. It provides out-of-the-box monitoring capabilities for the Kubernetes container orchestration platform.


- **Metric Collection**: Prometheus uses the pull model to retrieve metrics over HTTP. There is an option to push metrics to Prometheus using Pushgateway for use cases where Prometheus cannot Scrape the metrics.

- **Metric Endpoint**: The systems that you want to monitor using Prometheus should expose the metrics on an /metrics endpoint. Prometheus uses this endpoint to pull the metrics in regular intervals.

- **PromQL**: Prometheus comes with PromQL, a very flexible query language that can be used to query the metrics in the Prometheus dashboard. Also, the PromQL query will be used by Prometheus UI and Grafana to visualize metrics.

- **Prometheus Exporters**: Exporters are libraries which converts existing metric from third-party apps to Prometheus metrics format. There are many official and community Prometheus exporters. One example is, Kube State metrics, a service which talks to Kubernetes API server to get all the details about all the API objects like deployments, pods, daemonsets etc.

- **TSDB** (time-series database): Prometheus uses TSDB for storing all the data. By default, all the data gets stored locally. However, there are options to integrate remote storage for Prometheus TSDB.

*********************
Place in architecture
*********************
**Here is the high-level architecture of Prometheus.**

.. image:: https://prometheus.io/assets/architecture.png

***************
User guide
***************
Prometheus provides a web UI for running basic queries located at `http://<your_server_IP>:9090/`. This is how it looks like in a web browser:

.. image:: https://user-images.githubusercontent.com/100563908/156012977-574cd9f1-5c65-4ae2-bfdf-90c492967e85.PNG
The “Table” tab is used to view the results of a query, while the “Graph” tab is used to create graphs based on a query.

If you want to see a list of metrics sources, go to the Status → Targets page. Here, you will find a list of all services that are being monitored, including the path at which the metrics are available. In this case, the default path /metrics is used.

.. image:: https://user-images.githubusercontent.com/100563908/156013055-80bf10cb-1be4-4b80-9e45-ee31d4ef14c8.PNG

If you’re curious to see how the metrics page looks like, head over to one of them by clicking one of the endpoint URLs.

.. image:: https://user-images.githubusercontent.com/100563908/156013117-33257cdf-2d1d-443b-86c9-37fe6f42d3e4.PNG

***************
Prerequisites
***************
- Kubernetes 1.16+
- Helm 3+

***************
Installation
***************
**PUD Helm Chart**

**Helm** must be installed to use the charts. Please refer to Helm's [documentation](https://helm.sh/docs/) to get started.

- Once Helm is set up properly, add the repo as follows:

    ``helm repo add --username <<Username>> --password <<Token>> PUD https://gitlab.assist-iot.eu/api/v4/projects/60/packages/helm/stable``

    To obtain an Access Token:
    
    1. Go to Settings > Access Tokens.
    
    2. Insert a Token name.
    
    3. Insert an Expiration date (Optional).
    
    4. Select api scope.
    

- Update Helm's repositories.

    ``helm repo update``

- Install PUD's Prometheus to your Kubernetes system using the following command:

    ``helm install PUD/prometheus``

- Install PUD's Prometheus-elastic-adapter, Prometheus' remote storage adapter for Elasticsearch to your Kubernetes system using the following command:

    ``helm install PUD/prometheus-elastic-adapter``

- Install Elasticsearch and Kibana to your Kubernetes system using the following command:

    ``helm install PUD/elasticsearch-kibana``


*********************
Configuration options
*********************

***************
Developer guide
***************
**Prometheus Exporter**

**Prometheus** follows an HTTP pull model: It scrapes Prometheus metrics from endpoints routinely. Typically the abstraction layer between the application and Prometheus is an **exporter**, which takes application-formatted metrics and converts them to Prometheus metrics for consumption. Because Prometheus is an HTTP pull model, the exporter typically provides an endpoint where the Prometheus metrics can be scraped.

The relationship between Prometheus, the exporter, and the application in a Kubernetes environment can be visualized like this:

.. image:: https://trstringer.com/images/prometheus-exporter.png

There are a number of `exporters <https://prometheus.io/docs/instrumenting/exporters/>`_ that are maintained as part of the official `Prometheus GitHub <https://github.com/prometheus>`_

You might need to write your own exporter if:

- You're using 3rd party software that doesn't have an existing exporter already.
- You want to generate Prometheus metrics from software that you have written.

If you decide that you need to write your exporter, there are a handful of available languages and client libraries that you can use: Python, Go, Java, and `others <https://prometheus.io/docs/instrumenting/clientlibs/>`_.

Please refer to Prometheus' `documentation <https://prometheus.io/docs/instrumenting/writing_exporters/>`_ to get started.


***************************
Version control and release
***************************

***************
License
***************

********************
Notice(dependencies)
********************
