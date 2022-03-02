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
Prometheus is an open-source monitoring framework. It provides out-of-the-box monitoring capabilities for the Kubernetes container orchestration platform. Its main features are:


- **Metric Collection**: Prometheus uses the pull model to retrieve metrics over HTTP. There is an option to push metrics to Prometheus using Pushgateway for use cases where Prometheus cannot Scrape the metrics.

- **Metric Endpoint**: The systems that you want to monitor using Prometheus should expose the metrics on an /metrics endpoint. Prometheus uses this endpoint to pull the metrics in regular intervals.

- **PromQL**: Prometheus comes with PromQL, a very flexible query language that can be used to query the metrics in the Prometheus dashboard. Also, the PromQL query will be used by Prometheus UI and Grafana to visualize metrics.

- **Prometheus Exporters**: Exporters are libraries which converts existing metric from third-party apps to Prometheus metrics format. There are many official and community Prometheus exporters. One example is, Kube State metrics, a service which talks to Kubernetes API server to get all the details about all the API objects like deployments, pods, daemonsets etc.

- **TSDB** (time-series database): Prometheus uses TSDB for storing all the data. By default, all the data gets stored locally. However, there are options to integrate remote storage for Prometheus TSDB.

*********************
Place in architecture
*********************

Prometheus scrapes metrics from instrumented jobs. It stores all scraped samples locally and runs rules over this data to either aggregate and record new time series from existing data or generate alerts.

**Here is the high-level architecture of Prometheus.**

.. image:: https://prometheus.io/assets/architecture.png

Prometheus works well for recording any purely numeric time series. It fits both machine-centric monitoring as well as monitoring of highly dynamic service-oriented architectures. In a world of microservices, its support for multi-dimensional data collection and querying is a particular strength.

Prometheus is designed for reliability, to be the system you go to during an outage to allow you to quickly diagnose problems. Each Prometheus server is standalone, not depending on network storage or other remote services. You can rely on it when other parts of your infrastructure are broken, and you do not need to setup extensive infrastructure to use it.
***************
User guide
***************
Prometheus provides a web UI for running basic queries located at `http://<your_server_IP>:9090/`. This is how it looks like in a web browser:

.. image:: https://user-images.githubusercontent.com/100563908/156012977-574cd9f1-5c65-4ae2-bfdf-90c492967e85.PNG
The “Table” tab is used to view the results of a query, while the “Graph” tab is used to create graphs based on a query.

.. image:: https://user-images.githubusercontent.com/100563908/156175560-b75810c9-ae49-45f6-80ff-6b5a59504f35.PNG

If you want to see a list of metrics sources, go to the Status → Targets page. Here, you will find a list of all services that are being monitored, including the path at which the metrics are available. In this case, the default path /metrics is used.

.. image:: https://user-images.githubusercontent.com/100563908/156013055-80bf10cb-1be4-4b80-9e45-ee31d4ef14c8.PNG

If you’re curious to see how the metrics page looks like, head over to one of them by clicking one of the endpoint URLs.

.. image:: https://user-images.githubusercontent.com/100563908/156013117-33257cdf-2d1d-443b-86c9-37fe6f42d3e4.PNG

The Prometheus server collects metrics and stores them in a time series database. Individual metrics are identified with names such as kube_pod_container_resource_requests. A metric may have a number of “labels” attached to it, to distinguish it from other similar sources of metrics. As an example, suppose kube_pod_container_resource_requests refers to the number of requested request resource by a container. It may have a label such as resource, which helps you inspect individual system resources by mentioning them.
 
.. image:: https://user-images.githubusercontent.com/100563908/156173870-734063b3-4ab8-41cc-b511-7c65fa5eb0a9.PNG
 
In PromQL, an expression or subexpression should always evaluate to one of the following data types:

- Instant vector — It represents a time-varying value at a specific point of time.
- Range vector — it represents a time-varying value, over a period of time.
- Scalar — A simple numeric floating point value.
- String — A string value. String literals can be enclosed between single quotes, double quotes or backticks (`). However, escape sequences like \n are only processed when double quotes are used.

For more about Querying please refer to Prometheus' `documentation <https://prometheus.io/docs/prometheus/latest/querying/basics/>`_ to get started.

***************
Prerequisites
***************
- Kubernetes 1.16+
- Helm 3+

***************
Installation
***************
**PUD Helm Chart**

**Helm** must be installed to use the charts. Please refer to Helm's `documentation <https://helm.sh/docs/>`_ to get started.

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

  ``helm install PUD/prometheus --name my-release``

- Install PUD's Prometheus-elastic-adapter, Prometheus' remote storage adapter for Elasticsearch to your Kubernetes system using the following command:

  ``helm install PUD/prometheus-elastic-adapter --name my-release``

- Install Elasticsearch and Kibana to your Kubernetes system using the following command:

  ``helm install PUD/elasticsearch-kibana --name my-release``


*********************
Configuration options
*********************
The following table lists the configurable parameters of the **Prometheus** chart and their default values.

.. list-table::
   :widths: 25 50 20
   :header-rows: 1
   
   * - Parameter
     - Description
     - Default
   * - alertmanager.enabled
     - If true, create alertmanager
     - ``true``
   * - alertmanager.name
     - alertmanager container name
     - ``alertmanager``
   * - alertmanager.useClusterRole
     - Use a ClusterRole (and ClusterRoleBinding). If set to false - we define a Role and RoleBinding in the defined namespaces ONLY. This makes alertmanager work - for users who do not have ClusterAdmin privs, but wants alertmanager to operate on their own namespaces, instead of clusterwide.
     - ``alertmanager``
   * - alertmanager.useExistingRole
     - Set to a rolename to use existing role - skipping role creating - but still doing serviceaccount and rolebinding to the rolename set here.
     - ``alertmanager``
   * - alertmanager.image.repository
     - alertmanager container image repository
     - ``prom/alertmanager``
   * - alertmanager.image.tag
     - alertmanager container image tag
     - ``v0.21.0``
   * - alertmanager.image.pullPolicy
     - alertmanager container image pull policy
     - ``IfNotPresent``
   * - alertmanager.prefixURL
     - The prefix slug at which the server can be accessed
     - ``
   * - alertmanager.baseURL
     - The external url at which the server can be accessed
     - ``"http://localhost:9093"``
   * - alertmanager.extraArgs
     - Additional alertmanager container arguments
     - ``{}``
   * - alertmanager.extraSecretMounts
     - Additional alertmanager Secret mounts
     - ``[]``
   * - alertmanager.configMapOverrideName
     - Prometheus alertmanager ConfigMap override where full-name is {{.Release.Name}}-{{.Values.alertmanager.configMapOverrideName}} and setting this value will prevent the default alertmanager ConfigMap from being generated
     - ``""``
   * - alertmanager.configFromSecret
     - The name of a secret in the same kubernetes namespace which contains the Alertmanager config, setting this value will prevent the default alertmanager ConfigMap from being generated
     - ``""``
   * - alertmanager.configFileName
     - The configuration file name to be loaded to alertmanager. Must match the key within configuration loaded from ConfigMap/Secret.
     - ``alertmanager.yml``
   * - alertmanager.ingress.enabled
     - If true, alertmanager Ingress will be created
     - ``false``
   * - alertmanager.ingress.annotations
     - alertmanager Ingress annotations
     - ``{}``
   * - alertmanager.ingress.extraLabels
     - alertmanager Ingress additional labels
     - ``{}``
   * - alertmanager.ingress.hosts
     - alertmanager Ingress hostnamesv
     - ``[]``
   * - alertmanager.ingress.extraPaths
     - Ingress extra paths to prepend to every alertmanager host configuration. Useful when configuring custom actions with AWS ALB Ingress Controller
     - ``[]``
   * - alertmanager.ingress.tls
     - alertmanager Ingress TLS configuration (YAML)
     - ``[]``
   * - alertmanager.nodeSelector
     - node labels for alertmanager pod assignment
     - ``{}``
   * - alertmanager.tolerations
     - node taints to tolerate (requires Kubernetes >=1.6)
     - ``[]``
   * - alertmanager.affinity
     - pod affinity
     - ``{}``
   * - alertmanager.podDisruptionBudget.enabled
     - If true, create a PodDisruptionBudget
     - ``false``
   * - alertmanager.podDisruptionBudget.maxUnavailable
     - Maximum unavailable instances in PDB
     - ``1``
   * - alertmanager.schedulerName
     - alertmanager alternate scheduler name
     - ``nil``
   * - alertmanager.persistentVolume.enabled
     - If true, alertmanager will create a Persistent Volume Claim
     - ``true``
   * - alertmanager.persistentVolume.accessModes
     - alertmanager data Persistent Volume access modes
     - ``[ReadWriteOnce]``
   * - alertmanager.persistentVolume.annotations
     - Annotations for alertmanager Persistent Volume Claim
     - ``{}``
   * - alertmanager.persistentVolume.existingClaim
     - alertmanager data Persistent Volume existing claim name
     - ``""``
   * - alertmanager.persistentVolume.mountPath
     - alertmanager data Persistent Volume mount root path
     - ``/data``
   * - alertmanager.persistentVolume.size
     - alertmanager data Persistent Volume size
     - ``2Gi``
   * - alertmanager.persistentVolume.storageClass
     - alertmanager data Persistent Volume Storage Class
     - ``unset``
   * - alertmanager.persistentVolume.volumeBindingMode
     - alertmanager data Persistent Volume Binding Mode
     - ``unset``
   * - alertmanager.persistentVolume.subPath
     - Subdirectory of alertmanager data Persistent Volume to mount
     - ``""``
   * - alertmanager.podAnnotations
     - annotations to be added to alertmanager pods
     - ``{}``
   * - alertmanager.podLabels
     - labels to be added to Prometheus AlertManager pods
     - ``{}``
   * - alertmanager.podSecurityPolicy.annotations
     - Specify pod annotations in the pod security policy
     - ``{}``
   * - alertmanager.replicaCount
     - desired number of alertmanager pods
     - ``1``
   * - alertmanager.statefulSet.enabled
     - If true, use a statefulset instead of a deployment for pod management
     - ``false``
   * - alertmanager.statefulSet.podManagementPolicy
     - podManagementPolicy of alertmanager pods
     - ``OrderedReady``
   * - alertmanager.statefulSet.headless.annotations
     - annotations for alertmanager headless service
     - ``{}``
   * - alertmanager.statefulSet.headless.labels
     - labels for alertmanager headless service
     - ``{}``
   * - alertmanager.statefulSet.headless.enableMeshPeer
     - If true, enable the mesh peer endpoint for the headless service
     - ``false``
   * - alertmanager.statefulSet.headless.servicePort
     - alertmanager headless service port
     - ``80``
   * - alertmanager.priorityClassName
     - alertmanager priorityClassName
     - ``nil``
   * - alertmanager.resources
     - alertmanager pod resource requests & limits
     - ``{}``
   * - alertmanager.securityContext
     - Custom security context for Alert Manager containers
     - ``{}``
   * - alertmanager.service.annotations
     - annotations for alertmanager service
     - ``{}``
   * - alertmanager.service.clusterIP
     - internal alertmanager cluster service IP
     - ``""``
   * - alertmanager.service.externalIPs
     - alertmanager service external IP addresses
     - ``[]``
   * - alertmanager.service.loadBalancerIP
     - IP address to assign to load balancer (if supported)
     - ``""``
   * - alertmanager.service.loadBalancerSourceRanges
     - list of IP CIDRs allowed access to load balancer (if supported)
     - ``[]``
   * - alertmanager.service.servicePort
     - alertmanager service port
     - ``80``
   * - alertmanager.service.sessionAffinity
     - Session Affinity for alertmanager service, can be None or ClientIP
     - ``None``
   * - alertmanager.service.type
     - type of alertmanager service to create
     - ``ClusterIP``
   * - alertmanager.strategy
     - Deployment strategy
     - ``{ "type": "RollingUpdate" }``
   * - alertmanagerFiles.alertmanager.yml
     - Prometheus alertmanager configuration
     - ``example configuration``
   * - configmapReload.prometheus.enabled
     - If false, the configmap-reload container for Prometheus will not be deployed
     - ``true``
   * - configmapReload.prometheus.name
     - configmap-reload container name
     - ``configmap-reload``
   * - configmapReload.prometheus.image.repository
     - configmap-reload container image repository
     - ``jimmidyson/configmap-reload``
   * - configmapReload.prometheus.image.tag
     - configmap-reload container image tag
     - ``v0.4.0``
   * - configmapReload.prometheus.image.pullPolicy
     - configmap-reload container image pull policy
     - ``IfNotPresent``
   * - configmapReload.prometheus.extraArgs
     - Additional configmap-reload container arguments
     - ``{}``
   * - configmapReload.prometheus.extraVolumeDirs
     - Additional configmap-reload volume directories
     - ``{}``
   * - configmapReload.prometheus.extraConfigmapMounts
     - Additional configmap-reload configMap mounts
     - ``[]``
   * - configmapReload.prometheus.resources
     - configmap-reload pod resource requests & limits
     - ``{}``
   * - configmapReload.alertmanager.enabled
     - If false, the configmap-reload container for AlertManager will not be deployed
     - ``true``
   * - configmapReload.alertmanager.name
     - configmap-reload container name
     - ``configmap-reload``
   * - configmapReload.alertmanager.image.repository
     - configmap-reload container image repository
     - ``jimmidyson/configmap-reload``
   * - configmapReload.alertmanager.image.repository
     - configmap-reload container image repository
     - ``jimmidyson/configmap-reload``
   * - configmapReload.alertmanager.image.tag
     - configmap-reload container image tag
     - ``v0.4.0``
   * - configmapReload.alertmanager.image.pullPolicy
     - configmap-reload container image pull policy
     - ``IfNotPresent``
   * - configmapReload.alertmanager.extraArgs
     - Additional configmap-reload container arguments
     - ``{}``
   * - configmapReload.alertmanager.extraVolumeDirs
     - Additional configmap-reload volume directories
     - ``{}``
   * - configmapReload.alertmanager.extraConfigmapMounts
     - Additional configmap-reload configMap mounts
     - ``[]``
   * - configmapReload.alertmanager.resources
     - configmap-reload pod resource requests & limits
     - ``{}``
   * - initChownData.enabled
     - If false, don't reset data ownership at startup
     - ``true``
   * - initChownData.name
     - init-chown-data container name
     - ``init-chown-data``
   * - initChownData.image.repository
     - init-chown-data container image repository
     - ``busybox``
   * - initChownData.image.tag
     - init-chown-data container image tag
     - ``latest``
   * - initChownData.image.pullPolicy
     - init-chown-data container image pull policy
     - ``IfNotPresent``
   * - initChownData.resources
     - init-chown-data pod resource requests & limits
     - ``{}``
   * - kubeStateMetrics.enabled
     - If true, create kube-state-metrics sub-chart
     - ``true``
   * - kube-state-metrics
     - kube-state-metrics configuration options
     - ``Same as sub-chart's``
   * - rbac.create
     - If true, create & use RBAC resources
     - ``true``
   * - server.enabled
     - If false, Prometheus server will not be created
     - ``true``
   * - server.name
     - Prometheus server container name
     - ``server``
   * - server.image.repository
     - Prometheus server container image repository
     - ``prom/prometheus``
   * - server.image.tag
     - Prometheus server container image tag
     - ``v2.20.1``
   * - server.image.pullPolicy
     - Prometheus server container image pull policy
     - ``IfNotPresent``
   * - server.configPath
     - Path to a prometheus server config file on the container FS
     - ``/etc/config/prometheus.yml``
   * - server.global.scrape_interval
     - How frequently to scrape targets by default
     - ``1m``
   * - server.global.scrape_timeout
     - How long until a scrape request times out
     - ``10s``
   * - server.global.evaluation_interval
     - How frequently to evaluate rules
     - ``1m``
   * - server.remoteWrite
     - The remote write feature of Prometheus allow transparently sending samples.
     - ``[]``
   * - server.remoteRead
     - The remote read feature of Prometheus allow transparently receiving samples.
     - ``[]``
   * - server.extraArgs
     - Additional Prometheus server container arguments
     - ``{}``
   * - server.extraFlags
     - Additional Prometheus server container flags
     - ``["web.enable-lifecycle"]``
   * - server.extraInitContainers
     - Init containers to launch alongside the server
     - ``[]``
   * - server.prefixURL
     - The prefix slug at which the server can be accessed
     - ``
   * - server.baseURL
     - The external url at which the server can be accessed
     - ``
   * - server.env
     - Prometheus server environment variables
     - ``[]``
   * - server.extraHostPathMounts
     - Additional Prometheus server hostPath mounts
     - ``[]``
   * - server.extraConfigmapMounts
     - Additional Prometheus server configMap mounts
     - ``[]``
   * - server.extraSecretMounts
     - Additional Prometheus server Secret mounts
     - ``[]``
   * - server.extraVolumeMounts
     - Additional Prometheus server Volume mounts
     - ``[]``
   * - server.extraVolumes
     - Additional Prometheus server Volumes
     - ``[]``
   * - server.configMapOverrideName
     - Prometheus server ConfigMap override where full-name is {{.Release.Name}}-{{.Values.server.configMapOverrideName}} and setting this value will prevent the default server ConfigMap from being generated
     - ``""``
   * - server.ingress.enabled
     - If true, Prometheus server Ingress will be created
     - ``false``
   * - server.ingress.annotations
     - Prometheus server Ingress annotations
     - ``[]``
   * - server.ingress.extraLabels
     - Prometheus server Ingress additional labels
     - ``{}``
   * - server.ingress.hosts
     - Prometheus server Ingress hostnames
     - ``[]``
   * - server.ingress.extraPaths
     - Ingress extra paths to prepend to every Prometheus server host configuration. Useful when configuring custom actions with AWS ALB Ingress Controller
     - ``[]``
   * - server.ingress.tls
     - Prometheus server Ingress TLS configuration (YAML)
     - ``[]``
   * - server.nodeSelector
     - node labels for Prometheus server pod assignment
     - ``{}``
   * - server.tolerations
     - node taints to tolerate (requires Kubernetes >=1.6)
     - ``[]``
   * - server.affinity
     - pod affinity
     - ``{}``
   * - server.podDisruptionBudget.enabled
     - If true, create a PodDisruptionBudget
     - ``false``
   * - server.podDisruptionBudget.maxUnavailable
     - Maximum unavailable instances in PDB
     - ``1``
   * - server.priorityClassName
     - Prometheus server priorityClassName
     - ``nil``
   * - server.enableServiceLinks
     - Set service environment variables in Prometheus server pods
     - ``true``
   * - server.schedulerName
     - Prometheus server alternate scheduler name
     - ``nil``
   * - server.persistentVolume.enabled
     - If true, Prometheus server will create a Persistent Volume Claim
     - ``true``
   * - server.persistentVolume.accessModes
     - Prometheus server data Persistent Volume access modes
     - ``[ReadWriteOnce]``
   * - server.persistentVolume.annotations
     - Prometheus server data Persistent Volume annotations
     - ``{}``
   * - server.persistentVolume.existingClaim
     - Prometheus server data Persistent Volume existing claim name
     - ``""``
   * - server.persistentVolume.mountPath
     - Prometheus server data Persistent Volume mount root path
     - ``/data``
   * - server.persistentVolume.size
     - Prometheus server data Persistent Volume size
     - ``8Gi``
   * - server.persistentVolume.storageClass
     - Prometheus server data Persistent Volume Storage Class
     - ``unset``
   * - server.persistentVolume.volumeBindingMode
     - Prometheus server data Persistent Volume Binding Mode
     - ``unset``
   * - server.persistentVolume.subPath
     - Subdirectory of Prometheus server data Persistent Volume to mount
     - ``""``
   * - server.emptyDir.sizeLimit
     - emptyDir sizeLimit if a Persistent Volume is not used
     - ``""``
   * - server.podAnnotations
     - annotations to be added to Prometheus server pods
     - ``{}``
   * - server.podLabels
     - labels to be added to Prometheus server pods
     - ``{}``
   * - server.alertmanagers
     - Prometheus AlertManager configuration for the Prometheus server
     - ``{}``
   * - server.deploymentAnnotations
     - annotations to be added to Prometheus server deployment
     - ``{}``
   * - server.podSecurityPolicy.annotations
     - Specify pod annotations in the pod security policy
     - ``{}``
   * - server.replicaCount
     - desired number of Prometheus server pods
     - ``1``
   * - server.statefulSet.enabled
     - If true, use a statefulset instead of a deployment for pod management
     - ``false``
   * - server.statefulSet.annotations
     - annotations to be added to Prometheus server stateful set
     - ``{}``
   * - server.statefulSet.labels
     - labels to be added to Prometheus server stateful set
     - ``{}``
   * - server.statefulSet.podManagementPolicy
     - podManagementPolicy of server pods
     - ``OrderedReady``
   * - server.podLabels
     - labels to be added to Prometheus server pods
     - ``{}``
   * - server.alertmanagers
     - Prometheus AlertManager configuration for the Prometheus server
     - ``{}``
   * - server.deploymentAnnotations
     - annotations to be added to Prometheus server deployment
     - ``{}``
   * - server.podSecurityPolicy.annotations
     - Specify pod annotations in the pod security policy
     - ``{}``
   * - server.replicaCount
     - desired number of Prometheus server pods
     - ``1``
   * - server.statefulSet.enabled
     - If true, use a statefulset instead of a deployment for pod management
     - ``false``
   * - server.statefulSet.annotations
     - annotations to be added to Prometheus server stateful set
     - ``{}``
   * - server.statefulSet.labels
     - labels to be added to Prometheus server stateful set
     - ``{}``
   * - server.statefulSet.podManagementPolicy
     - podManagementPolicy of server pods
     - ``OrderedReady``
   * - server.statefulSet.headless.annotations
     - annotations for Prometheus server headless service
     - ``{}``
   * - server.statefulSet.headless.labels
     - labels for Prometheus server headless service
     - ``{}``
   * - server.statefulSet.headless.servicePort
     - Prometheus server headless service port
     - ``80``
   * - server.statefulSet.headless.gRPC.enabled
     - If true, open a second port on the service for gRPC
     - ``false``
   * - server.statefulSet.headless.gRPC.servicePort
     - Prometheus service gRPC port, (ignored if server.service.gRPC.enabled is not true)
     - ``10901``
   * - server.statefulSet.headless.gRPC.nodePort
     - Port to be used as gRPC nodePort in the prometheus service
     - ``0``
   * - server.readinessProbeInitialDelay
     - the initial delay for the Prometheus server readiness probe
     - ``30``
   * - server.readinessProbePeriodSeconds
     - how often (in seconds) to perform the Prometheus server readiness probe
     - ``5``
   * - server.readinessProbeTimeout
     - the timeout for the Prometheus server readiness probe
     - ``30``
   * - server.readinessProbeFailureThreshold
     - the failure threshold for the Prometheus server readiness probe
     - ``3``
   * - server.readinessProbeSuccessThreshold
     - the success threshold for the Prometheus server readiness probe
     - ``1``
   * - server.livenessProbeInitialDelay
     - the initial delay for the Prometheus server liveness probe
     - ``30``
   * - server.livenessProbePeriodSeconds
     - how often (in seconds) to perform the Prometheus server liveness probe
     - ``15``
   * - server.livenessProbeTimeout
     - the timeout for the Prometheus server liveness probe
     - ``30``
   * - server.livenessProbeFailureThreshold
     - the failure threshold for the Prometheus server liveness probe
     - ``3``
   * - server.livenessProbeSuccessThreshold
     - the success threshold for the Prometheus server liveness probe
     - ``1``
   * - server.resources
     - Prometheus server resource requests and limits
     - ``{}``
   * - server.verticalAutoscaler.enabled
     - If true a VPA object will be created for the controller (either StatefulSet or Deployemnt, based on above configs)
     - ``false``
   * - server.securityContext
     - Custom security context for server containers
     - ``{}``
   * - server.service.annotations
     - annotations for Prometheus server service
     - ``{}``
   * - server.service.clusterIP
     - internal Prometheus server cluster service IP
     - ``""``
   * - server.service.externalIPs
     - Prometheus server service external IP addresses
     - ``[]``
   * - server.service.loadBalancerIP
     - IP address to assign to load balancer (if supported)
     - ``""``
   * - server.service.loadBalancerSourceRanges
     - list of IP CIDRs allowed access to load balancer (if supported)
     - ``[]``
   * - server.service.nodePort
     - Port to be used as the service NodePort (ignored if server.service.type is not NodePort)
     - ``0``
   * - server.service.servicePort
     - Prometheus server service port
     - ``80``
   * - server.service.sessionAffinity
     - Session Affinity for server service, can be None or ClientIP
     - ``None``
   * - server.service.type
     - type of Prometheus server service to create
     - ``ClusterIP``
   * - server.service.gRPC.enabled
     - If true, open a second port on the service for gRPC
     - ``false``
   * - server.service.gRPC.servicePort
     - Prometheus service gRPC port, (ignored if server.service.gRPC.enabled is not true)
     - ``10901``
   * - server.service.gRPC.nodePort
     - Port to be used as gRPC nodePort in the prometheus service
     - ``0``
   * - server.service.statefulsetReplica.enabled
     - If true, send the traffic from the service to only one replica of the replicaset
     - ``false``
   * - server.service.statefulsetReplica.replica
     - Which replica to send the traffice to
     - ``0``
   * - server.hostAliases
     - /etc/hosts-entries in container(s)
     - ``[]``
   * - server.sidecarContainers
     - array of snippets with your sidecar containers for prometheus server
     - ``""``
   * - server.strategy
     - Deployment strategy
     - ``{ "type": "RollingUpdate" }``
   * - serviceAccounts.alertmanager.create
     - If true, create the alertmanager service account
     - ``true``
   * - serviceAccounts.alertmanager.name
     - name of the alertmanager service account to use or create
     - ``{{ prometheus.alertmanager.fullname }}``
   * - serviceAccounts.alertmanager.annotations
     - annotations for the alertmanager service account
     - ``{}``
   * - serviceAccounts.server.create
     - If true, create the server service account
     - ``true``
   * - serviceAccounts.server.name
     - name of the server service account to use or create
     - ``{{ prometheus.server.fullname }}``
   * - serviceAccounts.server.annotations
     - annotations for the server service account
     - ``{}``
   * - server.terminationGracePeriodSeconds
     - Prometheus server Pod termination grace period
     - ``300``
   * - server.retention
     - (optional) Prometheus data retention
     - ``"15d"``
   * - serverFiles.alerting_rules.yml
     - Prometheus server alerts configuration
     - ``{}``
   * - serverFiles.recording_rules.yml
     - Prometheus server rules configuration
     - ``{}``
   * - serverFiles.prometheus.yml
     - Prometheus server scrape configuration
     - ``example configuration``
   * - extraScrapeConfigs
     - Prometheus server additional scrape configuration
     - ``""``
   * - alertRelabelConfigs
     - Prometheus server alert relabeling configs for H/A prometheus
     - ``""``
   * - networkPolicy.enabled
     - Enable NetworkPolicy
     - ``false``
   * - forceNamespace
     - Force resources to be namespaced
     - ``null``

Specify each parameter using the ``--set key=value[,key=value]`` argument to ``helm install``. For example:

``helm install PUD/prometheus --name my-release --set server.terminationGracePeriodSeconds=360``

Alternatively, a YAML file that specifies the values for the above parameters can be provided while installing the chart. For example:

``helm install PUD/prometheus --name my-release -f values.yaml``

The following table lists the configurable parameters of the **Prometheus-elasticsearch-adapter** chart and their default values.

.. list-table::
   :widths: 25 50 20
   :header-rows: 1
   
   * - Env Variables
     - Description
     - Default
   * - ES_URL
     - Elasticsearch URL
     - ``http://localhost:9200``
   * - ES_USER
     - Elasticsearch User
     - 
   * - ES_PASSWORD
     - Elasticsearch User Password
     - 
   * - ES_WORKERS
     - Number of batch workers
     - ``1``
   * - ES_BATCH_MAX_AGE
     - Max period in seconds between bulk Elasticsearch insert operations
     - ``10``
   * - ES_BATCH_MAX_DOCS
     - Max items for bulk Elasticsearch insert operation
     - ``1000``
   * - ES_BATCH_MAX_SIZE
     - Max size in bytes for bulk Elasticsearch insert operation
     - ``4096``
   * - ES_ALIAS
     - Elasticsearch alias pointing to active write index
     - ``prom-metrics``
   * - ES_INDEX_DAILY
     - Create daily indexes and disable index rollover
     - ``false``
   * - ES_INDEX_SHARDS
     - Number of Elasticsearch shards to create per index
     - ``5``
   * - ES_INDEX_REPLICAS
     - Number of Elasticsearch replicas to create per index
     - ``1``
   * - ES_INDEX_MAX_AGE
     - Max age of Elasticsearch index before rollover
     - ``7d``
   * - ES_INDEX_MAX_DOCS
     - Max number of docs in Elasticsearch index before rollover
     - ``1000000``
   * - ES_INDEX_MAX_SIZE
     - Max size of index before rollover eg 5gb
     - 
   * - ES_SEARCH_MAX_DOCS
     - Max number of docs returned for Elasticsearch search operation
     - ``1000``
   * - ES_SNIFF
     - Enable Elasticsearch sniffing
     - ``false``
   * - STATS
     - Expose Prometheus metrics endpoint
     - ``true``
   * - DEBUG
     - Display extra debug logs
     - ``false``

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

Prometheus v2.31.1

Prometheus-es-adapter v3.3

ElasticSearch v6.4.2

Kibana v6.4.2

***************
License
***************

**Apache License 2.0**

********************
Notice(dependencies)
********************
