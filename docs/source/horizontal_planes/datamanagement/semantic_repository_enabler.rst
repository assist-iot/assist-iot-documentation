.. _Semantic Repository enabler:

###########################
Semantic Repository enabler
###########################

.. contents::
  :local:
  :depth: 1

Documentation for the Semantic Repository enabler of ASSIST-IoT.



Introduction
============

This enabler offers a “nexus” for data models, ontologies, and other
files, that can be uploaded in different file formats, and served to
users with relevant documentation. This enabler is aimed to support
files that describe data models or support data transformations, such as
ontologies, schema files, semantic alignment files etc. However, there
are no restrictions on file format and size.

Overall focus of the Semantic Repository’s design is high performance,
scalability, and resiliency. It should be able to scale up and down to
meet the specific use case.



Features
========

The enabler is in active development. Most features listed below are not
implemented yet. Marked in **bold** are those that are already
functioning.

Storing data models
~~~~~~~~~~~~~~~~~~~

-  **Storage of any type of data model, both textual and binary.**
-  **Ability to provide multiple formats of one data model, depending on
   the requester’s preferences.**
-  **Grouping data models into namespaces.**
-  **Flexible versioning with arbitrary tag names.**
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

The Semantic Repository enabler exposes a single REST API endpoint for
both manipulating the repository’s contents, as well as for retrieving
stored data models. There is also a graphical user interface for
performing most of the same tasks.

Basic concepts
--------------

-  **Namespace** – a top-level “group” in the repository, which can host
   any number of models.
-  **Model** – a data model, which can have many versions.
-  **Model version** – a specific version of a model. You can upload the
   content of a data model only to its specific version. The version can
   also have associated documentation pages and other metadata.
-  **Content** – each model version can have many content files
   attached, each in a different format. The format is recommended to
   correspond to the `Media
   Type <https://www.iana.org/assignments/media-types/media-types.xhtml>`__
   of the file – this is to best support HTTP-based technologies, such
   as Linked Data. However, you can always set the format to whatever
   you like.

**TODO: diagram of logical objects**

There are few restrictions on how you can use these concepts to build
your repository. For example, it is possible to upload files of
arbitrary size and format.

To give some context, in GitHub terms, a **namespace** would translate a
user or a group. A **model** would be a repository, and a **model
version** would be a branch or tag. This is just an example, of course.

REST API
--------

The following is a brief guide to using the API in practice. The
examples follow a basic use case of storing several `W3C
ontologies <https://www.w3.org/standards/semanticweb/ontology>`__.

The full specification of the REST API can be found in the `REST API
reference <#rest-api-reference>`__ section.

General information
~~~~~~~~~~~~~~~~~~~

The API follows a very simple structure of
/{namespace}/{model}/{model_version}. In general, ``POST`` creates a new
*thing* at the given URL, ``GET`` retrieves it, ``DELETE`` deletes it,
and ``PATCH`` modifies it.

The API only returns responses in plain JSON. The following guide should
give you a good idea of what the responses look like, but you can also
find the full schemas in the `REST API
reference <#rest-api-reference>`__ section.

It generally does not matter whether a URL ends with a slash or not.

Creating and retrieving models
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Step 1: create a namespace
^^^^^^^^^^^^^^^^^^^^^^^^^^

First, we will need to create a namespace for your models. We will name
it ``w3c``.

============= ============
Request URL   Request body
============= ============
``POST /w3c`` (empty)
============= ============

============= ===========================================
Response code Response body
============= ===========================================
200           ``{"message": "Created namespace 'w3c'."}``
============= ===========================================

You can examine the created namespace by performing an HTTP GET request:

============ ============
Request URL  Request body
============ ============
``GET /w3c`` –
============ ============

============= ===================
Response code Response body
============= ===================
200           ``{"name": "w3c"}``
============= ===================

Currently, there is no other in the namespace other than its name. We
will change this shortly.

You can also list all namespaces in the repository:

=========== ============
Request URL Request body
=========== ============
``GET /``   –
=========== ============

============= =============
Response code Response body
============= =============
============= =============

\| 200 \|

.. raw:: html

   <pre>{<br>&emsp;"namespaces": { <br>&emsp;&emsp;"items": [{"name": "w3c"}] <br>&emsp;&emsp;"totalCount": 1 <br>&emsp;} <br>}</pre>

\|

A collection of namespaces is returned. Browsing such collections is
described in detail in the `Browsing
collections <#browsing-collections>`__ section below.

**Note:** namespace name must meet the following criteria: - be at least
3 characters, and at most 100 characters long - must only contain lower
or upper letters of latin alphabet, digits, dashes (``-``), and
underscores (``_``)

Step 2: create models
^^^^^^^^^^^^^^^^^^^^^

In this example we will create two models: ``sosa`` and ``ssn``,
corresponding to `two well-known IoT
ontologies <https://www.w3.org/TR/vocab-ssn/>`__. Creating a model is
similar to creating a namespace:

================= =======
Request           Body
================= =======
``POST /w3c/ssn`` (empty)
================= =======

============= ===========================================
Response code Body
============= ===========================================
200           ``{"message": "Created model 'w3c/ssn'."}``
============= ===========================================

and for sosa:

================== =======
Request            Body
================== =======
``POST /w3c/sosa`` (empty)
================== =======

============= ============================================
Response code Body
============= ============================================
200           ``{"message": "Created model 'w3c/sosa'."}``
============= ============================================

You can examine the created model:

================= ====
Request           Body
================= ====
``GET /w3c/sosa`` –
================= ====

============= ========================================
Response code Body
============= ========================================
200           ``{"namespace": "w3c", "name": "sosa"}``
============= ========================================

When you again examine the contents of the namespace (``GET /w3c``), you
will see a collection of models:

::

   {
     "models": {
       "items": [
         {
           "name": "sosa",
           "namespace": "w3c"
         },
         {
           "name": "ssn",
           "namespace": "w3c"
         }
       ],
       "totalCount": 2
     },
     "name": "w3c"
   }

**Note:** model names must meet the same requirements as names for
namespaces.

Step 3: create versions
^^^^^^^^^^^^^^^^^^^^^^^

You cannot upload content to a model directly. First, you must
explicitly create a specific version of the model and work with that.

For example, to create a version ``1.0`` of model ``sosa``:

====================== =======
Request                Body
====================== =======
``POST /w3c/sosa/1.0`` (empty)
====================== =======

============= ========================================================
Response code Body
============= ========================================================
200           ``{"message": "Created model version 'w3c/sosa/1.0'."}``
============= ========================================================

You can examine the content of this version:

===================== ====
Request               Body
===================== ====
``GET /w3c/sosa/1.0`` –
===================== ====

+------------------------------------------------------+---------------+
| Response code                                        | Body          |
+======================================================+===============+
| 200                                                  | ``{"formats": |
|                                                      |  {}, "model": |
|                                                      |  "sosa", "nam |
|                                                      | espace": "w3c |
|                                                      | ", "version": |
|                                                      |  "1.0"}``     |
+------------------------------------------------------+---------------+

You can also retrieve a list of versions for the model (again,
``GET /w3c/sosa``):

::

   {
     "name": "sosa",
     "namespace": "w3c",
     "versions": {
       "items": [
         {
           "model": "sosa",
           "namespace": "w3c",
           "version": "1.0"
         }
       ],
       "totalCount": 1
     }
   }

Uploading content
~~~~~~~~~~~~~~~~~

In the following examples we will focus on uploading and retrieving
content for the ``/w3c/sosa/1.0`` model version we have created in the
previous section.

To upload content in format ``text/turtle``:

================================================= ===============
Request                                           Body
================================================= ===============
``POST /w3c/sosa/1.0/content?format=text/turtle`` content: (file)
================================================= ===============

In the body of the request (form-data) set the field ``content`` to the
file you want to upload.

In response you will get:

::

   {
       "message": "Uploaded content in format 'text/turtle' for model 'w3c/sosa/1.0'. Checksum: 5b844292b8402e448804f9c9f100d59e",
       "warnings": [
           "The default format of this model version was set to 'text/turtle'.'"
       ]
   }

The response notes that the default format of the model version was set
to “text/turtle” because that is the first format we have uploaded. You
can upload more content files for the model version in a similar manner.

The Semantic Repository support multipart, streaming uploads and can
handle files of any size this way.

To see the available formats, do a ``GET /w3c/sosa/1.0`` request:

::

   {
     "defaultFormat": "text/turtle",
     "formats": {
       "text/turtle": {
         "contentType": "text/turtle",
         "md5": "5b844292b8402e448804f9c9f100d59e",
         "size": 27326
       }
     },
     "model": "sosa",
     "namespace": "w3c",
     "version": "1.0"
   }

In the response notice that: - ``defaultFormat`` has been set to
“text/turtle”. You can change that later. - ``formats`` is keyed by
format name. - ``contentType`` displays the content type of the uploaded
file, which in this case is the same as format. - ``md5`` is the MD5
checksum of the entire file. - ``size`` is the file’s size in bytes.

Changing the default format
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Not implemented yet.

Deleting models and other objects
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

TODO, partially implemented.

Browsing collections
~~~~~~~~~~~~~~~~~~~~

Not implemented yet.

Meta endpoints
~~~~~~~~~~~~~~

TODO, partially implemented.

Graphical user interface
------------------------

The GUI of the Semantic Repository is under development.



REST API reference
==================

.. raw:: html
   :file: semantic_repository_enabler/api.html


Prerequisites
=============

There are currently no prerequisites for installing this enabler.



Installation
============

The installation procedure for this enabler is under development.



Configuration
=============

This enabler currently does not have any configuration settings. They
will be added later.



Developer guide
===============

The Semantic Repository is written in `Scala
3 <https://www.scala-lang.org/>`__, using the `Akka
framework <https://akka.io/>`__. The information about the managed
objects is stored in `MongoDB <https://www.mongodb.com/>`__ and the
files are stored in `MinIO <https://min.io/>`__ (S3-compatible storage).

TODO: architecture diagram, when finalized



Version control and releases
============================

TODO



License
=======

The Semantic Repository is licensed under the **Apache License, Version
2.0** (the “License”).

You may obtain a copy of the License at:
http://www.apache.org/licenses/LICENSE-2.0



Notice (dependencies)
=====================

Dependency list and licensing information will be provided before the
first major release.



