.. _Edge Data Broker enabler:

########################
Edge Data Broker enabler
########################

.. contents::
  :local:
  :depth: 1

***************
Introduction
***************
The Edge Data Broker enables the efficient management of data demand and data supply among edge nodes based on 
a publish/subscribe schema, taking account load balancing criteria. This enabler distributes data where it is 
needed for application, services and further analysis while considered essential only in those deployments that 
involve IoT architectures.

***************
Features
***************
The Edge Data Broker enabler has the following operational and intelligent functionalities:

- Subscriptions and messages between Edge Devices through the Edge Data Broker enabler
- Management and distribution of messages using scheduling, routing and delivery mechanisms
- Common interfaces for searching and finding information
- Integration with other data brokers if needed

*********************
Place in architecture
*********************
The Edge Data Broker enabler is part of the Data Management Plane of ASSIST-IoT. The Data Management plane 
encompasses any process, in which data is processed to deliver features concerning data interoperability, 
annotation, security, acquisition, provenance, aggregation, fusion, etc. This enabler provides a data 
communication channel to all IoT devices.

***************
User guide
***************
The Edge Data Broker is an distributed MQTT Broker and follows the MQTT specification. As such in theory any
MQTT compliant library can be used to connect, subscribe and publish messages to the Edge Data Broker.Here 
we provide an example using python.

This is a subscriber python script that uses the paho-mqtt library to connect to the Edge Data Broker, subscribe
to a topic and receive and print messages from it.

.. code-block:: python
    :emphasize-lines: 3,5

    import paho.mqtt.client as mqtt

    broker= "127.0.0.1"
    port  = 31883
    topic = "assist.test"

    # The callback for when the client receives a CONNACK response from the server.
    def on_connect(client, userdata, rc, test):
        print("Connected with result code "+str(rc))
        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        client.subscribe(topic)

    # The callback for when a PUBLISH message is received from the server.
    def on_message(client, userdata, msg):
        print(msg.topic+" "+str(msg.payload))

    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(broker, port, 60)

    # Blocking call that processes network traffic, dispatches callbacks and
    # handles reconnecting.
    # Other loop*() functions are available that give a threaded interface and a
    # manual interface.
    client.loop_forever()

This is a publisher python script that uses the paho-mqtt library to connect to the Edge Data Broker, subscribe
to a topic and publishes messages to it.

.. code-block:: python
    :emphasize-lines: 3,5
    
    import paho.mqtt.client as paho
    import json, time

    #broker= "10.0.2.15"
    broker= "127.0.0.1"
    port  = 31883
    topic = "assist.test"

    # The callback for when the client receives a CONNACK response from the server.
    def on_connect(client, userdata, rc, test):
        print("Connected with result code "+str(rc))

    def on_publish(client,userdata,result):                    # create function for callback
        print("data published!")
        pass

    client1= paho.Client("control1")                           # create client object
    client1.on_publish = on_publish                            # assign function to callback
    client1.on_connect = on_connect
    client1.connect(broker,port)                               # establish connection
    print("Connected to MQTT")
    body = {}
    body["name"] = "DeviceName"
    body["raw-data"] = 1.000

    i = 0
    while i < 1000 :
        body["raw-data"] = float(i)
        bodyS = json.dumps(body)
        print("Publishig data: " + bodyS)
        ret= client1.publish(topic, bodyS)               # publish
        i += 1
        time.sleep(0.1)

Executing those two scripts will produce and consume json messages to the Edge Data Broker.

***************
Prerequisites
***************
The Edge Data Broker enabler is designed to be executed on a cluster of devices on ARM64 
architecture. It can be executed of course on a x86 architecture as well by changing the 
docker image. It also requires Docker for building a new image and kubernetes/helm3 to
deploy the enabler on a cluster.

***************
Installation
***************

Building the Docker image
--------------------------
On the Docker folder execute:
::

  $ docker build . -t edb:latest

This will create the image. It should be visible with:
::

  $ docker images

To push the image to a registry (using a local registry for this example):
:: 

  $ docker tag edb:latest localhost:32000/edb:latest

  $ docker tag edb:latest localhost:32000/edb:latest

Now we can use this image in kubernetes and helm.

Deploying with Kubernetes and Helm3
------------------------------------

On the Helm folder execute:
::

  $ cp values.yaml values.yaml.bu
  $ helm3 install edb -f values.yaml .

This will install the enabler. To uninstall:
::

  $ helm3 uninstall edb


Verification
-------------

Using the kubectl command:
::

  $ kubectl get all -o wide
  NAME        READY   STATUS    RESTARTS   AGE   IP             NODE     NOMINATED NODE   READINESS GATES
  pod/edb-0   1/1     Running   0          9d    10.1.196.152   node01   <none>           <none>
  pod/edb-1   1/1     Running   0          9d    10.1.140.84    node02   <none>           <none>

  NAME                   TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)                         AGE   SELECTOR
  service/kubernetes     ClusterIP   10.152.183.1     <none>        443/TCP                         15d   <none>
  service/edb-headless   ClusterIP   None             <none>        4369/TCP,8888/TCP               9d    
  app.kubernetes.io/instance=edb,app.kubernetes.io/name=edb
  service/edb            NodePort    10.152.183.168   <none>        1883:31883/TCP,8888:30888/TCP   9d    
  app.kubernetes.io/instance=edb,app.kubernetes.io/name=edb

  NAME                   READY   AGE   CONTAINERS   IMAGES
  statefulset.apps/edb   2/2     9d    edb          localhost:32000/edb:latest

Also, the python scripts (provided in the User Guide section above) with the correct IP and PORT values can be used for testing.

*********************
Configuration options
*********************

The following table lists the configurable parameters of the chart and their default values.

+----------------------+----------------------+----------------------+
| Parameter            | Description          | Default              |
+======================+======================+======================+
| ``additionalEnv``    | additional           | see                  |
|                      | environment          | `values.y            |
|                      | variables            | aml <values.yaml>`__ |
+----------------------+----------------------+----------------------+
| ``envFrom``          | additional envFrom   | see                  |
|                      | configmaps or        | `values.y            |
|                      | secrets              | aml <values.yaml>`__ |
+----------------------+----------------------+----------------------+
| ``image.pullPolicy`` | container image pull | ``IfNotPresent``     |
|                      | policy               |                      |
+----------------------+----------------------+----------------------+
| ``image.repository`` | container image      | ``vernemq/vernemq``  |
|                      | repository           |                      |
+----------------------+----------------------+----------------------+
| ``image.tag``        | container image tag  | the current versions |
|                      |                      | (e.g. ``1.12.3``)    |
+----------------------+----------------------+----------------------+
| ``ingress.enabled``  | whether to enable an | ``false``            |
|                      | ingress object to    |                      |
|                      | route to the         |                      |
|                      | WebSocket service.   |                      |
|                      | Requires an ingress  |                      |
|                      | controller and the   |                      |
|                      | WebSocket service to |                      |
|                      | be enabled.          |                      |
+----------------------+----------------------+----------------------+
| ``ingress.labels``   | additional ingress   | ``{}``               |
|                      | labels               |                      |
+----------------------+----------------------+----------------------+
| ``i                  | additional service   | ``{}``               |
| ngress.annotations`` | annotations          |                      |
+----------------------+----------------------+----------------------+
| ``ingress.hosts``    | a list of routable   | ``[]``               |
|                      | hostnames for        |                      |
|                      | host-based routing   |                      |
|                      | of traffic to the    |                      |
|                      | WebSocket service    |                      |
+----------------------+----------------------+----------------------+
| ``ingress.paths``    | a list of paths for  | ``/``                |
|                      | path-based routing   |                      |
|                      | of traffic to the    |                      |
|                      | WebSocket service    |                      |
+----------------------+----------------------+----------------------+
| ``ingress.tls``      | a list of TLS        | ``[]``               |
|                      | ingress              |                      |
|                      | configurations for   |                      |
|                      | securing the         |                      |
|                      | WebSocket ingress    |                      |
+----------------------+----------------------+----------------------+
| ``nodeSelector``     | node labels for pod  | ``{}``               |
|                      | assignment           |                      |
+----------------------+----------------------+----------------------+
| ``persistent         | data Persistent      | ``[ReadWriteOnce]``  |
| Volume.accessModes`` | Volume access modes  |                      |
+----------------------+----------------------+----------------------+
| ``persistent         | annotations for      | ``{}``               |
| Volume.annotations`` | Persistent Volume    |                      |
|                      | Claim                |                      |
+----------------------+----------------------+----------------------+
| ``persis             | if true, create a    | ``true``             |
| tentVolume.enabled`` | Persistent Volume    |                      |
|                      | Claim                |                      |
+----------------------+----------------------+----------------------+
| ``per                | data Persistent      | ``5Gi``              |
| sistentVolume.size`` | Volume size          |                      |
+----------------------+----------------------+----------------------+
| ``persistentV        | data Persistent      | ``unset``            |
| olume.storageClass`` | Volume Storage Class |                      |
+----------------------+----------------------+----------------------+
| `                    | Additional           | ``[]``               |
| `extraVolumeMounts`` | volumeMounts to the  |                      |
|                      | pod                  |                      |
+----------------------+----------------------+----------------------+
| ``extraVolumes``     | Additional volumes   | ``[]``               |
|                      | to the pod           |                      |
+----------------------+----------------------+----------------------+
| ``secretMounts``     | mounts a secret as a | ``[]``               |
|                      | file inside the      |                      |
|                      | statefulset. Useful  |                      |
|                      | for mounting         |                      |
|                      | certificates and     |                      |
|                      | other secrets.       |                      |
+----------------------+----------------------+----------------------+
| ``podAntiAffinity``  | pod anti affinity,   | ``soft``             |
|                      | ``soft`` for trying  |                      |
|                      | not to run pods on   |                      |
|                      | the same nodes,      |                      |
|                      | ``hard`` to force    |                      |
|                      | kubernetes not to    |                      |
|                      | run 2 pods on the    |                      |
|                      | same node            |                      |
+----------------------+----------------------+----------------------+
| ``rbac.create``      | if true, create &    | ``true``             |
|                      | use RBAC resources   |                      |
+----------------------+----------------------+----------------------+
| ``rbac.ser           | if true, create a    | ``true``             |
| viceAccount.create`` | serviceAccount       |                      |
+----------------------+----------------------+----------------------+
| ``rbac.s             | name of the service  | ``{{ include "vern   |
| erviceAccount.name`` | account to use or    | emq.fullname" . }}`` |
|                      | create               |                      |
+----------------------+----------------------+----------------------+
| ``replicaCount``     | desired number of    | ``1``                |
|                      | nodes                |                      |
+----------------------+----------------------+----------------------+
| ``resources``        | resource requests    | ``{}``               |
|                      | and limits (YAML)    |                      |
+----------------------+----------------------+----------------------+
| ``securityContext``  | securityContext for  | ``{}``               |
|                      | containers in pod    |                      |
+----------------------+----------------------+----------------------+
| ``s                  | service annotations  | ``{}``               |
| ervice.annotations`` |                      |                      |
+----------------------+----------------------+----------------------+
| `                    | custom cluster IP    | ``none``             |
| `service.clusterIP`` | when                 |                      |
|                      | ``service.type`` is  |                      |
|                      | ``ClusterIP``        |                      |
+----------------------+----------------------+----------------------+
| ``s                  | optional service     | ``none``             |
| ervice.externalIPs`` | external IPs         |                      |
+----------------------+----------------------+----------------------+
| ``service.labels``   | additional service   | ``{}``               |
|                      | labels               |                      |
+----------------------+----------------------+----------------------+
| ``serv               | optional load        | ``none``             |
| ice.loadBalancerIP`` | balancer IP when     |                      |
|                      | ``service.type`` is  |                      |
|                      | ``LoadBalancer``     |                      |
+----------------------+----------------------+----------------------+
| ``service.loadBa     | optional load        | ``none``             |
| lancerSourceRanges`` | balancer source      |                      |
|                      | ranges when          |                      |
|                      | ``service.type`` is  |                      |
|                      | ``LoadBalancer``     |                      |
+----------------------+----------------------+----------------------+
| ``service.ext        | set this to          | ``unset``            |
| ernalTrafficPolicy`` | ``Local`` to         |                      |
|                      | preserve client      |                      |
|                      | source IPs and       |                      |
|                      | prevent additional   |                      |
|                      | hops between K8s     |                      |
|                      | nodes if the service |                      |
|                      | type is              |                      |
|                      | ``LoadBalancer`` or  |                      |
|                      | ``NodePort``         |                      |
+----------------------+----------------------+----------------------+
| ``servi              | service session      | ``none``             |
| ce.sessionAffinity`` | affinity             |                      |
+----------------------+----------------------+----------------------+
| ``service.ses        | service session      | ``none``             |
| sionAffinityConfig`` | affinity config      |                      |
+----------------------+----------------------+----------------------+
| ``se                 | whether to expose    | ``true``             |
| rvice.mqtt.enabled`` | MQTT port            |                      |
+----------------------+----------------------+----------------------+
| ``ser                | the MQTT port        | ``1883``             |
| vice.mqtt.nodePort`` | exposed by the node  |                      |
|                      | when                 |                      |
|                      | ``service.type`` is  |                      |
|                      | ``NodePort``         |                      |
+----------------------+----------------------+----------------------+
| `                    | the MQTT port        | ``1883``             |
| `service.mqtt.port`` | exposed by the       |                      |
|                      | service              |                      |
+----------------------+----------------------+----------------------+
| ``ser                | whether to expose    | ``false``            |
| vice.mqtts.enabled`` | MQTTS port           |                      |
+----------------------+----------------------+----------------------+
| ``serv               | the MQTTS port       | ``8883``             |
| ice.mqtts.nodePort`` | exposed by the node  |                      |
|                      | when                 |                      |
|                      | ``service.type`` is  |                      |
|                      | ``NodePort``         |                      |
+----------------------+----------------------+----------------------+
| ``                   | the MQTTS port       | ``8883``             |
| service.mqtts.port`` | exposed by the       |                      |
|                      | service              |                      |
+----------------------+----------------------+----------------------+
| ``service.type``     | type of service to   | ``ClusterIP``        |
|                      | create               |                      |
+----------------------+----------------------+----------------------+
| ``                   | whether to expose    | ``false``            |
| service.ws.enabled`` | WebSocket port       |                      |
+----------------------+----------------------+----------------------+
| ``s                  | the WebSocket port   | ``8080``             |
| ervice.ws.nodePort`` | exposed by the node  |                      |
|                      | when                 |                      |
|                      | ``service.type`` is  |                      |
|                      | ``NodePort``         |                      |
+----------------------+----------------------+----------------------+
| ``service.ws.port``  | the WebSocket port   | ``8080``             |
|                      | exposed by the       |                      |
|                      | service              |                      |
+----------------------+----------------------+----------------------+
| ``s                  | whether to expose    | ``false``            |
| ervice.wss.enabled`` | secure WebSocket     |                      |
|                      | port                 |                      |
+----------------------+----------------------+----------------------+
| ``se                 | the secure WebSocket | ``8443``             |
| rvice.wss.nodePort`` | port exposed by the  |                      |
|                      | node when            |                      |
|                      | ``service.type`` is  |                      |
|                      | ``NodePort``         |                      |
+----------------------+----------------------+----------------------+
| ``service.wss.port`` | the secure WebSocket | ``8443``             |
|                      | port exposed by the  |                      |
|                      | service              |                      |
+----------------------+----------------------+----------------------+
| ``state              | additional           | ``{}``               |
| fulset.annotations`` | annotations to the   |                      |
|                      | StatefulSet          |                      |
+----------------------+----------------------+----------------------+
| ``                   | additional labels on | ``{}``               |
| statefulset.labels`` | the StatefulSet      |                      |
+----------------------+----------------------+----------------------+
| ``stateful           | additional pod       | ``{}``               |
| set.podAnnotations`` | annotations          |                      |
+----------------------+----------------------+----------------------+
| ``statefulset.p      | start and stop pods  | ``OrderedReady``     |
| odManagementPolicy`` | in Parallel or       |                      |
|                      | OrderedReady         |                      |
|                      | (one-by-one.)        |                      |
|                      | **Note** - Cannot    |                      |
|                      | change after first   |                      |
|                      | release.             |                      |
+----------------------+----------------------+----------------------+
| ``sta                | configure how much   | ``60``               |
| tefulset.termination | time VerneMQ takes   |                      |
| GracePeriodSeconds`` | to move offline      |                      |
|                      | queues to other      |                      |
|                      | nodes                |                      |
+----------------------+----------------------+----------------------+
| ``stateful           | Statefulset          | ``RollingUpdate``    |
| set.updateStrategy`` | updateStrategy       |                      |
+----------------------+----------------------+----------------------+
| ``sta                | Statefulset          | ``{}``               |
| tefulset.lifecycle`` | lifecycle hooks      |                      |
+----------------------+----------------------+----------------------+
| ``ser                | whether to create a  | ``false``            |
| viceMonitor.create`` | ServiceMonitor for   |                      |
|                      | Prometheus Operator  |                      |
+----------------------+----------------------+----------------------+
| ``ser                | whether to add more  | ``{}``               |
| viceMonitor.labels`` | labels to            |                      |
|                      | ServiceMonitor for   |                      |
|                      | Prometheus Operator  |                      |
+----------------------+----------------------+----------------------+
| ``pdb.enabled``      | whether to create a  | ``false``            |
|                      | Pod Disruption       |                      |
|                      | Budget               |                      |
+----------------------+----------------------+----------------------+
| ``pdb.minAvailable`` | PDB (min available)  | ``1``                |
|                      | for the cluster      |                      |
+----------------------+----------------------+----------------------+
|                      | PDB (max             | ``nil``              |
|``pdb.maxUnavailable``| unavailable) for the |                      |
|                      | cluster              |                      |
+----------------------+----------------------+----------------------+

***************
Developer guide
***************


***************************
Version control and release
***************************

***************
License
***************

********************
Notice(dependencies)
********************
