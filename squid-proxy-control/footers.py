#!/usr/bin/env python
#-*- coding: utf-8 -*-
#Configuración
import ConfigParser
config = ConfigParser.ConfigParser()
config.read('/etc/squid-proxy-control/spc.cfg')

def standard():
    output = '''
        <div id="footer">
            <table style="table-layout:fixed; width: 100%;">
                <tr>
                    <td style="text-align: left;">Departamento de Informatica y Tecnologia</td>
                    <td style="text-align: right;">v. 
            ''' + config.get("System","version") + '''</td>
                </tr>
            </table>
        </div>
    '''
    return output

