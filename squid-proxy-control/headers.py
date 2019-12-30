#!/usr/bin/env python
#-*- coding: utf-8 -*-
#Configuración
import ConfigParser
config = ConfigParser.ConfigParser()
config.read('/etc/squid-proxy-control/spc.cfg')

def standard():
    header = '<div id="header" class="noindex">'
    header += "<h1><a href='/'><img src='"
    header += config.get("System","logo") 
    header += "' alt='ACP' /></a></h1>"
    header += '</div>'
    return header
