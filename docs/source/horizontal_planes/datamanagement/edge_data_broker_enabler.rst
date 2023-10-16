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
docker image.

- Kubernetes 1.16+
- Helm 3+

***************
Installation
***************

Edge Data Broker (EDB) Enabler Installation
-------------------------------------------

**To install the chart with the release name edbe:**

Clone the repository to your machine.

Install Edge Data Broker Enabler.

.. code-block:: cmd

  helm install edbe ./edge-data-broker
  
The command deploys EDB on the Kubernetes cluster in the default configuration.

**Note**: ``kostasiccs/vernemq`` image is suitable for ARM architectures (Assist-IoT's GWEN, Raspberry Pi, etc.) and is the defaul image used in Edbe's helm chart. For other architectures use ``vernemq/vernemq`` official image and accept the VerneMQ EULA by appending the following in the additionalEnv.

.. code-block::

  - name: DOCKER_VERNEMQ_ACCEPT_EULA
    value: "yes"

To check if the installation was successful run:

.. code-block:: cmd

  kubectl get pods

The result should show something like:

.. code-block::

  NAME                         READY   STATUS    RESTARTS   AGE
  edbe-0                       1/1     Running   0          174m
  edbe-1                       1/1     Running   0          172m
  fr-script-66f6f8688d-7x6ts   1/1     Running   0          174m
  
**To make the two VerneMQ nodes (edbe-0, edbe-1) run as a singular cluster, you'll need to join one node to the other like this:**

- Connect to a shell of a running container within Kubernetes pod (edbe-0 or edbe-1).

.. code-block:: cmd

  kubectl exec -it edbe-0 -- /bin/bash
  
- Check the cluster state (you should see a 1 node cluster):

.. code-block:: cmd

  vmq-admin cluster show
  
The result should show something like:

.. code-block::

  +--------------------------------------------------------+---------+
  | Node                                                   | Running |
  +--------------------------------------------------------+---------+
  | VerneMQ@edbe-0.edbe-headless.default.svc.cluster.local | true    |
  +--------------------------------------------------------+---------+

- Join one node to the other with:

.. code-block:: cmd

  vmq-admin cluster join discovery-node=<OtherClusterNode>
  
- Check the cluster state (you should see a 2 node cluster):

.. code-block:: cmd

  vmq-admin cluster show
  
The result should show something like:

.. code-block::

  +--------------------------------------------------------+---------+
  | Node                                                   | Running |
  +--------------------------------------------------------+---------+
  | VerneMQ@edbe-0.edbe-headless.default.svc.cluster.local | true    |
  +--------------------------------------------------------+---------+
  | VerneMQ@edbe-1.edbe-headless.default.svc.cluster.local | true    |
  +--------------------------------------------------------+---------+
  
**To make an MQTT Bridge connection between two different VermeMQ clusters before the installation append in one of the cluster's values.yaml file the following additionaEnv:**

.. code-block::

  - name: DOCKER_VERNEMQ_PLUGINS__VMQ_BRIDGE
    value: "on"
  - name: DOCKER_VERNEMQ_VMQ_BRIDGE__TCP__BR0
    value: "10.43.0.1:31883"
  - name: DOCKER_VERNEMQ_VMQ_BRIDGE__TCP__BR0__TOPIC__1
    value: "* in"
  - name: DOCKER_VERNEMQ_VMQ_BRIDGE__TCP__BR0__MAX_OUTGOING_BUFFERED_MESSAGES
    value: "100"
    
**Note**:  With the above configuration we allow to only import messages (all of them, '*'="#" wildcard) from a remote broker with address 10.43.0.1 and port 31883 and store up to 100 messages to our buffer.

For more info refer to vernemq official `Documentation page <https://docs.vernemq.com/configuring-vernemq/bridge>`_.

- Connect to a shell of a running container within Kubernetes pod.

.. code-block:: cmd

  kubectl exec -it edbe-0 -- /bin/bash

- Check the bridges state:

.. code-block:: cmd
  
  vmq-admin bridge show
  
The result should show something like:

.. code-block::

  +------+-----------------+-------------+------------+---------------------+--------------------------+
  | name | endpoint        | buffer size | buffer max | buffer dropped msgs | MQTT process mailbox len |
  +------+-----------------+-------------+------------+---------------------+--------------------------+
  | br0  | 10.43.0.1:31883 | 0           | 100        | 0                   | 0                        |
  +------+-----------------+-------------+------------+---------------------+--------------------------+
  
**To monitor Edge Data Broker Enabler, type to your browser:**

``http://<IP>:30888/status`` to get EDBE's status page.

``http://<IP>:30888/metrics`` to get EDBE's metrics page made for Performance and Usage Diagnosis Enabler's consumption.

**To access Filtering and Ruling json file:**

Port forward fr-script's pod to port 8000:

.. code-block:: cmd

  kubectl port-forward fr-script-66f6f8688d-7x6ts 8000
  
``GET`` or ``POST`` Filtering and Ruling json file by Postman, CURL, etc, with ``http://<ip>:8000/``.

To see fr-script's logs:

.. code-block:: cmd

  kubectl logs fr-script-66f6f8688d-7x6ts

*********************
Configuration options
*********************

The following table lists the configurable parameters of the chart and their default values.

.. list-table::
   :widths: 25 50 20
   :header-rows: 1
   
   * - Parameter
     - Description
     - Default
   * - additionalEnv
     - additional environment variables
     - see values.yaml
   * - envFrom
     - additional envFrom configmaps or secrets
     - see values.yaml
   * - image.pullPolicy
     - container image pull policy
     - ``IfNotPresent``
   * - image.repository
     - container image repository
     - ``kostasiccs/vernemq``
   * - image.tag
     - container image tag
     - the current versions (e.g. `1.12.3`)
   * - ingress.enabled
     - whether to enable an ingress object to route to the WebSocket service. Requires an ingress controller and the WebSocket service to be enabled.
     - ``false``
   * - ingress.labels
     - additional ingress labels
     - ``{}``
   * - ingress.annotations
     - additional service annotations
     - ``{}``
   * - ingress.hosts
     - a list of routable hostnames for host-based routing of traffic to the WebSocket service
     - ``[]``
   * - ingress.paths
     - a list of paths for path-based routing of traffic to the WebSocket service
     - ``/``
   * - ingress.tls
     - a list of TLS ingress configurations for securing the WebSocket ingress
     - ``[]``
   * - nodeSelector
     - node labels for pod assignment
     - ``{}``
   * - persistentVolume.accessModes
     - data Persistent Volume access modes
     - ``[ReadWriteOnce]``
   * - persistentVolume.annotations
     - annotations for Persistent Volume Claim
     - ``{}``
   * - persistentVolume.enabled
     - if true, create a Persistent Volume Claim
     - ``true``
   * - persistentVolume.size
     - data Persistent Volume size
     - ``5Gi``
   * - persistentVolume.storageClass
     - data Persistent Volume Storage Class
     - ``unset``
   * - extraVolumeMounts
     - Additional volumeMounts to the pod
     - ``[]``
   * - extraVolumes
     - Additional volumes to the pod
     - ``[]``
   * - secretMounts
     - mounts a secret as a file inside the statefulset. Useful for mounting certificates and other secrets
     - ``[]``
   * - podAntiAffinity
     - pod anti affinity, `soft` for trying not to run pods on the same nodes, `hard` to force kubernetes not to run 2 pods on the same node
     - ``soft``
   * - rbac.create
     - if true, create & use RBAC resources
     - ``true``
   * - rbac.serviceAccount.create
     - if true, create a serviceAccount
     - ``true``
   * - rbac.serviceAccount.name
     - name of the service account to use or create
     - ``{{ include "vernemq.fullname" . }}``
   * - replicaCount
     - desired number of nodes
     - ``1``
   * - resources
     - resource requests and limits (YAML)
     - ``{}``
   * - securityContext
     - securityContext for containers in pod
     - ``{}``
   * - service.annotations
     - service annotations
     - ``{}``
   * - service.clusterIP
     - custom cluster IP when `service.type` is `ClusterIP`
     - ``none``
   * - service.externalIPs
     - optional service external IPs
     - ``none``
   * - service.labels
     - additional service labels
     - ``{}``
   * - service.loadBalancerIP
     - optional load balancer IP when `service.type` is `LoadBalancer`
     - ``none``
   * - service.loadBalancerSourceRanges
     - optional load balancer source ranges when `service.type` is `LoadBalancer`
     - ``none``
   * - service.externalTrafficPolicy
     - set this to `Local` to preserve client source IPs and prevent additional hops between K8s nodes if the service type is `LoadBalancer` or `NodePort`
     - ``unset``
   * - service.sessionAffinity
     - service session affinity
     - ``none``
   * - service.sessionAffinityConfig
     - service session affinity config
     - ``none``
   * - service.mqtt.enabled
     - whether to expose MQTT port
     - ``true``
   * - service.mqtt.nodePort
     - the MQTT port exposed by the node when `service.type` is `NodePort`
     - ``1883``
   * - service.mqtt.port
     - the MQTT port exposed by the service
     - ``1883``
   * - service.mqtts.enabled
     - whether to expose MQTTS port
     - ``false``
   * - service.mqtts.nodePort
     - the MQTTS port exposed by the node when `service.type` is `NodePort`
     - ``8883``
   * - service.mqtts.port
     - the MQTTS port exposed by the service
     - ``8883``
   * - service.type
     - type of service to create
     - ``ClusterIP``
   * - service.ws.enabled
     - whether to expose WebSocket port
     - ``false``
   * - service.ws.nodePort
     - the WebSocket port exposed by the node when `service.type` is `NodePort`
     - ``8080``
   * - service.ws.port
     - the WebSocket port exposed by the service
     - ``8080``
   * - service.wss.enabled
     - whether to expose secure WebSocket port
     - ``false``
   * - service.wss.nodePort
     - the secure WebSocket port exposed by the node when `service.type` is `NodePort`
     - ``8443``
   * - service.wss.port
     - the secure WebSocket port exposed by the service
     - ``8443``
   * - statefulset.annotations
     - additional annotations to the StatefulSet
     - ``{}``
   * - statefulset.labels
     - additional labels on the StatefulSet
     - ``{}``
   * - statefulset.podAnnotations
     - additional pod annotations
     - ``{}``
   * - statefulset.podManagementPolicy
     - start and stop pods in Parallel or OrderedReady (one-by-one.)  **Note** - Cannot change after first release.
     - ``OrderedReady``
   * - statefulset.terminationGracePeriodSeconds
     - configure how much time VerneMQ takes to move offline queues to other nodes
     - ``60``
   * - statefulset.updateStrategy
     - Statefulset updateStrategy
     - ``RollingUpdate``
   * - statefulset.lifecycle
     - Statefulset lifecycle hooks
     - ``{}``
   * - serviceMonitor.create
     - whether to create a ServiceMonitor for Prometheus Operator
     - ``false``
   * - serviceMonitor.labels
     - whether to add more labels to ServiceMonitor for Prometheus Operator
     - ``{}``
   * - pdb.enabled
     - whether to create a Pod Disruption Budget
     - ``false``
   * - pdb.minAvailable
     - PDB (min available) for the cluster
     - ``1``
   * - pdb.maxUnavailable
     - PDB (max unavailable) for the cluster
     - ``nil``
   * - certificates.cert
     - String (not base64 encoded) containing the listener certificate in PEM format
     - ``nil``
   * - certificates.key
     - String (not base64 encoded) containing the listener private key in PEM format
     - ``nil``
   * - certificates.ca
     - String (not base64 encoded) containing the CA certificate for validating client certs    
     - ``nil``
   * - certificates.secret.labels
     - additional labels for the created secret containing certificates and keys
     - ``nil``
   * - certificates.secret.annotations
     - additional labels for the created secret containing certificates and keys
     - ``nil``
   * - acl.enabled
     - whether acls should be applied
     - ``false``
   * - acl.content
     - content of the acl file
     - ``topic #``
   * - acl.labels
     - additional labels on the acl configmap
     - ``{}``
   * - acl.annotations
     - additional annotations on the acl configmap
     - ``{``


****************
Developer guide
****************

FR-Script Documentation
-----------------------

In order for the fr_script to operate the user should provide relevant filters and rules corresponding to different use cases (scenarios). 

The filters and rules should be provided in json format. GET, POST, PATCH, DELETE HTTP Methods can be used to fetch, post, update and delete json objects via an API respectively. The APIs can get accessed on port 30008. Use endpoint ``/docs#/`` for accessing swgger UI.

.. image:: https://user-images.githubusercontent.com/100563908/222690700-13739082-a840-4431-90c9-2373e0fa9fc1.PNG

The _json_ consists of two parts.

.. code::

  {
	  “filters”: [],
	  “rules”: []
  }

Witch both contains an array of objects.

Filters
-------

For the filtering, the MQTT **topic** which the user wants to filter is required. It consists of one or more topic levels and can contain ``“#”`` and ``“+”`` wildcard as well.

A **subtopic** is also required. It will get appended to the topic that is being filtered and create the new topic in which the filtered messages will be published. This can also consist one or more topic levels.

After setting the topic and subtopic of the filter, **statements** also need to get defined. Statements is an array of objects. Every statement consists of two components, a **condition** and a **new_payload**.
A condition takes as value the same thing that an if statement expression would. Variables, values, comparison operators, logical operators and parenthesis, to set the priority of the operations. **NOTE**: Use spaces between every instance of the condition.

The variables should exist as key values in the json message sent to the topic that is being filtered. In the json file with the filters and rules that the user provides, those same variables should start with the ``$`` sign, followed by their name. If the filtered json message has nested objects, the parent variable comes after the ``$`` sign, followed by a dot ``.`` and then the child variable. **Example**: ``$parent.child``

The **new_payload** takes as value a ``string`` value or ``""``. The new_payload’s value is the new message that will be published at the newlly set filtered topic. If the new_payload’s value is ``""`` and the statements condition is met, the initial message of the filtered topic will be sent. 

**Example**

Let’s say we have a number of houses in a smart city. There are sensors installed inside and outside of those houses that generate data like the json below.

``{"h_id":1,"inside":{"temperature":35,"humidity":60},"temperature":43,"wind_speed":34}``
  
The sensors of every house publish their data in a topic like ``house/1``, ``house/2``, etc.

The team that inspects and monitors the smart city wants to receive the sensor’s data only when those exceed some threshold and not all of them, so they subscribe on the topic ``house/+/alert/`` (``“+”`` is a single-level wildcard that matches any name for a specific topic level.) and use the json below to set the rules for the filtering of the data being published on 
``house/#``.

.. code::

  {
      "filters": [
          {
              "topic": "house/#",
              "subtopic": "alert/",
              "statements": [
                  {
                      "condition": "( $inside.temperature < 20 and $inside.humidity >= 60 ) or $temperature < 5",
                      "new_payload": ""
                  },
                  {
                      "condition": "$inside.temperature >= 45 and $inside.humidity <= 15",
                      "new_payload": "fire_danger"
                  }
              ]
          }
      ],
      "rules": []
  }

The messages below published by the sensors of houses 1,2 and 3 in topics ``house/1``, ``house/2`` and ``house/3`` respectively.

``{"h_id":1,"inside":{"temperature":50,"humidity":6},"temperature":8,"wind_speed":34}``

``{"h_id":2,"inside":{"temperature":15,"humidity":60},"temperature":8,"wind_speed":34}``

``{"h_id":3,"inside":{"temperature":22,"humidity":55},"temperature":8,"wind_speed":35}``
  
And the monitoring team’s client that was subscribed to the topic ``house/+/alert/`` got the messages:

``house/1/alert/--> b'fire_danger'``

``house/2/alert/--> b'{"h_id":2,"inside":{"temperature":15,"humidity":60},"temperature":8,"wind_speed":34}'``
  
Rules
-----

In the rules part of fr_script, every rule consists of two parts.

.. code::

  {
    “filters”: [],
    “rules”: [
      “statements”: [],
      “logic”: []
      ]
  }
  
**statements** and **logic** witch both contains an array of objects.

The **statements** are situated very similar to the filters.
Every statement consists of the MQTT **topic** that the user wants to apply rules against, the **condition** which work exactly like the conditions in filtering, an **id** unique for every statement and the **payload type** of the messages’ fields sent to the above defined topic and are used as variables in our condition. Those can be ``int``, ``float``, ``str``, ``bool``.

Every instance in logic array consist of the logical **operations** which constitute the essence of the ruling part of the script, the newly created topic **new_topic** and the **payload** that would be published in it only if the logical operations return true.

**Example**

Let’s say we are managers in a mine. We have sensors inside the mine monitoring its environment as well as biometric sensors on every miner. The sensors monitoring mine’s environment produces messages like the json below:

``{“temperature”: 25, “humidity”: 90}``
  
and publish them in ``mine/environment`` topic.

The miners’ biometric sensors produce messages like:

``{“m_id”:1, “body-temperature”: 36.6, “heart-rate”: 80}``
  
And publish their data in a topic like ``miner/1``, ``miner/2``, etc.

So as managers we want to apply the following rules to monitor the miners’ wellbeing.

- If miner’s heart rate is between 100-120 and the mine’s temperature is above 35 or the humidity is above 85 the miner should rest.

- If miner’s body temperature is above 38 degrees and the mine’s temperature is above 30 the miner should leave.

- If miner’s heart rate is 0 the miner is dead.

The fr_script should be as follows:

.. code::

  {
    “filters”: [],
    “rules”: [
      {
              "statements": [
                  {   
                      "id": 1,
                      "topic": "miner/#",
                      "payload_type": "float",
                      "condition": "$heart-rate >= 100 and $heart-rate <= 120"
                  },
                  {
                      "id": 2,
                      "topic": "mine/environment",
                      "payload_type": "int",
                      "condition": "$temperature > 35 or $humidity > 85"
                  }
              ],
              "logic": [
                  {
                      "operations": "( $1 ) and ( $2 )",
                      "new_topic": "action/rest",
                      "new_payload": ""
                  }
              ]
          },
          {
              "statements": [
                  {   
                      "id": 3,
                      "topic": "miner/#",
                      "payload_type": "float",
                      "condition": "$body-temperature > 38"
                  },
                  {
                      "id": 4,
                      "topic": "mine/environment",
                      "payload_type": "int",
                      "condition": "$temperature > 30"
                  }
              ],
              "logic": [
                  {
                      "operations": "$3 and $4",
                      "new_topic": "action/leave",
                      "new_payload": ""
                  }
              ]
          },
          {
              "statements": [
                  {   
                      "id": 5,
                      "topic": "miner/#",
                      "payload_type": "float",
                      "condition": "$heart-rate == 0"
                  }
              ],
              "logic": [
                  {
                      "operations": "$5",
                      "new_topic": "action/dead",
                      "new_payload": ""
                  }
              ]
          }
      ]
  }

The messages below published by the sensors on the workers’ 1 and workers’ 2 equipment as well as sensors on the mine itself. Our topics are ``miner/1``, ``miner/2`` and ``mine/environment`` respectively and the messages are published in the order shown bellow.

``{"m_id":1, "body-temperature": 36.6, "heart-rate": 105}``

to topic ``miner/1``

``{"m_id":2, "body-temperature": 38.6, "heart-rate": 75}``

to topic ``miner/2``

``{"temperature": 35, "humidity": 90}``

to topic ``mine/environment``

``{"m_id":1, "body-temperature": 16.6, "heart-rate": 0}``
to topic ``miner/1``

The monitoring team’s client that was subscribed to the topic ``!action`` will get the messages:

``!action/rest--> "{'miner/1': {'m_id': 1, 'body-temperature': 39.6, 'heart-rate': 105}, 'mine/environment': {'temperature': 35, 'humidity': 90}}"``

``!action/leave--> "{'miner/2': {'m_id': 2, 'body-temperature': 38.6, 'heart-rate': 75}, 'mine/environment': {'temperature': 35, 'humidity': 90}}"``

*(Just after the message sent to topic mine/environment)*

``!action/dead--> "{'miner/1': {'m_id': 1, 'body-temperature': 16.6, 'heart-rate': 0}}"``

**NOTE**: If the messages were sent in a different order like bellow: 

``{"m_id":1, "body-temperature": 36.6, "heart-rate": 105}``

to topic ``miner/1``

``{"temperature": 35, "humidity": 90}``

to topic ``mine/environment``

``{"m_id":2, "body-temperature": 38.6, "heart-rate": 75}``

to topic ``miner/2``

``{"m_id":1, "body-temperature": 16.6, "heart-rate": 0}``

to topic ``miner/1``

And the monitoring team’s client that was subscribed to the topic ``!action`` will get the messages:

``!action/rest--> "{'miner/1': {'m_id': 1, 'body-temperature': 39.6, 'heart-rate': 105}, 'mine/environment': {'temperature': 35, 'humidity': 90}}"``

``!action/dead--> "{'miner/1': {'m_id': 1, 'body-temperature': 16.6, 'heart-rate': 0}}"``

This happens because when a logical operation comes True in fr_script’s rules and a new message is sent, the array holding the messages previously sent to fr_script, empty itself.

Lastly as we can see when ``“new_payload”: “”`` the new payload generated by fr_script is a json with the topic(s) used in the logic’s operations and their payload(s). Topics created by fr_script will always start with ``“!”`` as shown above.

****************************
Version control and release
****************************
VerneMQ v1.12.3

FR_Script v1.0

****************
License
****************
Will be determined after the release of the enabler.
