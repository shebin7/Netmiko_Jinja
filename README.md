

## Table of contents
* [General info](#general-info)
* [Technologies](#technologies)
* [Libraries](#libraries)
* [Setup](#setup)

## General info
This project is based on Netmiko and Jinja ,this programme will build a configuration file from Jinja Template and pushes that file inividualy to each Devices.
When the programme is first executed it does SSH to Terminal-Server/Intermediate-Server(Linux) and after getting access ,another command is executed from here 
to SSH login on remote Network Devices, Then after this Configuration files are pushed and saved on Network Devices
	
## Technologies
Project is created with:
* Python 3.6.9

Network Device from Cisco Sandbox
* GNS3 IOU and IOS Routers


## Libraries
 * [Netmiko](https://github.com/ktbyers/netmiko/blob/develop/README.md)

 * [Jinja2](https://jinja2docs.readthedocs.io/en/stable/)

 * [Rich](https://rich.readthedocs.io/en/latest/)
	
## Setup
To run this project, clone this to your local Folder using 'git clone'

```
$ git clone https://github.com/shebin7/Netmiko_Jinja
```
Then run it from IDE or from Terminal 
```
$ python3 Netmiko_Jinja.py
```

