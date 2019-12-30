#!/usr/bin/env python
#-*- coding: utf-8 -*-

# Librerías standard y de sistema
import sys

#Configuración
import ConfigParser
config = ConfigParser.ConfigParser()
config.read('/etc/squid-proxy-control/spc.cfg')
sys.path.append(config.get("System","path"))

# Import Date-Time functions
import datetime

# Web.py
import web

# Beaker Middleware for Sessions
from beaker.middleware import SessionMiddleware

# Modulos
import headers
import footers
import menues

# Import authentication routines against LDAP
import auth

#Location of the render templates
render = web.template.render(config.get("System","path") + '/templates/', cache=False)

# URLs accepted by web.py
urls = (
        '/', 'index',
        '/login', 'login',
        '/logout', 'logout',
        '/grupos$', 'grupos',
        '/grupo/(.*)/(.*)$', 'acceso_grupo',
        '/grupo/(.*)$', 'acceso_grupo',
        '/equipos$', 'equipos',
        '/equipo/(.*)/(.*)$', 'equipo',
        '/equipo/(.*)$', 'equipo',
        '/herramientas$', 'herramientas',
)

## AUTHORIZATION STUFF
#
def initsession(session):
    session['nivel_autorizacion'] = [0,]
    session['nombre'] = ''
    session['username'] = ''
    session['groups'] = [0,]
    session['loggedin'] = 0

def checkaccess(where=0):
    session = web.ctx.environ['beaker.session']
    if "logeddin" in session:
        if session["logeddin"] == 1:
            if where in session['nivel_autorizacion']:
                return True
            else:
                return False
    else:
        initsession(session)
        raise web.seeother("/../login")

# Página de Inicio
class index:
    '''
    Muestra la pagina de inicio del sistema
    '''
    def GET(self):
        checkaccess()
        pagina = { 'header'    : headers.standard(),
                   'menues'    : menues.mostrar("Home"),
                   'footer'    : footers.standard()
                 }
        return render.index(pagina)
    
class login:
    '''
    Formulario y pagina de Login para empleados
    '''
    def GET(self):
        pagina = { 'header'    : headers.standard(),
                    'menues'    : menues.mostrar("Home"),
                   'footer'    : footers.standard()
                 }
        grupos = db.query("SELECT * FROM Grupos")
        return render.login(pagina, False, grupos)

    def POST(self):
        session = web.ctx.environ['beaker.session']
        i = web.input()
        if auth.validate(i.username, i.password):
            initsession(session)
            session['logeddin'] = 1
            session['nombre'] = auth.getdata(i.username, i.password)
            session['username'] = i.username
            session.save()

            if i.grupo == "0":
                raise web.seeother('/../')
            else:
                # Si seleccionó un grupo lo envío directo
                raise web.seeother('/../grupo/' + str(i.grupo))
        else:
            pagina = { 'header'    : headers.standard(),
                       'menues'    : menues.mostrar("Home"),
                       'footer'    : footers.standard()
                     }
            grupos = db.query("SELECT * FROM Grupos")
            return render.login(pagina, True, grupos)

class logout:
    '''
    Pagina de Logout
    '''
    def GET(self):
        session = web.ctx.environ['beaker.session']
        try:
            log.write(db,session['username'],"Salio del Sistema")
        except:
            None
        session.invalidate()
        raise web.seeother('/../')

class acceso_grupo:
    def GET(self, grupo=0, acceso=0):
        checkaccess()
        if acceso == 0:
            # es sólo display
            try:
                equipos = db.query("SELECT Equipos.*, ip_acceso.acceso FROM Equipos, ip_acceso WHERE EXISTS (SELECT * FROM equipo_grupo WHERE grupo=" + str(grupo) + " AND equipo_grupo.equipo = Equipos.ip ) AND ip_acceso.ip = Equipos.ip")          
                pagina = { 'header'    : headers.standard(),
                            'menues'    : menues.mostrar("Grupos"),
                           'footer'    : footers.standard()
                         }
                descripcion = "SELECT * FROM Grupos WHERE id=" + str(grupo)
                descripcion = db.query(descripcion)[0].descripcion
                grupo = { 'descripcion' : descripcion,
                          'id' : grupo,
                }
                return render.listar_grupos_iconos(pagina, equipos, grupo)
            except:
                data = [ "Error", "No se encuentra el equipo en el sistema", "/../grupos", 5 ]
                return render.mensaje_sistema(data)
        else:
            #estoy aplicando un nivel a todo un grupo
            try:
                equipos = db.query("SELECT Equipos.*, ip_acceso.acceso FROM Equipos, ip_acceso WHERE EXISTS (SELECT * FROM equipo_grupo WHERE grupo= $grupo AND equipo_grupo.equipo = Equipos.ip ) AND ip_acceso.ip = Equipos.ip AND ip_acceso.acceso <> $acceso",
                                    { 'acceso': acceso,
                                      'grupo' : grupo,
                                    }
                                )
                for e in equipos:
                    db.query("UPDATE ip_acceso SET acceso = $acceso WHERE ip = $ip",
                                { 'acceso': acceso,
                                  'ip'    : e.IP,
                                }
                             )
                raise web.seeother('/../grupo/' + str(grupo))
            except:
                data = [ "Error", "No se encuentra el equipo en el sistema", "/../grupos", 5 ]
                return render.mensaje_sistema(data)

class equipo:
    def GET(self, ip=0, acceso=0):
        checkaccess()
        if acceso == 0:
            # es sólo display
            try:
                equipo = db.query("SELECT Equipos.*, ip_acceso.acceso FROM Equipos, ip_acceso WHERE Equipos.IP = $ip AND ip_acceso.ip = Equipos.IP",
                                   { 'ip': ip
                                    }
                                   )[0]
                pagina = { 'header'    : headers.standard(),
                            'menues'    : menues.mostrar("Equipos"),
                           'footer'    : footers.standard()
                         }
                return render.equipo(pagina, equipo)
            except:
                data = [ "Error", "No se encuentra el equipo en el sistema", "/../equipos", 5 ]
                return render.mensaje_sistema(data)
        else:
            db.query("UPDATE ip_acceso SET acceso = $acceso WHERE ip = $ip",
                        { 'acceso': acceso,
                          'ip'    : ip,
                        }
                     )
        raise web.seeother('/../equipo/' + str(ip))
    
class equipos:
    '''
    Formulario para seleccionar y luego mostrar un equipo
    '''
    def GET(self):
        checkaccess()
        #web.header("Content-Type", "text/html; charset=iso-8859-1") 
        equipos = db.query('SELECT * FROM Equipos ORDER BY Puesto, IP, MAC')
        pagina = { 'header'    : headers.standard(),
                   'menues'    : menues.mostrar("Equipos", "Mostrar"),
                   'footer'    : footers.standard()
                 }
        return render.seleccionar_equipo(pagina, "equipos", equipos)


    def POST(self):
        checkaccess()
        #web.header("Content-Type", "text/html; charset=iso-8859-1") 
        i = web.input()
        raise web.seeother('/../equipo/' + str(i.equipo))
    
class grupos:
    '''
    Formulario para seleccionar y luego mostrar un grupo
    '''
    def GET(self):
        checkaccess()
        #web.header("Content-Type", "text/html; charset=iso-8859-1") 
        grupos = db.query('SELECT * FROM Grupos ORDER BY descripcion')
        pagina = { 'header'    : headers.standard(),
                   'menues'    : menues.mostrar("Grupos", "Mostrar"),
                   'footer'    : footers.standard()
                 }
        return render.seleccionar_grupo(pagina, "grupos", grupos)


    def POST(self):
        checkaccess()
        #web.header("Content-Type", "text/html; charset=iso-8859-1") 
        i = web.input()
        raise web.seeother('/../grupo/' + str(i.grupo))

class herramientas:
    def GET(self):
        data = [ "Denied", "Usted no tiene acceso a esta opción del sistema", "/../", 5 ]
        return render.mensaje_sistema(data)
#
## MIDDLEWARE FACTORIES
#        

#wsgi
def session_mw(app):
    date_now = datetime.datetime.now()
    expiration_period = datetime.datetime(date_now.year + 1, date_now.month%12 + 1,  date_now.day%28 + 1,  date_now.hour, date_now.minute)
    return SessionMiddleware(app, key = "proxy_access", cookie_expires = expiration_period, secret='kasjhqdkajshdks') 


#DataBase
db = web.database(
                    dbn=config.get("Database","dbn"),
                    user=config.get("Database","user"),
                    pw=config.get("Database","password"),
                    db=config.get("Database","db"),
                    host=config.get("Database","host")
                  )

#
## RUN APPLICATION
#    
#web.wsgi.runwsgi = lambda func, addr=None: web.wsgi.runfcgi(func, addr)
#web.webapi.internalerror = web.debugerror

# Check and enable debugging
if config.get("System","debug"):
    web.config.debug = True
else:
    web.config.debug = False

app = web.application(urls, globals(), autoreload=True)

#para WSGI
application = session_mw(app.wsgifunc()) 
