.. _Semantic Repository enabler:

###########################
Semantic Repository enabler
###########################

.. contents::
  :local:
  :depth: 1

This repo is for the API part of the Semantic Repository enabler.
However, the docs are for the complete enabler. We will probably need to
fix that later.

For now, feel free to put as much content in this wiki as possible. We
will tidy it up sometime around M18.

We are kind of trying to follow the `tentative
template <https://vrionisnickrtd-tutorial.readthedocs.io/en/latest/index.html>`__
for enabler documentation.



Introduction
============

This enabler offers a “nexus” for data models, ontologies, and other
files, that can be uploaded in different file formats, and served to
users with relevant documentation. This enabler is aimed to support
files that describe data models or support data transformations, such as
ontologies, schema files, semantic alignment files etc. However, there
are no restrictions on file format and size.



Features
========

Do mind that almost none of these features are implemented yet.

TODO: add links to relevant help pages

Storing data models
~~~~~~~~~~~~~~~~~~~

-  Storage of any type of data model, both textual and binary.
-  Ability to provide multiple formats of one data model, depending on
   the requester’s preferences.
-  Grouping data models into namespaces.
-  Flexible versioning with arbitrary tag names.
-  Granular and easy-to-use access control.

Metadata
~~~~~~~~

-  Tracking provenance information (creation/modification dates,
   authors).
-  Ability to attach arbitrary additional metadata.
-  Metadata searching and sorting.

Documentation
~~~~~~~~~~~~~

-  Support for Markdown/ASCIIDOC manual documentation pages.
-  Automatic documentation generation for some data model types.
-  Flexible plugin architecture for creating additional documentation
   generation modules.



Place in architecture
=====================

TBD



User guide
==========

TBD



REST API reference
==================

.. raw:: html
   :file: semantic_repository_enabler/api.html


Prerequisites
=============

TBD



Installation
============

TBD



Configuration
=============

TBD



Developer guide
===============

TBD



Version control and releases
============================

TBD



License
=======

TBD



Notice (dependencies)
=====================

TBD!

image test

.. figure:: semantic_repository_enabler/uploads/2d59a4113785508222cd85fccda8baf9/ibspan-bg-square.png
   :alt: ibspan-bg-square

   ibspan-bg-square



