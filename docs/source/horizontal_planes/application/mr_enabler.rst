.. _MR enabler:

############
MR enabler
############

.. contents::
  :local:
  :depth: 1

***************
Introduction
***************
The MR enabler receives data and transforms it in a format suitable for visualization through head-mounted MR devices. Data, which may come from long-term storage or real-time data streams, are requested according to its relevance to the user. Information is displayed to the user, according to their authorization/access rights, via an MR device. The enabler supports user interaction with the virtual content and view customization.

***************
Features
***************
The MR enabler: 
 * visualizes the model of the construction site through the head-mounted MR devices, along with the danger zones of the site. The model of the site and all its related data come from the long-term storage,
 * visualizes the location of the workers of the construction site, along with their crucial information,
 * receives alert messages from real-time data streams and display their details to the user
 * provides the ability to create and send new reports
 * and captures and stores media files in order to include them in a report.

*********************
Place in architecture
*********************
The MR enabler is located in the application and service layer of Assist-IoT. It will provide immersive experience to practitioners of ASSIST-IoT, transforming collected data into more suitable formats for visualization capabilities over head-mounted MR displays.
The ASSIST-IoT Application and Services plane is intended to provide access to data via human-centric visualization enablers. 

***************
User guide
***************
In order to use the MR enabler, the user needs to power up the MR device, unlock it and then hold out one of their hands with the palm facing up and look at their wrist, where the menu button will appear. Pressing the button with their free hand will show up the central navigation menu, where the user can find and execute the MR enabler application. Alternatively, the user can use the device's portal of the MR device that will be available through any browser on a computer of the local network, using the MR device's local IP as the URL. 
The MR enabler will load and visualize the construction site model, along with its relative data (for instance its dangerous zones) and its handles, that will allow the user to manipulate the model's transform (position, rotation and scale). The handles have different colors and shapes in order to be more understandable for the user about the model's transform attribute that they are affecting. 
The user has to keep the palm of their right hand open in order to access the MR enabler application's menu. The MR enabler can receive alerts from the real-time storage on runtime, visualize them to the user, along with their details and then the user has the option to silence the alert from the menu, after that they have acknowledged about the incoming alert.
Moreover, the MR application can present the location of the workers inside the BIM building, followed by a panel, filled in with their crucial, for the HS officer, information.
The application also provides the ability of localization, meaning that the user is able to choose one from several languages for the displayed messages. He is able to change language at any time, through the settings panel that exists in the application’s main menu.
Last but not least, the application's menu also offers the ability to capture a media (either a photo or a video) and store it in the device's storage in order to include it in a report in combination with other report and action information filled in. In order to capture a media file, the user needs to guide into the application's report action’s panel and click with their free hand the button "Open Camera" and use the Camera panel that pops up next to the menu. 

***************
Prerequisites
***************
The MR enabler is designed to be executed on a Microsoft Hololens 2 device with ARM64 architecture. Access to a computer that is connected to the same network with the device is needed for the installation of the MR enabler application.

***************
Installation
***************
In order to install the application, the user has to use the device's portal of the MR device that will be available through any browser on a computer of the local network, using the MR device's local ip as the url. The users has to go to Views > Apps and find the Deploy apps section, click "Browse..." and select the package with the installation files of the MR enabler, that will be either in ".appx" or ".msix" format, and is required for the package to be signed with a digital signature. The user should also check the box next to "Allow me to select framework packages", if it is the first time installing the app on their device. Finally, they should click on "Install" to complete the installation (or "Next" if option "Allow me to select framework packages" is selected).

.. figure:: ./installation.svg
   :width: 800px 

*********************
Configuration options
*********************
The following table lists the configurable parameters of the MR enabler.

+---------------------------+-------------------------------------------+
| Parameter                 | Description                               |
+===========================+===========================================+
| ``name``                  | Gets the name of the construction site    |
+---------------------------+-------------------------------------------+
| ``pilot_uuid``            | Gets the unique id of the construction    |
|                           | site                                      |
+---------------------------+-------------------------------------------+
| ``edbe_url``              | Access point’s IP for consuming real–time |
|                           | data                                      |
+---------------------------+-------------------------------------------+
| ``edbe_port``             | Access point’s Port for consuming         |
|                           | real-time data                            |
+---------------------------+-------------------------------------------+
| ``alerts_topic``          | Path to subscribe to Edge Data Broker to  |
|                           | receive real-time alerts                  |
+---------------------------+-------------------------------------------+
| ``workers_location_topic``| Path to subscribe to Edge Data Broker to  |
|                           | receive real-time workers’                |
|                           | location from the Edge Data Broker        |
+---------------------------+-------------------------------------------+
| ``semantic_url``          | Access point’s IP for receiving ifc       |
|                           | models                                    |
+---------------------------+-------------------------------------------+
| ``semantic_port``         | Access point’s port for receiving ifc     |
|                           | models                                    |
+---------------------------+-------------------------------------------+
| ``building_path``         | Receives IFC models files                 |
+---------------------------+-------------------------------------------+
| ``ltse_url``              | Access point’s IP for receiving           |
|                           | localization dictionaries, worker’s data  |
|                           | and sending reports                       |
+---------------------------+-------------------------------------------+
| ``ltse_port``             | Access point’s port for receiving         |
|                           | localization dictionaries, worker’s data  |
|                           | and sending reports                       |
+---------------------------+-------------------------------------------+
| ``workers_info``          | Receives training and medical data of     |
|                           | the workers                               |
+---------------------------+-------------------------------------------+
| ``report_files``          | Gets the path for uploading and saving    |
|                           | reports                                   |
+---------------------------+-------------------------------------------+


***************
Developer guide
***************
In order to test the correct functionality of the MR enabler, the developers need a device where they can execute scripts, host a mqtt broker and an instance of the LTS enabler. Any scripting language is able to test the MR enabler, as long as the language supports sending messages with the HTTP and the MQTT protocols. The developer then is able to:
* Send alerts from the script with the mqtt protocol to a broker and check if they receive them inside the MR enabler application
* Send reports to the LTS enabler and check the LTS tables to confirm that the report has been sent correctly
* Check the PUD enabler if the MR device is constantly sending correct health metrics.

***************************
Version control and release
***************************
Version 0.2.0.0

***************
License
***************
GNU AGPLv3

