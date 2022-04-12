.. _Location processing:

###################
Location processing
###################

.. contents::
  :local:
  :depth: 1

Location Processing Enabler
===========================

Introduction
------------

This Enabler was scoped out from the original (Geo)localization Enabler.
It’s been decided to split its functionality into two enablers – one
concentrating mostly on the hardware part and this one – focusing on
localization data processing. Eventually, the Location Processing
Enabler will provide flexible geofencing capabilities allowing to:

Features
--------

-  define “regions” and “points” of interest, and identify them in a
   unique way
-  update the geometry of defined regions and points (possibly also in a
   streaming fashion)
-  query relationships between a given position and selected
   region/point(s)
-  create and subscribe to streams of “geofencing events”.

Place in architecture
---------------------

For ASSIST-IoT Pilot it will be closely used with Location Trackin
EnBLER

User guide
----------

TBD

Prerequisites
-------------

Scala
~~~~~

`Scala <https://www.scala-lang.org/>`__ is a language of preference for
the SRIPAS group. Scala provides support for functional idioms and
static typing. Those two features and familiarity with the language are
arguments for Scala in the IoT environment, to support high reliability
demand of the business.

PostGIS
~~~~~~~

PostGIS is a spatial database extender for PostgreSQL object-relational
database.

REST (Enabler’s API)
~~~~~~~~~~~~~~~~~~~~

Currently it is decided as project-wide standard. REST is overall a web
standard.

Installation
------------

TBD

Configuration options
---------------------

TBD

Developer guide
---------------

TBD

Version control and release
---------------------------

We will use gitlab as version control and release tooling.

License
-------

TBD



