#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sys
import os

import MySQLdb

# Configuration
import ConfigParser
config = ConfigParser.ConfigParser()
config.read('dhcp.cfg')

import getopt
import netaddr

# Open db Connection
try:
    db = MySQLdb.connect(
                        user=config.get("Database","user"),
                        passwd=config.get("Database","password"),
                        db=config.get("Database","db"),
                        host=config.get("Database","host")
                        )
except MySQLdb.Error, e:
     sys.stderr.write("ERR - Error %d: %s\n" % (e.args[0], e.args[1]))

scope = netaddr.ip.IPNetwork(config.get("dhcp","scope"))
for server in config.get("dhcp","server").split(","):
    try:
        # Run Query
        db.query("SELECT IP, MAC FROM Equipos")
        # Gather Data
        r = db.store_result()
        # For each result on the db
        for linea in r.fetch_row(maxrows=0):
            ip, mac = linea
            mac = netaddr.eui.EUI(mac, dialect = netaddr.mac_bare)
            ip = netaddr.ip.IPAddress(ip)
            if ip in scope:
                if config.get("System","debug"):
                    sys.stdout.write("netsh dhcp server " + str(server) +" scope " + str(scope.ip) + " add reservedip " + str(ip) + " " + str(mac) + "\n")
                # Run Netsh Command to reserve ip on the DHCP server
                os.system("netsh dhcp server " + str(server) +" scope " + str(scope.ip) + " add reservedip " + str(ip) + " " + str(mac) )

    except MySQLdb.Error, e:
         sys.stderr.write("ERR - Error %d: %s\n" % (e.args[0], e.args[1]))
    sys.stdout.flush()

# Close Connection
db.close ()