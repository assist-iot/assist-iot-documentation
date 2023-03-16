.. _Monitoring and Notifying enabler:

################################
Monitoring and Notifying enabler
################################

.. contents::
  :local:
  :depth: 1

***************
Introduction
***************
This enabler could be viewed as a general purpose by representing it as a combination of high-level monitoring module (which would allow to monitor devices, logs, etc.) and notifying module that could send custom messages to predefined system components.

***************
Features
***************
The monitoring and notifying enabler has the following functionalities:

- Monitor the uninterrupted functionality of edge devices
- Create a notification when an unexpexted incident occurs
- Common interfaces for quering log-data and notifications

*********************
Place in architecture
*********************

The monitoring and notifying enabler is part of the vertical plane enablers Self-*. It is directly connected to the Edge Data Broker Enabler by subscribing to its topics.


***************
User guide
***************

**NOTE**: This is a continuation of the installation steps. Please proceed with the installation first and then continue with the current section.

======
Testing the deployment:
======

In order to test the deployment we are going to create a topic and test if producers/consumers can exchange messages both inside the k8s cluster and from outside as well.

**Create a topic**

- Create a topic named mytopic using the commands below. Replace the KAFKA_SERVICE_NAME placeholder with the one mentioned above.

.. code:: bash

  export POD_NAME=$(kubectl get pods --namespace default -l "app.kubernetes.io/name=kafka,app.kubernetes.io/instance=mykafka,app.kubernetes.io/component=kafka" -o jsonpath="{.items[0].metadata.name}")

  kubectl --namespace default exec -it $POD_NAME -- kafka-topics.sh --create --bootstrap-server <KAFKA_SERVICE_NAME>:9092 --replication-factor 1 --partitions 1 --topic mytopic


**Create a producer/consumer inside the cluster**

- Start a Kafka message **consumer**. This consumer will connect to the cluster and retrieve and display messages as they are published to the mytopic topic. Replace the KAFKA_SERVICE_NAME placeholder with the one mentioned above. (If you are in the same terminal you created the topic then ignore the first line).

.. code:: bash
  
  export POD_NAME=$(kubectl get pods --namespace default -l "app.kubernetes.io/name=kafka,app.kubernetes.io/instance=mykafka,app.kubernetes.io/component=kafka" -o jsonpath="{.items[0].metadata.name}")

  kubectl --namespace default exec -it $POD_NAME -- kafka-console-consumer.sh --bootstrap-server <KAFKA_SERVICE_NAME>:9092 --topic <TOPIC_NAME> --consumer.config /opt/bitnami/kafka/config/consumer.properties

Using a different console, start a Kafka message producer and produce some messages by running the command below and then entering some messages, each on a separate line. Replace the KAFKA_SERVICE_NAME placeholder with the one mentioned above.

.. code:: bash

  export POD_NAME=$(kubectl get pods --namespace default -l "app.kubernetes.io/name=kafka,app.kubernetes.io/instance=mykafka,app.kubernetes.io/component=kafka" -o jsonpath="{.items[0].metadata.name}")

  kubectl --namespace default exec -it $POD_NAME -- kafka-console-producer.sh --bootstrap-server <KAFKA_SERVICE_NAME>:9092 --topic <TOPIC_NAME> --producer.config /opt/bitnami/kafka/config/producer.properties

======
Run the custom producer outside the cluster and the custom consumer inside the cluster
======

Assuming we have an IoT or Edge device outside the k8s cluster we create a virtual temperature generator with the following assumptions:

- The device generates temperatures between (1, 30) degrees Celsius in fixed 1sec time intervals (normal distribution).
- If the temperature published by the producer exceeds 20°C, the consumer produces a warning that the temperature is high.
- If the temperature published by the producer exceeds 27°C, the producer stops for the sake of not looping forever.

Assuming that we can create the consumer in the form of a "dashboard" that exists in the cluster, so we can constantly watch the temperatures generated, as well as the warnings, we run the following commands:

.. code:: bash
  cd consumer

  helm install myconsumer .

In order to be able to watch what the logs of the consumer we run in the terminal:

.. code:: bash
  
  kubectl get pods

  kubectl logs -f <POD_NAME>

Where <POD_NAME> is the name of the pod created. Copy it from the first command.

------------

In order to create the custom temperature producer outside the cluster we need to have java installed. In a new terminal we type:

.. code:: bash

  sudo apt install default-jdk

Verify the installation:

.. code:: bash

  java -version

Then we run:

.. code:: bash

  java -jar <PATH_TO_FILE>/TempGenK8s.jar

***************
Prerequisites
***************

- Linux
- Docker
- kubectl
- Helm

============ ======================================================================================================================================================================================================================================================================== 
  Technology   Justification                                                                                                                                                                                                                                                           
============ ======================================================================================================================================================================================================================================================================== 
  **Kafka**        Kafka provides a standardized method to enable a diverse set of technologies to communicate and interact. It is used to build real-time streaming data pipelines and real-time streaming applications which will be very useful in the IoT environment of the project.  
  **Java 8**       Java is a low complexity programming language and since Kafka is written in Java, it is one of the best choices for the enabler.                                                                                                                                        
  **MQTT**         MQTT is a lightweight publish/subscribe messaging protocol and it is widely used l in IoT solutions. Since Edge Data Broker Enabler will use this protocol, it is under consideration to be used for easier integration.                                                
============ ======================================================================================================================================================================================================================================================================== 


***************
Installation
***************

======
Installing the chart:
======

**Zookeeper**

.. code:: bash

  cd Zookeeper-Chart

  $ helm install myzookeeper . --set auth.enabled=false --set allowAnonymousLogin=true

- In your terminal you will see: Zookeeper can be accessed via port 2181 on the following DNS name from within your cluster:

.. code:: bash
  
  myzookeeper.default.svc.cluster.local
  
- And the above is your <ZOOKEEPER_SERVICE_NAME>

**Kafka**

.. code:: bash
  
  $cd Kafka-Chart

  $ helm install mykafka . --set externalZookeeper.servers=<ZOOKEPER_SERVICE_NAME>  \
  --set externalAccess.service.type=NodePort \
  --set externalAccess.service.nodePorts[0]=30910 \
  --set externalAccess.enabled=true \
  --set externalAccess.service.domain=<NODE_IP>

- In your terminal you will see: Kafka can be accessed via port 9092 on the following DNS name from within your cluster:

.. code:: bash
  
  mykafka-0.mykafka-headless.default.svc.cluster.local
  
- And the above is your <KAFKA_SERVICE_NAME>

*********************
Configuration options
*********************

Some basic configurations are listed below:

================== ========================================== ========================== 
 Variable           Description                                Example                   
================== ========================================== ========================== 
 BootstrapServers   Broker adress and port                     "localhost:9092       
 groupId            Group of devices the consumer belongs      "TemperatureSensors"    
 topic              Topic to subscribe                         "device1", "device2"  
 threshold          Threshold value to produce notifications   "20"                  
================== ========================================== ========================== 

Additional configurations can be found in the corresponding gitlab repository README.md.

***************
Developer guide
***************

The monitoring and notifying enabler is build on Apache Kafka, written in Java 8, using the maven repository infrastructure. The logs are stored in MongoDB.

***************************
Version control and release
***************************

Gitlab will be used as version control and release tool.

***************
License
***************

Licensing information will be provided after the release of the enabler.

********************
Notice(dependencies)
********************

Currently there are no dpendencies.
