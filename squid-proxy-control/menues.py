#!/usr/bin/env python
#-*- coding: utf-8 -*-
#Configuración
#import sigconfig

def mostrar(n1="", n2=""):
    nivel1 =  [ ["Home", "/", [ 
                                ["Login" , "/login", []],
                                ["Logout", "/logout", []],
                              ]
                ],
                ["Equipos", "/equipos",
                                        [
                                         ["Mostrar", "/equipos", []],
                                        ]
                ],
                ["Grupos", "/grupos",
                                        [
                                         ["Mostrar", "/grupos", []],
                                        ]
                ],                
                ["Herramientas", "/herramientas",
                                        [
                                         ["Log", "/log", []],
                                        ]
                ],
    ]
    output = '<div class="noindex" id="nav">'
    output += "<ul>"
    for item in nivel1:
        output += "<li"
        if item[0] == n1:
            output += " class='nav_selected' "
            nivel2 = item[2]
        output += "><a href='" + item[1] + "'>" + item[0] + "</a></li>"
    output += "</ul></div>"
    #Sub navbar
    output += '<div class="noindex" id="subnav">'
    if nivel2 <> []:
        output += "<ul>"
        for item in nivel2:
            output += "<li"
            if item[0] == n2:
                output += " class='nav_selected'"
            output += "><a href='" + item[1] + "'>" + item[0] + "</a></li>"
        output += "</ul>"
    output += "</div>"
    return output
