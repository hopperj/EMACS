EMACS 
Environmental Management And Control System
=====

Volta November Hackathon

EMACS is a distributed system for monitoring and control of various environmental variables in your home. Each distributed platform reads temperature, humidity, and pressure before relaying the data over a radio link to a central server. 

The central server running on a Rasberry Pi is responsible for collecting data from the various sensor nodes and pushing them to a web interface viewable by the end user. The web interface allows users to monitor the status of connected sensors and change variables for temperature and humidity which are then relayed to a control interface.


