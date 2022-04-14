.. _Semantic Translation enabler:

############################
Semantic Translation enabler
############################

.. contents::
  :local:
  :depth: 1

Documentation for the Semantic Translation Enabler of ASSIST-IoT.



Introduction
============

Semantic interoperability is the ability of different applications and
business partners to exchange data with unambiguous, shared meaning. As
a result, data analysis and knowledge discovery can be done on a
federation of systems.

**Semantic Translation Enabler (STE)** enables alignments-based semantic
translation of RDF data (messages). At its core STE builds on a
considerably enhanced version of the Inter Platform Semantic Mediator
(IPSM) component, developed by the INTER-IoT project.

The translation performed by STE is based on alignments and uses a
deployment-specific modularized `central
ontology <IPSM/Central-ontology>`__. For IoT domain, the core modules
describing, e.g. devices, observations are (usually) based on `GOIoTP
(Generic Ontology of IoT
Platforms) <https://inter-iot.github.io/ontology>`__ that is a meta-data
reference data model. Additionally, any domain specific module can be
included e.g. medical ontology, logistic ontology. However, central
ontology can be any ontology that can serve as a central data model. It
is not directly used configure STE but should be considered when
defining alignments that are used for STE configuration. Additionally,
any domain specific module can be included e.g. medical ontology,
logistic ontology.

The alignment is a set of correspondences between simple entities or
complex structure from source and target ontologies. It contains rules
for transformation between input and output RDF graphs. Specifically,
STE translates RDF graph named *payload* (that is part of the message
send to STE). Alignments are parts of STE instance configuration, and
are used directly to execute translation. Semantic translation always
constitutes application of two alignments - one from source ontology to
central ontology, the other from central ontology to target ontology.

The following figure shows a sample situation with four IoT artifacts
(P1-4). Each with it’s own ontology (O1-4). The central ontology
contains modules g1…gn. The two-way communication requires preparation
of two alignments: (i) from artifact’s ontology to central ontology
e.g. A1G, (ii) from central ontology to artifact’s ontology e.g. AG1.
Each alignments contains correspondences between ontology modules that
are required for this part of communication. |Overview of translation
with central modularized ontology|

*Overview of translation with central modularized ontology*

To achieve semantic interoperability between two artifacts:

1. Instantiate modular central ontology
2. Select/define artifact’s ontologies: create from scratch or use one
   of existing tools
3. Align semantics between ontology of each artifact and central
   ontology (set of alignments)
4. Implement syntactic translators
5. Configure STE - upload alignments, create translation channels

The following figure shows a process of sending a message from source to
target artifact that needs to be semantically and syntactically
translated. |Process overview|\ *Process overview*

The message originates at source artifact in it’s format and semantics
e.g. XML message with respect to XML Schema. To use STE the message
needs to be transformed to RDF with source artifact’s semantics. This
translation is called `syntactic
translation <https://docs.google.com/document/d/1dXeOnX8_lQXBBMb17cbcevSf02mQX93apop6o6J3L94/edit>`__.
In fact, when STE is to be used in a standalone mode (without other
INTER-IoT layers), syntactic translation can be implemented in any
arbitrary component that will “prepare” input for semantic translation.
Note that, conversion to RDF may not be necessary, when artifacts
already have communication based on RDF. When a source artifact does not
support semantics, an RDF represantation of data exchanged with the
ecosystem needs to be proposed.

When the message arrives at STE, the RDF named graph *payload* is
translated with respect to configuration of the semantic translation
channel (see `Architecture <IPSM/Architecture>`__). Usually two
alignments are applied, however STE can be configured with special
predefined IDENTITY alignment that does not change the graph. Another
remark here, is that STE follows the rule: translate only what can be
translated, leave the rest as it was. The resultant message is expressed
in RDF with semantics corresponding to target semantic of last applied
alignment.

This message can be feed into another syntactic translator that will
transform it’s format to e.g. JSON cosidering target artifact’s
semantics. Another possible scenario is that there are applications
consuming data in RDF and central semantics. In such case, second
syntactic translation is not necessary.

.. |Overview of translation with central modularized ontology| image:: images/platforms.png
.. |Process overview| image:: images/process.png




Place in architecture
=====================

TBD



Version control and releases
============================

TBD



License
=======

The Inter Platform Semantic Mediator is licensed under the **Apache
License, Version 2.0** (the “License”).

You may obtain a copy of the License at:
http://www.apache.org/licenses/LICENSE-2.0



Notice dependencies
===================

Dependency list and licensing information will be provided before the
first major release of the STE.



