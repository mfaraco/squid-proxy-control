#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sys

# Módulo para usar MySQL
import MySQLdb

# Configuración
import ConfigParser
config = ConfigParser.ConfigParser()
config.read('/etc/squid-proxy-control/spc.cfg')
sys.path.append(config.get("System","path"))

import getopt

# Abro la base de datos
try:
    db = MySQLdb.connect(
                        user=config.get("Database","user"),
                        passwd=config.get("Database","password"),
                        db=config.get("Database","db"),
                        host=config.get("Database","host")
                        )
except MySQLdb.Error, e:
     print "ERR - Error %d: %s" % (e.args[0], e.args[1])
     sys.exit (1)

while(1):
    # Ejecuto la consulta     
    cursor = db.cursor ()
    linea=sys.stdin.readline()[:-1]
    try:
        ip, acceso= linea.split(" ")
        query= "SELECT * FROM ip_acceso WHERE ip = '" + ip +"' AND acceso= " + acceso
#	sys.stderr.write("IP %s\n"%ip)
#    	sys.stderr.write("ACCESO %s\n"%acceso)
        cursor.execute (query)
        if cursor.rowcount == 0:
            sys.stdout.write("ERR\n")
        else:
            sys.stderr.write("MATCH " + str(acceso) + ", " + str(ip) + "\n")
            sys.stdout.write("OK\n")
        sys.stdout.flush()
        cursor.close ()
    except:
#        sys.stderr.write("ERROR en helper: " + linea + "\n")
        sys.stdout.write("ERR\n")
db.close ()
