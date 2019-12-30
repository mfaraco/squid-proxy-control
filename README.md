# Proxy ACL Control for Education running on Squid 2

This project provides 3 components:

1. Web interface to control Squid access controls lists
2. squid 2.0 helper to enforce ACLs
3. dhcp reservation script to add machine IPs based on MAC and control access based on IP

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

You need Squid 2
Apache server with web.py framework and support for wsgi and Python
Windows DHCP Server installed and access to modify using netsh

### Installing

Install apache 2 and wsgi

```
sudo apt-get install apache2 apache2-utils python \
sudo apt-get install libapache2-mod-wsgi
```

## Deployment

Install Apache2 Server for the controlling interface
Add IP and client on the mysql database (no need to run it on the same server)
Add [Squid helper](https://wiki.squid-cache.org/Features/AddonHelpers) locally and configure as example config file

## Built With

* [Python](http://python.org/) - Python
* [web.py](http://webpy.org/) - web.py simple framework
* [mysql](https://mysql.com/) - MySQL
* [Squid Proxy](http://squid-cache.org/) - Squid acting as proxy

## Authors

* **Mariano Faraco** - *Initial work* - [mfaraco](https://github.com/mfaraco)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
