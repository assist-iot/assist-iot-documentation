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
TUNGSTEN (https://tungstenfabric.github.io/website/Tungsten-Fabric-Ubuntu-one-line-install-on-k8s.html)

uONOS (https://docs.onosproject.org/developers/deploy_with_helm/)
ONOS can also be deployed on a bare metal cluster provisioned with Rancher or equivalent.
Kubectl and Helm are can be run from your local PC to control the remote cluster.

To deploy the Helm chart locally:
1. First, you will need to install Docker (https://docs.docker.com/get-docker/) to build and deploy an image locally.
2. Second, install Kind (https://kind.sigs.k8s.io/).
        Kind v0.11.0 at least is required, which provides the K8S API v1.21
3. Third, install Helm version 3. On OSX, this Helm can be installed using Brew (https://brew.sh/):
        brew install helm

*********************
Configuration options
*********************
Will be determined after the release of the enabler.

***************
Developer guide
***************
Will be determined after the release of the enabler.

***************************
Version control and release
***************************
Version 1.0

***************
License
***************
Open source.

********************
Notice(dependencies)
********************
No dependencies.
