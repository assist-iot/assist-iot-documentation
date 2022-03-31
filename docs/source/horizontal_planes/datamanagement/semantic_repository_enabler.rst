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
   attached, each in a different format.

**TODO: diagram of logical objects**

There are few restrictions on how you can use these concepts to build
your repository. For example, it is possible to upload files of
arbitrary size and format.

To give some context, in GitHub terms, a **namespace** would translate a
user or a group. A **model** would be a repository, and a **model
version** would be a branch or tag. This is just an example, of course.

Model versions
--------------

The Semantic Repository does not force a specific versioning scheme on
your models. You can use for example Git branches and tags, plain
numbers, or `Semantic Versioning <https://semver.org/>`__.

The ``latest`` version tag is special – it is a pointer to the most
recent version of the model, as set by the model’s owner. It must always
be set manually. A model may have no ``latest`` pointer, and the pointer
may lead to a non-existent version. Enforcing a specific style of use is
up to the owner.

The benefit of the ``latest`` tag is that it allows clients to easily
retrieve the most recent version of the model (see the API user guide).

Content
-------

One model version can have multiple content files attached, each in a
different format. The format is recommended to correspond to the `Media
Type <https://www.iana.org/assignments/media-types/media-types.xhtml>`__
of the file – this is to best support HTTP-based technologies, such as
`Linked Data <https://www.w3.org/standards/semanticweb/data>`__.
However, you can always set the format to whatever you like.

The content for one model version *should* be immutable, i.e., you
should avoid modifying the once-uploaded content for a specific version.
This is so that clients can expect that the content for a given version
will not change suddenly, introducing a backward-incompatible change. It
is however *possible* to overwrite earlier-uploaded content, in case of
a mistake, for example. See the API guide below for more details.

Metadata
--------

Not implemented yet.



User guide – REST API
=====================

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

Currently, there is no other information in the namespace other than its
name.

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
3 characters, and at most 100 characters long - only contain lower or
upper letters of the latin alphabet, digits, dashes (``-``), and
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

**Note:** model names must meet the following criteria: - be at least 1
and at most 100 characters long - only contain lower or upper letters of
the latin alphabet, digits, dashes (``-``), and underscores (``_``) -
not start with one of the following characters: ``_-``

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

**Note:** version tags must meet the following criteria: - be at least 1
and at most 100 characters long - only contain lower or upper letters of
the latin alphabet, digits, dashes (``-``), underscores (``_``), dots
(``.``), and plus signs (``+``) - not start with one of the following
characters: ``._-+`` - not be ``latest``, which is a reserved tag (see
below)

``latest`` pointer
~~~~~~~~~~~~~~~~~~

The ``latest`` version pointer can be set on a given model using a PATCH
request:

=================== ============================
Request             Body
=================== ============================
``PATCH /w3c/sosa`` ``{"latestVersion": "1.0"}``
=================== ============================

============= ============================================
Response code Body
============= ============================================
200           ``{"message": "Updated model 'w3c/sosa'."}``
============= ============================================

Now it can be used in GET requests instead of the explicit version. So,
``GET /w3c/sosa/latest`` is equivalent to ``GET /w3c/sosa/1.0``.

**Important:** to prevent accidental overwrites, **it is not possible to
make POST, PATCH, or DELETE requests via the ``latest`` pointer**. Use
the explicit version in the URL instead.

The version pointer can also be set during model creation:

================= ============================
Request           Body
================= ============================
``POST /w3c/ssn`` ``{"latestVersion": "1.0"}``
================= ============================

============= ===========================================
Response code Body
============= ===========================================
200           ``{"message": "Created model 'w3c/ssn'."}``
============= ===========================================

To change the pointer to a new value, simply make a PATCH request. To
**unset** the pointer completely, use the special ``@unset`` value in a
PATCH request:

=================== ===============================
Request             Body
=================== ===============================
``PATCH /w3c/sosa`` ``{"latestVersion": "@unset"}``
=================== ===============================

============= ============================================
Response code Body
============= ============================================
200           ``{"message": "Updated model 'w3c/sosa'."}``
============= ============================================

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

To see the available formats, make a ``GET /w3c/sosa/1.0`` request:

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

Overwriting content
^^^^^^^^^^^^^^^^^^^

As noted in the `User guide <#user-guide>`__, the content for a specific
version of a model *should* be immutable. So, if you try to repeat the
request presented above, it will be rejected with an HTTP 400 error:

::

   {
     "error": "Content in format 'text/turtle' already exists for this model version. If you want to update it, it is recommended to create a new version instead. If you really want to overwrite this content, retry the upload with the 'overwrite=1' query parameter."
   }

If you really want to overwrite this content (in case of a mistake, for
example), add the ``overwrite=1`` parameter:

=============================================================
===============
Request                                                       Body
=============================================================
===============
``POST /w3c/sosa/1.0/content?format=text/turtle&overwrite=1`` content: (file)
=============================================================
===============

Response:

::

   {
     "message": "Uploaded content in format 'text/turtle' for model 'w3c/sosa/1.0'. Checksum: 5b844292b8402e448804f9c9f100d59e",
     "warnings": [
       "Overwrote an earlier version of the content."
     ]
   }

Changing the default format
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Not implemented yet.

Downloading the content
^^^^^^^^^^^^^^^^^^^^^^^

Downloading the models is very straightforward. The most explicit way is
to specify the namespace, model, version, and the desired format:

``GET /w3c/sosa/1.0/content?format=text/turtle``

You can also omit the ``format`` parameter to obtain the content in the
default format:

``GET /w3c/sosa/1.0/content``

If you have set the ``latest`` tag for this model, you can use it
instead of the explicit version, to fetch the most recent version of the
model.

There is also a second, shorter style of URLs for downloading content,
with the ``/c`` prefix:

1. ``GET /c/w3c/sosa/1.0/text/turtle``
2. ``GET /c/w3c/sosa/latest/text/turtle``
3. ``GET /c/w3c/sosa/1.0``
4. ``GET /c/w3c/sosa/latest``
5. ``GET /c/w3c/sosa``

Assuming that the ``latest`` tag is set to version ``1.0`` and the
default format is ``text/turtle``, all of the above requests will return
the same result. Request 5 is simply a shorthand for “the latest version
of this model, in the default format”, which should be sufficient for
most applications.

In all cases the response will be simply the stored file, with the
appropriate Content-Type header.

Deleting models and other objects
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

TODO, partially implemented.

Browsing collections
~~~~~~~~~~~~~~~~~~~~

Not implemented yet.

Meta endpoints
~~~~~~~~~~~~~~

TODO, partially implemented.



User guide – graphical user interface
=====================================

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



