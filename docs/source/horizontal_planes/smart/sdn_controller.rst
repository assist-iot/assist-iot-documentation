.. _SDN Controller:

##############
SDN Controller
##############

.. contents::
  :local:
  :depth: 1

***************
Introduction
***************
The SDN Controller is the key element of an SDN-enabled network, where the main functionalities are re-lated to network management, operation and maintenance, allowing topology management, network config-uration, network control and network operations, among other features. Two solutions are investigated based on open source implementation: µONOS and Tungsten.

***************
Features
***************
The SDN Controller is the software that takes over the responsibilities of the control plane from the hardware elements (switches mostly), including monitoring and management of packet flows. Although typically installed in a dedicated machine, its functionalities are intended to be provided following the ASSIST-IoT architecture based on enablers, either by adopting a distribution that matches it or by making the necessary adaptations to fulfil them. The main functionalities are related to network management, operation and maintenance, allowing topology management, network configuration, network control and network operations, among other features.

*********************
Place in architecture
*********************
SDN controller is part of Smart Network and Control plane. 
In this paradigm, the NFV Management and Orchestration (MANO) and the SDN Controller are the main elements, being the former in charge of instantiating and managing the lifecycle of Virtualised Network Functions (VNFs), and the latter in controlling the packet forwarding, among other networking aspects, based on specified policies. In the ASSIST-IoT ecosystem we aim at leveraging this paradigm, but adapted to an industrial ecosystem in which containers (and Kubernetes as container orchestrator) are expected to be prevalent, instead of leveraging (or at least minimising the necessity of) virtual machines.

***************
User guide
***************
Tungesten (https://tungsten.io/start/)
Tungsten Fabric provides a scalable virtual networking platform that works with a variety of virtual machine and container orchestrators, and can integrate with physical networking and compute infrastructure. Tungsten fabric uses networking industry standards such as BGP EVPN control plane and VXLAN overlays to seamlessly connect workloads in different orchestrator domains. E.g. Virtual machines managed by VMware vCenter and containers managed by Kubernetes.
Tungsten Fabric consists of two primary pieces of software:
--> Tungsten Fabric Controller– a set of software services that maintains a model of networks and network policies, typically running on several servers for high availability
--> Tungsten Fabric vRouter– installed in each host that runs workloads (virtual machines or containers), the vRouter performings packet forwarding and enforces network and security policies.
For detailed description go to:
https://tungstenfabric.github.io/website/Tungsten-Fabric-Architecture.html#key-features

uONOS (https://docs.onosproject.org/)
In the ONOS architecture (the one that will be leveraged for the project), one can distinguish core functional modules like Configuration, Control, Operation, Topology, and Northbound (NB) and Southbound (SB) API. Core subsystems are related to device, link, host, topology, etc. On the one hand, the usage of the SB API on the network level facilitates the integration of different vendors’ devices. On the other hand, the NB API is available for application developers. Being ONOS the  implementation that will be used for the project, it is possible to leverage REST API and also new generation of control and configuration interfaces like gNMI, gNOI, P4Runtime, NetDisco. The main functions envisioned in the project to be useful are the following: Device, Link, Host, Topology, Path, Flow , Flow Objectives, Group, Meter, Intent,, Application, Component Configuration.

µONOS is a code-name for the next generation architecture of ONOS - an open-source SDN control and configuration platform. The µONOS architecture is:
- Natively based on new generation of control and configuration interfaces and standards, e.g. P4/P4Runtime, gNMI/OpenConfig, gNOI
- Provides basis for zero-touch operations support
- Implemented in systems-level languages - primarily Go, some C/C++ as necessary
- Modular and based on established and efficient polyglot interface mechanism - gRPC
- Composed as a set of micro-services and deployable on cloud and data-center infrastructures - Kubernetes
- Highly available, dynamically scalable and high performance in terms of throughput (control/config ops/sec) and latency for implementing control-loops
- Available in ready-to-deploy form with a set of tools required for sustained operation, e.g. Docker images, Helm charts, monitoring and troubleshooting tools, etc.
The platform enables comprehensive set of network operations:
- Configuration, monitoring and maintenance of network devices for zero touch operation
- Configuration and programming of the forwarding plane structure (forwarding pipelines specified in P4)
- Validation of network topology and of forwarding plane behaviour
- Efficient collection of fine-grained network performance metrics (INT)

***************
Prerequisites
***************
TUNGSTEN:
1. A running Kubernetes cluster
    There are multiple options available to a user to install Kubernetes. The most simplest being kubeadm: https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/create-cluster-kubeadm/
Alternatively if you would like to install Tungsten Fabric and K8s cluster together, you can use Tungsten Fabric Ansible Deployer.
2. Docker version on all nodes should be >= 1.24

uONOS:
The individual components of µONOS may be deployed one at a time, or altogether through an overarching (unbrella) Helm chart, or some combination of both.
In all cases the prerequisites must be satisfied:
- Creation of a namespace
- deployment of Atomix controller(s) in the namespace.

The individual components in the umbrella chart are:
- onos-topo:
- onos-config:
- onos-cli:
- onos-gui:

The Helm chart provides resources for deploying the config service and accessing it over the network, both inside and outside the k8s cluster:
- Deployment - Provides a template for ONOS Config pods
- ConfigMap - Provides test configurations for the application
- Service - Exposes ONOS Config to other applications on the network
- Secret - Provides TLS certificates for end-to-end encryption
- Ingress - Optionally provides support for external load balancing

***************
Installation
***************

# ONOS 
---
## Required software

In order to run ONOS on a host is required to have installed:
 - **Kubernetes cluster** - a running cluster in order to provide master IP to installation yaml and spread scripts to nodes via DeamonSets,
 - **Docker** - in version **>= 1.24** on all nodes to set up Contrail containers.
 - this example installation was done using Kind (Kubernetes in Docker) on Ubuntu 18. 

Linux updates
```sh
apt-get update
apt-get upgrade
```

Docker installation

```sh
apt install docker.io
```

KinD instalation

Install GO
```sh 
wget https://dl.google.com/go/go1.14.2.linux-amd64.tar.gz
tar -xzf go1.14.2.linux-amd64.tar.gz
rm go1.14.2.linux-amd64.tar.gz
mv go /usr/local
```
Prepare profile file for GO
```sh 
cat << 'EOF' >> ~/.profile
export GOROOT=/usr/local/go
export GOPATH=~/go/kind
export PATH=$GOPATH/bin:$GOROOT/bin:$PATH
EOF
```
```sh 
source ~/.profile

GO111MODULE="on" go get sigs.k8s.io/kind@v0.8.0
```

Install Helm
```sh 
curl https://baltocdn.com/helm/signing.asc | gpg --dearmor | sudo tee /usr/share/keyrings/helm.gpg > /dev/null
apt-get install apt-transport-https --yes
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/helm.gpg] https://baltocdn.com/helm/stable/debian/ all main" | sudo tee /etc/apt/sources.list.d/helm-stable-debian.list
apt-get update
apt-get install helm
```

Installation Kubectl

```sh
snap install kubectl --classic
```


## Installation


Seccomp activation

For ONOS installation seccomp option -  computer security facility in the Linux kernel must be enabled

```sh
mkdir ./profiles
curl -L -o profiles/audit.json https://k8s.io/examples/pods/security/seccomp/profiles/audit.json
curl -L -o profiles/violation.json https://k8s.io/examples/pods/security/seccomp/profiles/violation.json
curl -L -o profiles/fine-grained.json https://k8s.io/examples/pods/security/seccomp/profiles/fine-grained.json
ls profiles
```
```sh
curl -L -O https://k8s.io/examples/pods/security/seccomp/kind.yaml
```




```sh
vi kind.yaml
```
For single node installation

```
apiVersion: kind.x-k8s.io/v1alpha4
kind: Cluster
nodes:
- role: control-plane
  extraMounts:
  - hostPath: "./profiles"
    containerPath: "/var/lib/kubelet/seccomp/profiles"
```

For High availability (HA) installation

```
apiVersion: kind.x-k8s.io/v1alpha4
kind: Cluster
nodes:
- role: control-plane
- role: worker
- role: worker
- role: worker
  extraMounts:
  - hostPath: "./profiles"
    containerPath: "/var/lib/kubelet/seccomp/profiles"
```

Create cluster

```sh
kind create cluster --name onos-classic --config=kind.yaml  --image=kindest/node:v1.23.6@sha256:b1fa224cc6c7ff32455e0b1fd9cbfd3d3bc87ecaa8fcb06961ed1afb3db0f9ae
```


Kubectl access

```sh
kind get kubeconfig --name=onos-classic > ~/.kube/kind

export KUBECONFIG=~/.kube/kind
```

Adding helm repo

```sh
helm repo add cord https://charts.opencord.org

helm repo add atomix https://charts.atomix.io

helm repo add onosproject https://charts.onosproject.org

helm repo update

helm search repo onos
```

Create namespace

```sh
kubectl create namespace micro-onos

helm install -n kube-system atomix-controller atomix/atomix-controller 

helm install -n kube-system atomix-raft-storage atomix/atomix-raft-storage

helm install -n kube-system onos-operator onosproject/onos-operator
```

ONOS Installation


For single node
```sh
helm -n micro-onos install onos-classic onosproject/onos-classic --set atomix.replicas=0 --set replicas=1
```

For HA version
```sh
helm -n micro-onos install onos-classic onosproject/onos-classic --set atomix.persistence.enabled=false
```
## Checking status

Installation verification

```sh
kubectl -n micro-onos get pods
```

Single pod

```sh
NAME                          READY   STATUS    RESTARTS      AGE
onos-classic-onos-classic-0   1/1     Running   3 (14m ago)   6d5h
```

HA
```sh
NAME                          READY   STATUS    RESTARTS        AGE
onos-classic-atomix-0         1/1     Running   4 (2m48s ago)   5h14m
onos-classic-atomix-1         1/1     Running   2 (3m51s ago)   5h14m
onos-classic-atomix-2         1/1     Running   2 (2m55s ago)   5h14m
onos-classic-onos-classic-0   1/1     Running   1 (7m34s ago)   5h14m
onos-classic-onos-classic-1   1/1     Running   2 (7m32s ago)   5h14m
onos-classic-onos-classic-2   1/1     Running   2 (7m36s ago)   5h14m
```

CLI access

```sh
kubectl -n micro-onos port-forward $(kubectl -n micro-onos get pods -l app=onos-classic -o name | cut --delimiter $'\n' --fields 1) 8101
```

```sh
ssh -p 8101 onos@localhost
```
Credentials

The credentials are by default:

| Login | Password |
| ------| ------   |
| onos  | rocks    |


## Dashboard

GUI activation

By default GUI in this ONOS versin ins not active It must be acttivated using ONOS CLI

```sh
onos@root > app-ids |grep gui

id=177, name=org.onosproject.gui
id=198, name=org.onosproject.openstacknetworkingui
id=202, name=org.onosproject.yang-gui
id=333, name=org.onosproject.gui2
```
```sh
app activate org.onosproject.gui2
```

GUI access

GUI port forwarding
```sh
kubectl -n micro-onos port-forward $(kubectl -n micro-onos get pods -l app=onos-classic-onos-classic -o name) --address <ip address of Kind VM> 8181
```

```
http://localhost:8181/onos/ui/
```

*********************
Configuration options
*********************
Configuration is dependend on the developer needs and soltution requirements. Detailed configuration options are:
https://wiki.onosproject.org/display/ONOS/Configuring+ONOS

Default configuration is included in installation process.

***************
Developer guide
***************
Developer Guide is :
https://wiki.onosproject.org/display/ONOS/Developer+Guide

***************************
Version control and release
***************************
Version 1.0 Final

***************
License
***************
Open source.

********************
Notice(dependencies)
********************
No dependencies.
