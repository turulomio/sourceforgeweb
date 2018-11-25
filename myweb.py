#!/usr/bin/python3
import argparse
import os
import datetime
import shutil
import gettext
import codecs
import sys

gettext.install('myweb', 'po/locale')
class SetCommons:
    def __init__(self):
        self.arr=[]

    def append(self, o):
        self.arr.append(o)
        
    def length(self):
        return len(self.arr)



class Screenshot:
    def __init__(self, title, file, dt, width=100):
        self.title=title
        self.file=file
        self.datetime=dt
        self.width=width
        
    def html(self):
        return '<img src="{}" width="{}%" align="middle" border="1" title="{}. {}"><p>\n'.format(self.file, self.width, self.datetime, self.title)


class SetScreenshots(SetCommons):
    def __init__(self):
        SetCommons.__init__(self)
    def sort(self):
        self.arr=sorted(self.arr, key=lambda s: s.datetime,  reverse=True) 

class SetDistFiles(SetCommons):
    def __init__(self):
        SetCommons.__init__(self)
        
    def find(self, sourcecode, so):
        for d in self.arr:
            if d.sourcecode==sourcecode and  d.so==so:
                return d
        return None

class DistFile:
    def __init__(self, sourcecode, so, path):
        self.sourcecode=sourcecode#src or bin
        self.so=so #"Windows or Linux"
        self.path=path

class Release:
    def __init__(self,  dt,  version, subversion):
        self.datetime=dt
        self.subversion=subversion
        self.version=version
        self.distfiles=SetDistFiles()
        
    def appendDistfile(self, distfile):
        self.distfiles.append(distfile)

    def html(self):
        body=""
        body=body+'    <tr>\n'
        body=body+'        <td><center>'+str(self.datetime)[:16]+'</center></td>\n'
        body=body+'        <td><center>'+_('Versión {}').format(self.version)+'</center></td>\n'
        body=body+'        <td><center>r{}</center></td>\n'.format(self.subversion)
            
        body=body+"<td><center>"
        
        d=self.distfiles.find(True,"Linux")
        if d!=None:
            body=body+'<a href="{}"><img src="images/linux.png" height="36"></a>'.format(d.path)
        d=self.distfiles.find(True,"Windows")
        if d!=None:
            body=body+'<a href="{}"><img src="images/windows.png" height="36"></a>'.format(d.path)
        body=body+"</center></td><td><center>"
        d=self.distfiles.find(False,"Linux")
        if d!=None:
            body=body+'<a href="{}"><img src="images/linux.png" height="36"></a>'.format(d.path)
        d=self.distfiles.find(False,"Windows")
        if d!=None:
            body=body+'<a href="{}"><img src="images/windows.png" height="36"></a>'.format(d.path)
        body=body+'</center></td>\n'
        body=body+'    </tr>\n'
        return body
        
    ##Date string from self.datetime and without -
    def date_linux(self):
        return str(self.datetime.date()).replace("-", "")
        
    ##Date string from self.datetime for windows versions
    def date_windows(self):
        return "{}.{}.{}".format(self.datetime.year, self.datetime.month, self.datetime.day)


class SetPages:
    def __init__(self,  output, language, projects):
        self.projects=projects
        self.output=output
        self.language=language

    def write(self):
        self.Index()
        self.QuienSoy()
        self.Proyectos()

    def Index(self):
        self.pagina_proyectos("index.html")
    
    def pagina_proyectos(self, page):
        p=Page("Página principal de Turulomio", page)
        body='<h1>'+_('Mis proyectos')+'</h1>\n'
        body=body+ _('Todos mis proyectos de código abierto los puedes encontrar en el <a href="https://github.com/Turulomio?tab=repositories">Repositorio de GITHUB</a>.<p>')
        body=body+ _('De entre ellos destacan:')+'\n'
        body=body+ '<ul>\n'
        body=body+ '   <li><a href="https://github.com/Turulomio/devicesinlan">DevicesInLan</a></li>\n'
        body=body+ '   <li><a href="https://github.com/Turulomio/didyoureadme">DidYouReadMe</a></li>\n'
        body=body+ '   <li><a href="https://github.com/Turulomio/glparchis">glParchis</a></li>\n'
        body=body+ '   <li><a href="https://github.com/Turulomio/kdepim2google">Kdepim2google</a></li>\n'
        body=body+ '   <li><a href="https://github.com/Turulomio/recovermypartition">RecoverMyPartition</a></li>\n'
        body=body+ '   <li><a href="https://github.com/Turulomio/xulpymoney">Xulpymoney</a></li>\n'
        body=body+ '   <li><a href="https://github.com/Turulomio/mangenerator/">ManGenerator</a></li>\n'
        body=body+ '   <li><a href="https://github.com/Turulomio/officegenerator/">OfficeGenerator</a></li>\n'
        body=body+ '   <li><a href="https://github.com/Turulomio/recpermissions/">RecPermissions</a></li>\n'
        body=body+ '   <li><a href="https://github.com/Turulomio/toomanyfiles/">Too many files</a></li>\n'
        body=body+ '   <li><a href="https://github.com/Turulomio/ttyrecgenerator/">TtyRecGenerator</a></li>\n'
        body=body+ '   <li></li>\n'
        body=body+ '</ul>\n'
        p.write(body)

        body=body+ _('También participo o he participado en otros proyectos como:')+'\n'
        body=body+ '<ul>\n'
        body=body+ '   <li><a href="http://www.navit-project.org/">Navit</a></li>\n'
        body=body+ '   <li><a href="https://www.openstreetmap.org">OpenStreetMap</a></li>\n'
        body=body+ '</ul>\n'
        p.write(body)

    def QuienSoy(self):
        p=Page(_("¿Quién soy?"), 'quiensoy.html')
        body="<h1>{}</h1>".format(_("¿Quién soy?"))
        body=body+ _('Trabajo en las tecnologías de la información en una empresa informática desde 1998.')+'<p>\n'
        body=body+ _('Tuve mi primer contacto con el Sistema Operativo Linux en el año 1999 y desde entonces lo he usado constantemente como administrador, desarrollador y usuario.')+' <p>\n'
        body=body+ _("He utilizado muchas distribuciones Linux, Red Hat, Mandrake, Suse, Ubuntu, Kubuntu, Debian.., pero ninguna me satisfizo completamente hasta que probe Gentoo. Llevo usándola desde el 2003 como desktop y server, con total satisfacción.")+" <p>\n"
        body=body+ _('Tengo mi propio portage que puedes encontar en')+' <a href="https://github.com/Turulomio/myportage">GitHub</a><p>\n'
        body=body+ _('Además pondré en esta página web todo tipo de noticias de interés general, relacionados con mis hobbies, la lectura, la ciencia, etcétera.')+'<p>\n'
        p.write(body)


    def Proyectos(self):
        self.pagina_proyectos("proyectos.html")

class SetProjects(SetCommons):
    def __init__(self, output, language):
        SetCommons.__init__(self)
        self.output=output
        self.language=language
        
    def write(self):
        self.kdepim2google()
        self.glparchis()
        self.didyoureadme()
        self.recovermypartition()
        self.spoken_uptime()
        self.devicesinlan()
        
    def kdepim2google(self):
        def installation():
            s="<h3>"+_("Antes de la instalación")+"</h3>"
            s=s+_("Antes de la instalación debo tener instaladas de las siguientas herramientas:")
            s=s+"<ul>"
            s=s+"<li>" +_("Gcc: Compilador")+"</li>"
            s=s+"<li>" +_("Cmake: Utilidades de compilación")+"</li>"
            s=s+"<li>" +_("QtCore: Librerías de programación")+"</li>"
            s=s+"</ul>"
            s=s+"<h3>"+_("Instalación")+"</h3>"
            s=s+_("Para la instalación del programa realizaré lo siguiente:")
            s=s+"<ol>"
            s=s+"<li>"+_("Descagaré la última versión del programa y la descomprimiré")+"</li>"
            s=s+"<li>"+_("Entro en el directorio creado al descomprimir y creo la carpeta build con #mkdir build")+"</li>"
            s=s+"<li>"+_("Entro en el directorio build y ejecuto #cmake .. ")+"</li>"
            s=s+"<li>"+_("Ejecuto make y make install (por defecto se instala en /usr/local/) ")+"</li>"
            s=s+"</ol>"
            p.installation=s

        def releases():
            p.releases.append(Release(datetime.datetime(2014,9,1,17,0),"0.1.1",3))
            p.releases.append(Release(datetime.datetime(2014,9,4,6,0),"0.2.0",11))

            r=Release(datetime.datetime(2014,9,11,6,0),"0.3.0", 15)
            r.appendDistfile(DistFile(True, "Linux", "https://sourceforge.net/projects/kdepim2google/files/kdepim2google/0.3.0/kdepim2google-src-0.3.0.tar.gz/download" ))
            r.appendDistfile(DistFile(True, "Windows", "https://sourceforge.net/projects/kdepim2google/files/kdepim2google/0.3.0/kdepim2google-src-0.3.0.tar.gz/download" ))
            p.releases.append(r)

            r=Release(datetime.datetime(2014,9,17,6,0),"0.4.0", 17)
            r.appendDistfile(DistFile(True, "Linux", "https://sourceforge.net/projects/kdepim2google/files/kdepim2google/0.4.0/kdepim2google-src-0.4.0.tar.gz/download" ))
            r.appendDistfile(DistFile(True, "Windows", "https://sourceforge.net/projects/kdepim2google/files/kdepim2google/0.4.0/kdepim2google-src-0.4.0.tar.gz/download" ))
            p.releases.append(r)
            
            r=Release(datetime.datetime(2014,12,30,19,25),"0.5.0", 18)
            r.appendDistfile(DistFile(True, "Linux", "https://sourceforge.net/projects/kdepim2google/files/kdepim2google/0.5.0/kdepim2google-src-0.5.0.tar.gz/download" ))
            r.appendDistfile(DistFile(True, "Windows", "https://sourceforge.net/projects/kdepim2google/files/kdepim2google/0.5.0/kdepim2google-src-0.5.0.tar.gz/download" ))
            p.releases.append(r)            

        def news():
            p.news.append(News(datetime.datetime(2014,9,1,17,00),
                                                   _("Proyecto Kdepim2Google"), 
                                                   p.htmlImage(), 
                                                   _("""Primera versión de estas utilidades de integración de Kdepim en Google""")))

            p.news.append(News(datetime.datetime(2014,9,11,6,0),
                                                   _("Proyecto Kdepim2Google. Nueva versión {}").format("0.3.0"),
                                                   p.htmlImage(), 
                                                   _("""Nueva versión de estas utilidades de integración de Kdepim en Google. Se han realizado los siguientes cambios:
            <ul>
              <li>Se han arreglado los contadores de contactos</li>
              <li>Se ha mejorado la búsqueda de la cadena 'Ocultar cumpleaños'</li>
              <li>Se ha mejorado la ayuda del programa</li>
            </ul>""")))

            p.news.append(News(datetime.datetime(2014,9,17,6,0),
                                                   _("Proyecto Kdepim2Google. Nueva versión {}").format("0.4.0"), 
                                                   p.htmlImage(), 
                                                   _("""Nueva versión de estas utilidades de integración de Kdepim en Google. Se han realizado los siguientes cambios:
            <ul>
              <li>Arreglado error en la traducción española</li>
            </ul>""")))
            p.news.append(News(datetime.datetime(2014,12,30,19,25),
                                                   _("Proyecto Kdepim2Google. Nueva versión {}").format("0.5.0"), 
                                                   p.htmlImage(), 
                                                   _("""Nueva versión de estas utilidades de integración de Kdepim en Google. Se han realizado los siguientes cambios:
            <ul>
              <li>Para extraer el nombre del contacto, ahora busca también en N:</li>
            </ul>""")))
        ##############################
        p=Project("kdepim2google", "Kdepim2Google", "images/google.png", "app-misc/kdepim2google")
        p.brief=_('Utilidades de integración entre Kdepim y Google')
        news()
        releases()
        installation()
        p.writePage()
        self.append(p)

    def didyoureadme(self):
        def screenshots():
            p.screenshots.append(Screenshot("", "images/didyoureadme-20121220-screenshot.2.png",  datetime.datetime(2012, 12, 20), 40))
            p.screenshots.append(Screenshot("", "images/didyoureadme-20121220-screenshot.3.png",  datetime.datetime(2012, 12, 20), 60))
            p.screenshots.append(Screenshot("", "images/didyoureadme-20160521-screenshot.1.png",  datetime.datetime(2016, 5, 21), 60))

        def releases():
            r=Release(datetime.datetime(2014,1,28,6,0),"20140128", 43)
            r.appendDistfile(DistFile(True, "Linux", "http://sourceforge.net/projects/didyoureadme/files/didyoureadme/didyoureadme-20140128/didyoureadme-src-linux-20140128.tar.gz/download" ))
            r.appendDistfile(DistFile(False, "Linux", "http://sourceforge.net/projects/didyoureadme/files/didyoureadme/didyoureadme-20140128/didyoureadme-bin-linux-20140128.tar.gz/download" ))
            p.releases.append(r)
            
            r=Release(datetime.datetime(2015,1,28,6,0),"20150128", 58)
            r.appendDistfile(DistFile(True, "Linux", "http://sourceforge.net/projects/didyoureadme/files/didyoureadme/didyoureadme-20150128/didyoureadme-src-linux-20150128.tar.gz/download" ))
            r.appendDistfile(DistFile(False, "Linux", "http://sourceforge.net/projects/didyoureadme/files/didyoureadme/didyoureadme-20150128/didyoureadme-bin-linux-20150128.tar.gz/download" ))
            p.releases.append(r)
            
            r=Release(datetime.datetime(2016,5,21,8,0),"20160521", 103)
            r.appendDistfile(DistFile(True, "Linux", "http://sourceforge.net/projects/didyoureadme/files/didyoureadme/didyoureadme-20150128/didyoureadme-src-linux-20150128.tar.gz/download" ))
            r.appendDistfile(DistFile(False, "Linux", "http://sourceforge.net/projects/didyoureadme/files/didyoureadme/didyoureadme-20150128/didyoureadme-bin-linux-20150128.tar.gz/download" ))
            p.releases.append(r)
            
        def news():    
            p.news.append(News(datetime.datetime(2012,12,21,12,12), 
                                                   _("Proyecto DidYouReadMe"), 
                                                   p.htmlImage(), 
                                                   _("Se ha publicado el código completamente funcional en el subversión del nuevo proyecto DidYouReadMe.")+" "+_("Es un programa que envía correo a una serie de usuarios controlando el envío y la recepción de los mismos.")))        
                        
            p.news.append(News(datetime.datetime(2013,1,8,11,12), 
                                                   _("Proyecto DidYouReadMe. Versión")+" 20130108", 
                                                   p.htmlImage(), 
                                                   _("Se ha publicado la primera versión de DidYouReadMe.")))
                                                   
            p.news.append(News(datetime.datetime(2013,1,14,14,12), 
                                                   _("Proyecto DidYouReadMe. Versión")+" 20130114", 
                                                   p.htmlImage(), 
                                                   _("Nueva versión. Se ha mejorada la visualización de ficheros y la edición de comentarios de los documentos.")))
                        
            p.news.append(News(datetime.datetime(2013,1,16,12,12), 
                                                   _("Proyecto DidYouReadMe. Versión")+" 20130116", 
                                                   p.htmlImage(), 
                                                   _("""Nueva versión. Se han realizado los siguientes cambios:
<ul>
  <li>Añadido soporte de backup del sistema.</li>
  <li>Corregido bug importante al mandar correos sin comentario.</li>
</ul>
""")))

            p.news.append(News(datetime.datetime(2013,2,8,16,00), 
                                                   _("Proyecto DidYouReadMe. Versión")+" 20130208", 
                                                   p.htmlImage(), 
                                                   _("""Nueva versión. Se han realizado los siguientes cambios:
<ul>
  <li>Se han cambiado los combos de grupo y usuarios por listas, mejorando el interfaz de usuario</li>
  <li>frmMain ahora actualiza las tablas automáticamente</li>
  <li>Se ha quitado bottle.py del proyecto, se debe usar el packete bottle de tu distribución</li>
  <li>Al añadir un documento ahora se comprueba si el fichero seleccionado existe y es un fichero</li>
  <li>Se ha mejorado el interfaz de usuario</li>
</ul>
""")))

            p.news.append(News(datetime.datetime(2013,7,10,9,40), 
                                                   _("Proyecto DidYouReadMe. Versión")+" 20130710", 
                                                   p.htmlImage(), 
                                                   _("""Nueva versión. Se han realizado los siguientes cambios:
<ul>
  <li>Solucionado error al cambiar el puerto del servidor web</li>
  <li>El correo muestra la fecha y hora en formato internacional</li>
  <li>Se ha añadido un selector por meses para mostrar documentos cerrados</li>
  <li>Ahora no recorta los datetimes con 00 segundos</li>
  <li>Ahora members es un set, no un list</li>
</ul>
""")))

            p.news.append(News(datetime.datetime(2013,7,11,9,0), 
                                                   _("Proyecto DidYouReadMe. Versión")+" 20130711", 
                                                   p.htmlImage(), 
                                                   _("""Nueva versión. Se han realizado los siguientes cambios:
<ul>
  <li>Solucionado error al poner el día de la semana en el contenido del correo</li>
</ul>
""")))

            p.news.append(News(datetime.datetime(2014,1,28,9,0), 
                                                   _("Proyecto DidYouReadMe. Versión")+" 20140128", 
                                                   p.htmlImage(), 
                                                   _("""Nueva versión. Se han realizado los siguientes cambios:
<ul>
  <li>Solucionado error con las fechas de los correos</li>
  <li>Añadida opción de actualizar tablas automaticamente en frmSettings</li>
  <li>Los informes muestran ahora el identificador interno del documento</li>
</ul>
""")))

            p.news.append(News(datetime.datetime(2015,1,28,6,0), 
                                                   _("Proyecto DidYouReadMe. Versión")+" 20150128", 
                                                   p.htmlImage(), 
                                                   _("""Nueva versión. Se han realizado los siguientes cambios:
<ul>
  <li>Añadida vigencia a los documentos</li>
  <li>Los documentos se almacenan ahora dentro de la base de datos</li>
  <li>Mejorada la reutilización de código</li>
  <li>Ahora puede borrar documentos en el modo administrador</li>
</ul>
""")))



            p.news.append(News(datetime.datetime(2016,5,21,9,0), 
                                                   _("Proyecto DidYouReadMe. Versión")+" 20160521", 
                                                   p.htmlImage(), 
                                                   _("""Nueva versión. Se han realizado los siguientes cambios:
<ul>
  <li>Se ha portado a Windows de 32 y 64 bits</li>
  <li>Muchos cambios</li>
</ul>
""")))
        ##############################
        p=Project("didyoureadme", "DidYouReadMe", "images/noticia.jpg",  "app-office/didyoureadme")
        p.brief=_('Programa que envía correo a una serie de usuarios controlando el envío y la recepción de los mismos.')

        news()
        releases()
        screenshots()
        p.writePage()
        self.append(p)
        
    def glparchis(self):
        def screenshots():
            p.screenshots.append(Screenshot("", "images/glparchis-20120921-screenshot.1.png",  datetime.datetime(2012, 9, 21), 100))
            p.screenshots.append(Screenshot("", "images/glparchis-20120910-screenshot.1.png",  datetime.datetime(2012, 9, 10), 60))
            p.screenshots.append(Screenshot("", "images/glparchis-20120910-screenshot.2.png",  datetime.datetime(2012, 9, 10), 100))
            p.screenshots.append(Screenshot("", "images/glparchis-20120917-screenshot.1.png",  datetime.datetime(2012, 9, 17), 35))
            p.screenshots.append(Screenshot("", "images/glparchis-20120917-screenshot.2.png",  datetime.datetime(2012, 9, 17), 50))
            p.screenshots.append(Screenshot("", "images/glparchis-20180510-screenshot.4.png",  datetime.datetime(2018, 5, 10), 50))
            p.screenshots.append(Screenshot("", "images/glparchis-20180510-screenshot.3.png",  datetime.datetime(2018, 5, 10), 50))
            p.screenshots.append(Screenshot("", "images/glparchis-20180510-screenshot.2.png",  datetime.datetime(2018, 5, 10), 50))
            p.screenshots.append(Screenshot("", "images/glparchis-20180510-screenshot.1.png",  datetime.datetime(2018, 5, 10), 50))
            
        def releases():
            r=Release(datetime.datetime(2013,7,16,6,0),"20130716", 341)
            r.appendDistfile(DistFile(True, "Linux", "http://sourceforge.net/projects/glparchis/files/glparchis/glparchis-20130716/glparchis-src-linux-20130716.tar.gz/download" ))
            r.appendDistfile(DistFile(True, "Windows", "http://sourceforge.net/projects/glparchis/files/glparchis/glparchis-20130716/glparchis-src-windows-20130716.zip/download" ))
            r.appendDistfile(DistFile(False, "Linux", "http://sourceforge.net/projects/glparchis/files/glparchis/glparchis-20130716/glparchis-bin-linux-20130716.tar.gz/download" ))
            r.appendDistfile(DistFile(False, "Windows", "http://sourceforge.net/projects/glparchis/files/glparchis/glparchis-20130716/glparchis-bin-windows-20130716.exe/download" ))
            r=Release(datetime.datetime(2016,3,25,12,0),"20160325", 382)
            r.appendDistfile(DistFile(True, "Linux", "http://sourceforge.net/projects/glparchis/files/glparchis/glparchis-20160325/glparchis-src-20160325.tar.gz/download" ))
            r.appendDistfile(DistFile(False, "Linux", "http://sourceforge.net/projects/glparchis/files/glparchis/glparchis-20160325/glparchis-linux-20160325.x86_64.tar.gz/download" ))
            r.appendDistfile(DistFile(False, "Windows", "http://sourceforge.net/projects/glparchis/files/glparchis/glparchis-20160325/glparchis-windows-20160325.amd64.exe/download" ))
            p.releases.append(r)
            r=Release(datetime.datetime(2016,6,23,0,0),"20160623", 392)
            r.appendDistfile(DistFile(True, "Linux", "http://sourceforge.net/projects/glparchis/files/glparchis/glparchis-20160623/glparchis-src-20160623.tar.gz/download" ))
            r.appendDistfile(DistFile(False, "Linux", "http://sourceforge.net/projects/glparchis/files/glparchis/glparchis-20160623/glparchis-linux-20160623.x86_64.tar.gz/download" ))
            r.appendDistfile(DistFile(False, "Windows", "http://sourceforge.net/projects/glparchis/files/glparchis/glparchis-20160623/glparchis-windows-20160623.amd64.exe/download" ))
            p.releases.append(r)
            r=Release(datetime.datetime(2016,8,1,19,0),"20160801", 396)
            r.appendDistfile(DistFile(True, "Linux", "http://sourceforge.net/projects/glparchis/files/glparchis/glparchis-20160801/glparchis-src-20160801.tar.gz/download" ))
            r.appendDistfile(DistFile(False, "Linux", "http://sourceforge.net/projects/glparchis/files/glparchis/glparchis-20160801/glparchis-linux-20160801.x86_64.tar.gz/download" ))
            r.appendDistfile(DistFile(False, "Windows", "http://sourceforge.net/projects/glparchis/files/glparchis/glparchis-20160801/glparchis-windows-20160801.amd64.exe/download" ))
            p.releases.append(r)
            r=Release(datetime.datetime(2016,8,12,18,30),"20160812", 402)
            r.appendDistfile(DistFile(True, "Linux", "http://sourceforge.net/projects/glparchis/files/glparchis/glparchis-20160812/glparchis-src-20160812.tar.gz/download" ))
            r.appendDistfile(DistFile(False, "Linux", "http://sourceforge.net/projects/glparchis/files/glparchis/glparchis-20160812/glparchis-linux-20160812.x86_64.tar.gz/download" ))
            r.appendDistfile(DistFile(False, "Windows", "http://sourceforge.net/projects/glparchis/files/glparchis/glparchis-20160812/glparchis-windows-20160812.amd64.exe/download" ))
            p.releases.append(r)
            r=Release(datetime.datetime(2017,7,26,5,30),"20170726", 432)
            r.appendDistfile(DistFile(True, "Linux", "http://sourceforge.net/projects/glparchis/files/glparchis/glparchis-20170726/glparchis-20170726.tar.gz/download" ))
            r.appendDistfile(DistFile(False, "Linux", "http://sourceforge.net/projects/glparchis/files/glparchis/glparchis-20170726/glparchis-linux-20170726.x86_64.tar.gz/download" ))
            r.appendDistfile(DistFile(False, "Windows", "http://sourceforge.net/projects/glparchis/files/glparchis/glparchis-20170726/glparchis-2017.7.26-amd64.msi/download" ))
            p.releases.append(r)
            r=Release(datetime.datetime(2018,3,7,18,50),"20180307", 442)
            r.appendDistfile(DistFile(True, "Linux", "http://sourceforge.net/projects/glparchis/files/glparchis/glparchis-20180307/glparchis-20180307.tar.gz/download" ))
            r.appendDistfile(DistFile(False, "Linux", "http://sourceforge.net/projects/glparchis/files/glparchis/glparchis-20180307/glparchis-linux-20180307.x86_64.tar.gz/download" ))
            r.appendDistfile(DistFile(False, "Windows", "http://sourceforge.net/projects/glparchis/files/glparchis/glparchis-20180307/glparchis-2018.3.7-amd64.msi/download" ))
            p.releases.append(r)
            r=Release(datetime.datetime(2018,3,8,18,50),"20180308", 443)
            r.appendDistfile(DistFile(True, "Linux", "http://sourceforge.net/projects/glparchis/files/glparchis/glparchis-20180308/glparchis-20180308.tar.gz/download" ))
            r.appendDistfile(DistFile(False, "Linux", "http://sourceforge.net/projects/glparchis/files/glparchis/glparchis-20180308/glparchis-linux-20180308.x86_64.tar.gz/download" ))
            r.appendDistfile(DistFile(False, "Windows", "http://sourceforge.net/projects/glparchis/files/glparchis/glparchis-20180308/glparchis-2018.3.8-amd64.msi/download" ))
            p.releases.append(r)
            r=Release(datetime.datetime(2018,4,16,18,50), "20180416", 466)
            r.appendDistfile(DistFile(True, "Linux", "http://sourceforge.net/projects/glparchis/files/glparchis/glparchis-{0}/glparchis-{0}.tar.gz/download".format(r.date_linux())))
            r.appendDistfile(DistFile(False, "Linux", "http://sourceforge.net/projects/glparchis/files/glparchis/glparchis-{0}/glparchis-linux-{0}.x86_64.tar.gz/download".format(r.date_linux())))
            r.appendDistfile(DistFile(False, "Windows", "http://sourceforge.net/projects/glparchis/files/glparchis/glparchis-{0}/glparchis-{1}-amd64.msi/download".format(r.date_linux(), r.date_windows())))
            p.releases.append(r)
            r=Release(datetime.datetime(2018,5,10,5,0), "20180510", 489)
            r.appendDistfile(DistFile(True, "Linux", "http://sourceforge.net/projects/glparchis/files/glparchis/glparchis-{0}/glparchis-{0}.tar.gz/download".format(r.date_linux())))
            r.appendDistfile(DistFile(False, "Linux", "http://sourceforge.net/projects/glparchis/files/glparchis/glparchis-{0}/glparchis-linux-{0}.x86_64.tar.gz/download".format(r.date_linux())))
            r.appendDistfile(DistFile(False, "Windows", "http://sourceforge.net/projects/glparchis/files/glparchis/glparchis-{0}/glparchis-{1}-amd64.msi/download".format(r.date_linux(), r.date_windows())))
            p.releases.append(r)
            r=Release(datetime.datetime(2018,10,20,12,0), "20181020", 499)
            r.appendDistfile(DistFile(True, "Linux", "http://sourceforge.net/projects/glparchis/files/glparchis/glparchis-{0}/glparchis-{0}.tar.gz/download".format(r.date_linux())))
            r.appendDistfile(DistFile(False, "Linux", "http://sourceforge.net/projects/glparchis/files/glparchis/glparchis-{0}/glparchis-linux-{0}.x86_64.tar.gz/download".format(r.date_linux())))
            r.appendDistfile(DistFile(False, "Windows", "http://sourceforge.net/projects/glparchis/files/glparchis/glparchis-{0}/glparchis-{1}-amd64.msi/download".format(r.date_linux(), r.date_windows())))
            p.releases.append(r)
        def news():    
            p.news.append(News(datetime.datetime(2010,3,14,10,27), 
                                                   _("Publicación del proyecto glParchis"), 
                                                   p.htmlImage(), 
                                                   _("He integrado en mi página personal el proyecto glParchis")))        
            
            p.news.append(News(datetime.datetime(2012,9,2,10,0), 
                                                    _("Proyecto glParchis. Versión")+" 20120902", 
                                                   p.htmlImage(), 
                                                    _("Nueva versión basada en PyQt y opengl. Funciona para con varios usuarios. La inteligencia artificial debe ser mejorada")))
                                                    

            p.news.append(News(datetime.datetime(2012,9,10,23,0), 
                                                    _("Proyecto glParchis. Versión")+" 20120910", 
                                                    p.htmlImage(), 
                                                    _("Nueva versión con inteligencia artificial y corrigiendo numerosos bugs")))

            p.news.append(News(datetime.datetime(2012,9,14,17,0), 
                                                    _("Proyecto glParchis. Versión")+" 20120914", 
                                                    p.htmlImage(), 
                                                    _("Sale la primera versión para el sistema operativo Windows. Además se corrigen varios errores")))

            p.news.append(News(datetime.datetime(2012,9,17,16,10), 
                                                    _("Proyecto glParchis. Versión")+" 20120917", 
                                                    p.htmlImage(), 
                                                    _("Nueva versión con grandes mejoras en internacionalización y estabilidad del programa.")))

            p.news.append(News(datetime.datetime(2012,9,21,19,5), 
                                                    _("Proyecto glParchis. Versión")+" 20120921", 
                                                    p.htmlImage(), 
                                                    _("Nueva versión con nuevos sonidos y texturas.")))

            p.news.append(News(datetime.datetime(2013,2,28,21,00), 
                                                    _("Proyecto glParchis. Versión")+" 20130228", 
                                                    p.htmlImage(), 
                                                    _("""Nueva versión. Se han realizado los siguientes cambios:
<ul>
  <li>Añadido soporte para mejores puntuaciones y estadísticas</li>
  <li>Ahora pueden jugar 6 y 8 jugadores</li>
</ul>
""")))
            
            p.news.append(News(datetime.datetime(2013,7,16,16,10), 
                                                    _("Proyecto glParchis. Versión")+" 20130716", 
                                                    p.htmlImage(), 
                                                    _("""Nueva versión. Se han realizado los siguientes cambios:
<ul>
  <li>Cuando se come una ficha en la casilla de salida, esta ficha es la última en llegar si son dos distintas al color de la casilla</li>
  <li>Cambiado el pink por el fuchsia, el cyan por darkturquoise y el orange por darkorange en colores web. </li>
  <li>Se ha añadido compatibilidad con los highscores que usaban los antiguos</li>
  <li>Se ha añadido soporte para autoguardado</li>
  <li>Mejorado el interfaz de usuario</li>
  <li>Solucionado error al cerrar la aplicación</li>
  <li>Añadida opción de que el panel de usuario siga al jugador actual o no</li>
  <li>Al guardar la partida se graba, el tiempo de inicio y el número de fichas comidas.</li>
  <li>Se ha migrado a python3, yo lo he testeado con python 3.3</li>
</ul>
""")))

            p.news.append(News(datetime.datetime(2013,7,13,19,00), 
                                                    _("Proyecto glParchis. Referencias en revistas"), 
                                                    p.htmlImage(), 
                                                    _("""Hoy he estado surfeando por la web y me encontré con un artículo de una revista digital cubana de software libre <a href="http://gutl.jovenclub.cu/swl-x/">SWL-X</a> con un artículo de glParchis. La revista te la puedes bajar en el siguiente <a href="http://gutl.jovenclub.cu/wp-content/ftp/ftp-gutl/docs/revistas/swl-x/swlx2.pdf">enlace</a>. Gracias por dar publicidad al proyecto y un saludo""")))

            p.news.append(News(datetime.datetime(2016,3,25,12,00), 
                                                    _("Proyecto glParchis. Versión")+" 20160325", 
                                                    p.htmlImage(), 
                                                    _("""Hoy he publicado una nueva versión de glParchis, después de dos años, con los siguientes cambios:
<ul>
<li>La configuración del sonido se graba ahora en glparchis.cfg</li>
<li>Se ha cambiado el makefile para que se compile con make y se instale con make install</li>
<li>Ya no se van a distribuir los sources de windows</li>
<li>Ahora se generan versiones de Windows de 32 bits y de 64 bits</li>
<li>Se ha eliminado el soporte para phonon, ahora se utiliza QMultimedia</li>
<li>Se ha migrado a PyQt5</li>
<li>Se ha añadido el modo de pantalla completa</li>
</ul>
  """)))          
  
            p.news.append(News(datetime.datetime(2016,6,23,9,00), 
                                                    _("Proyecto glParchis. Versión")+" 20160623", 
                                                    p.htmlImage(), 
                                                    _("""Hoy he publicado una nueva versión de glParchis con los siguientes cambios:
<ul>
    <li>Añadido el script project_i18n para traducir la documentación del proyecto</li>
    <li>Ahora el tablero rota por su centro pulsando la letra m</li>
    <li>Rendimiento mejorado</li>
    <li>Corregido error con el icono de fullscreen</li>
</ul>
  """)))
  
            p.news.append(News(datetime.datetime(2016,8,1,19,00), 
                                                    _("Proyecto glParchis. Versión")+" 20160801", 
                                                    p.htmlImage(), 
                                                    _("""Hoy he publicado una nueva versión de glParchis con los siguientes cambios:
<ul>
    <li>La configuración del splitter del juego se guarda ahora en pantalla normal y en pantalla completa</li>
</ul>
  """)))

            p.news.append(News(datetime.datetime(2016,8,12,18,30), 
                                                    _("Proyecto glParchis. Versión")+" 20160812", 
                                                    p.htmlImage(), 
                                                    _("""Hoy he publicado una nueva versión de glParchis con los siguientes cambios:
<ul>
    <li>El estado de pantalla completa se guarda en el fichero de configuración</li>
    <li>Añadido sistema de estadística en la base de datos de Sourceforge</li>
    <li>Añadida opción de no contribuir a la estadística mundial</li>
</ul>
  """)))
  
            p.news.append(News(datetime.datetime(2017,7,26,5,30), 
                                                    _("Proyecto glParchis. Versión")+" 20170726", 
                                                    p.htmlImage(), 
                                                    _("""Hoy he publicado una nueva versión de glParchis con los siguientes cambios:
<ul>
    <li>Añadida la opción de configuración de retraso entre movimientos</li>
    <li>Añadida la opción de configuración de nivel de dificultad</li>
    <li>Añadida la opción de subir y bajar el tablero en el eje z con las teclas + y -</li>
    <li>Añadidas estadísticas individuales de juego</li>
    <li>El distribuible de windows se ha cambiado por un msi. DESINSTALE EL ANTIGUO GLPARCHIS ANTES DE INSTALAR EL NUEVO</li>
</ul>
  """)))  
            p.news.append(News(datetime.datetime(2018,3,7,18,50), 
                                                    _("Proyecto glParchis. Versión")+" 20180307", 
                                                    p.htmlImage(), 
                                                    _("""Hoy he publicado una nueva versión de glParchis con los siguientes cambios:
<ul>
    <li>Ahora se puede tirar el dado pulsando ENTER</li>
    <li>Añadida la opción de acercar y alejar el tablero en el menú</li>
</ul>
  """)))
            p.news.append(News(datetime.datetime(2018,3,8,18,50), 
                                                    _("Proyecto glParchis. Versión")+" 20180308", 
                                                    p.htmlImage(), 
                                                    _("""Hoy he publicado una nueva versión de glParchis con los siguientes cambios:
<ul>
    <li>Linux: Solucionado error al cargar los ficheros de traducción</li>
</ul>
  """)))
            p.news.append(News(datetime.datetime(2018,4,16,18,50), 
                                                    _("Proyecto glParchis. Versión")+" 20180416", 
                                                    p.htmlImage(), 
                                                    _("""Hoy he publicado una nueva versión de glParchis con los siguientes cambios:
<ul>
    <li>Windows: Solucionado bug molesto. El usuario necesitaba hacer varios clicks para mover una ficha</li>
    <li>Mejorado el código de OpenGL y su documentación</li>
    <li>Añadido el sistema de documentación de Doxygen para desarrolladores</li>
    <li>Windows: Solucionado error al mostrar objetos en el menu Acerca De</li>
</ul>
  """)))
            p.news.append(News(datetime.datetime(2018,5,10,5,0), 
                                                    _("Proyecto glParchis. Versión")+" 20180510", 
                                                    p.htmlImage(), 
                                                    _("""Hoy he publicado una nueva versión de glParchis con los siguientes cambios:
<ul>
    <li>Añadido el modo de 3 jugadores</li>
    <li>Ahora puedes informar de errores desde glParchis</li>
</ul>
  """)))
            p.news.append(News(datetime.datetime(2018,10,20,5,0), 
                                                    _("Proyecto glParchis. Versión")+" 20181020", 
                                                    p.htmlImage(), 
                                                    _("""Hoy he publicado una nueva versión de glParchis con los siguientes cambios:
<ul>
    <li>Añadida acción para ocultar/mostrar el panel izquierdo</li>
    <li>Añadido el automatismo del dado</li>
    <li>Añadido automatismo a las fichas cuando solo se puede mover una</li>
</ul>
  """)))

        ##############################
        p=Project("glparchis", "glParchis", "images/parchis.png",  "games-board/glparchis")

        brief='   <p>'+_('Juego de parchís de código abierto. Su licencia es GPL. Esta desarrollado para Linux y Windows. Es una versión Beta. Si encuentras cualquier error no dudes en publicarlo en el foro o en ponerte en contacto conmigo')+'\n'
        brief=brief+'   <p>'+_('Se cambio el desarrollo desde C++ a python utilizando las librerías PyQt y pyopengl, a partir de la versión 20120902')+'<p>\n'
        brief=brief+'   <p>'+_('Puedes contribuir al mantenimiento de este proyecto haciendo una donación:')+' <a href="http://sourceforge.net/donate/index.php?group_id=158664"><img src="http://images.sourceforge.net/images/project-support.jpg" width="88" height="32" border="0" alt="Support This Project" /> </a>\n'
        brief=brief+'   <p>'+_('Puedes consultar las estadísticas de juego en este ') + ' <a href="http://glparchis.sourceforge.net/php/glparchis_statistics.php">'+_('enlace')+'</a>\n'
        p.brief=brief
        news()
        releases()
        screenshots()
        p.writePage()
        self.append(p)        

        
    def recovermypartition(self):      
        def screenshots():
            p.screenshots.append(Screenshot("", "images/recovermypartition-20100520-screenshot.1.png",  datetime.datetime(2010, 5, 20), 100))

        def releases():            
            r=Release(datetime.datetime(2010,5,21,6,0),"0.1", 8)
            r.appendDistfile(DistFile(True, "Linux", "http://sourceforge.net/projects/recovermypartit/files/recovermypartit/0.1/recovermypartit-0.1.tar.gz/download" ))
            p.releases.append(r)

            r=Release(datetime.datetime(2010,8,12,6,0),"0.2", 20)
            r.appendDistfile(DistFile(True, "Linux", "http://sourceforge.net/projects/recovermypartit/files/recovermypartit/0.2/recovermypartit-0.2.tar.gz/download" ))
            p.releases.append(r)

            r=Release(datetime.datetime(2014,9,12,6,0),"0.3", 34)
            r.appendDistfile(DistFile(True, "Linux", "http://sourceforge.net/projects/recovermypartit/files/recovermypartit/0.3/recovermypartit-0.3.tar.gz/download" ))
            p.releases.append(r)

            r=Release(datetime.datetime(2018,1,24,7,0),"0.4", 38)
            r.appendDistfile(DistFile(True, "Linux", "http://sourceforge.net/projects/recovermypartit/files/recovermypartit/{0}/recovermypartit-{0}.tar.gz/download".format(r.version)))
            p.releases.append(r)

        def news():            
            p.news.append(News(datetime.datetime(2010,3,13,15,37),
                                                   _("Proyecto RecoverMyPartition"), 
                                                   p.htmlImage(), 
                                                   _("""Se ha añadido un nuevo proyecto para recuperar una partición utilizando python y sleuthkit.""")))
            p.news.append(News(datetime.datetime(2010,8,12,19,00),
                                                   _("Proyecto RecoverMyPartition"), 
                                                   p.htmlImage(), 
                                                   _("""He publicado una nueva versión de este proyecto:
<p>Los cambios más importantes son:
<ul>
   <li>Solucionado error si no se declaraba --partition</li>
   <li>Se ha añadido soporte internacional para la documentación con omegat</li>
   <li>Se ha cambiado la forma interna del proyecto</li>
</ul>""")))
            p.news.append(News(datetime.datetime(2014,9,12,6,0),
                                                   _("Proyecto RecoverMyPartition"), 
                                                   p.htmlImage(), 
                                                   _("""Se ha publicado la versión 0.3 del proyecto que mejora el sistema de instalación y el de traducción.""")))
            p.news.append(News(datetime.datetime(2018,1,24,7,0),
                                                   _("Proyecto RecoverMyPartition"), 
                                                   p.htmlImage(), 
                                                   _("""Se ha publicado la versión 0.4 del proyecto que actualiza el código a PyQt5 y mejora el sistema de distribución.""")))

        ##############################
        p=Project("recovermypartit", "RecoverMyPartition", "images/forensics.png", "app-forensics/recovermypartition")
        p.brief=_('Programa de análisis forense para recuperar una partición')+'<p>\n'+_('Este programa surge de la necesidad de recuperar una partición rápidamente, incluyendo ficheros borrados y clusters sin asignar. Utiliza de backend a Sleuthkit. Es un programa en consola y tiene una gran velocidad.') + "\n"
        news()
        releases()
        screenshots()
        p.writePage()
        self.append(p)
        
    def spoken_uptime(self):      
        def screenshots():
            p.screenshots.append(Screenshot("", "images/spoken-uptime-20150329-screenshot.1.png",  datetime.datetime(2015, 3, 29), 70))

        def releases():            
            r=Release(datetime.datetime(2015,3,21,16,0),"0.1.0", 5)
            r.appendDistfile(DistFile(True, "Linux", "http://sourceforge.net/projects/spoken-uptime/files/spoken-uptime/0.1.0/spoken-uptime-0.1.0.tar.gz/download" ))
            p.releases.append(r)

        def news():            
            p.news.append(News(datetime.datetime(2015,3,21,16,0),
                                                   _("Proyecto Spoken-Uptime"), 
                                                   p.htmlImage(), 
                                                   _("""Se ha publicado una nueva versión:
<p>Los cambios más importantes son:
<ul>
   <li>Versión estable</li>
</ul>""")))
        p=Project("spoken-uptime", "Spoken-Uptime", "images/spoken-uptime.png", "sys-apps/spoken-uptime")
        p.brief=_('Spoken linux system uptime') + "\n"

    def devicesinlan(self):      
        def screenshots():
            p.screenshots.append(Screenshot("", "images/devicesinlan-20150519-screenshot.1.png",  datetime.datetime(2015, 5, 19), 60))

        def releases():            
            r=Release(datetime.datetime(2015,5,9,15,0),"0.1.0", 3)
            r.appendDistfile(DistFile(True, "Linux", "http://sourceforge.net/projects/devicesinlan/files/devicesinlan/0.1.0/devicesinlan-0.1.0.tar.gz/download" ))
            p.releases.append(r)
            r=Release(datetime.datetime(2015,5,9,17,0),"0.2.0", 5)
            r.appendDistfile(DistFile(True, "Linux", "http://sourceforge.net/projects/devicesinlan/files/devicesinlan/0.2.0/devicesinlan-0.2.0.tar.gz/download" ))
            p.releases.append(r)
            r=Release(datetime.datetime(2015,5,9,19,0),"0.3.0", 7)
            r.appendDistfile(DistFile(True, "Linux", "http://sourceforge.net/projects/devicesinlan/files/devicesinlan/0.3.0/devicesinlan-0.3.0.tar.gz/download" ))
            p.releases.append(r)
            r=Release(datetime.datetime(2015,5,24,8,14),"0.4.0", 13)
            r.appendDistfile(DistFile(True, "Linux", "http://sourceforge.net/projects/devicesinlan/files/devicesinlan/0.4.0/devicesinlan-0.4.0.tar.gz/download" ))
            p.releases.append(r)
            r=Release(datetime.datetime(2015,6,17,16,0),"0.5.0", 15)
            r.appendDistfile(DistFile(True, "Linux", "http://sourceforge.net/projects/devicesinlan/files/devicesinlan/0.5.0/devicesinlan-0.5.0.tar.gz/download" ))
            p.releases.append(r)
            r=Release(datetime.datetime(2015,8,19,16,10),"0.6.0", 30)
            r.appendDistfile(DistFile(True, "Linux", "http://sourceforge.net/projects/devicesinlan/files/devicesinlan/0.6.0/devicesinlan-0.6.0.tar.gz/download" ))
            p.releases.append(r)
            r=Release(datetime.datetime(2017,2,5,15,10),"0.9.0", 76)
            r.appendDistfile(DistFile(True, "Linux", "http://sourceforge.net/projects/devicesinlan/files/devicesinlan/0.9.0/devicesinlan-0.9.0.tar.gz/download" ))
            r.appendDistfile(DistFile(False, "Linux", "http://sourceforge.net/projects/devicesinlan/files/devicesinlan/0.9.0/devicesinlan-linux-0.9.0.x86_64.tar.gz/download" ))
            r.appendDistfile(DistFile(False, "Windows", "https://sourceforge.net/projects/devicesinlan/files/devicesinlan/0.9.0/devicesinlan-windows-0.9.0.amd64.exe/download" ))
            p.releases.append(r)
            r=Release(datetime.datetime(2017,2,6,6,10),"0.10.0", 80)
            r.appendDistfile(DistFile(True, "Linux", "http://sourceforge.net/projects/devicesinlan/files/devicesinlan/{0}/devicesinlan-{0}.tar.gz/download".format(r.version) ))
            r.appendDistfile(DistFile(False, "Linux", "http://sourceforge.net/projects/devicesinlan/files/devicesinlan/{0}/devicesinlan-linux-{0}.x86_64.tar.gz/download".format(r.version) ))
            r.appendDistfile(DistFile(False, "Windows", "https://sourceforge.net/projects/devicesinlan/files/devicesinlan/{0}/devicesinlan-windows-{0}.amd64.exe/download".format(r.version) ))
            p.releases.append(r)
            r=Release(datetime.datetime(2017,2,7,6,10),"0.11.0", 85)
            r.appendDistfile(DistFile(True, "Linux", "http://sourceforge.net/projects/devicesinlan/files/devicesinlan/{0}/devicesinlan-{0}.tar.gz/download".format(r.version) ))
            r.appendDistfile(DistFile(False, "Linux", "http://sourceforge.net/projects/devicesinlan/files/devicesinlan/{0}/devicesinlan-linux-{0}.x86_64.tar.gz/download".format(r.version) ))
            r.appendDistfile(DistFile(False, "Windows", "https://sourceforge.net/projects/devicesinlan/files/devicesinlan/{0}/devicesinlan-windows-{0}.amd64.exe/download".format(r.version) ))
            p.releases.append(r)
            r=Release(datetime.datetime(2017,2,8,20,0),"1.0.0", 108)
            r.appendDistfile(DistFile(True, "Linux", "http://sourceforge.net/projects/devicesinlan/files/devicesinlan/{0}/devicesinlan-{0}.tar.gz/download".format(r.version) ))
            r.appendDistfile(DistFile(False, "Linux", "http://sourceforge.net/projects/devicesinlan/files/devicesinlan/{0}/devicesinlan-linux-{0}.x86_64.tar.gz/download".format(r.version) ))
            r.appendDistfile(DistFile(False, "Windows", "https://sourceforge.net/projects/devicesinlan/files/devicesinlan/{0}/devicesinlan-windows-{0}.amd64.exe/download".format(r.version) ))
            p.releases.append(r)
            r=Release(datetime.datetime(2017,2,9,6,0),"1.0.1", 110)
            r.appendDistfile(DistFile(True, "Linux", "http://sourceforge.net/projects/devicesinlan/files/devicesinlan/{0}/devicesinlan-{0}.tar.gz/download".format(r.version) ))
            r.appendDistfile(DistFile(False, "Linux", "http://sourceforge.net/projects/devicesinlan/files/devicesinlan/{0}/devicesinlan-linux-{0}.x86_64.tar.gz/download".format(r.version) ))
            r.appendDistfile(DistFile(False, "Windows", "https://sourceforge.net/projects/devicesinlan/files/devicesinlan/{0}/devicesinlan-windows-{0}.amd64.exe/download".format(r.version) ))
            p.releases.append(r)
            r=Release(datetime.datetime(2017,2,22,6,0),"1.0.2", 116)
            r.appendDistfile(DistFile(True, "Linux", "http://sourceforge.net/projects/devicesinlan/files/devicesinlan/{0}/devicesinlan-{0}.tar.gz/download".format(r.version) ))
            r.appendDistfile(DistFile(False, "Linux", "http://sourceforge.net/projects/devicesinlan/files/devicesinlan/{0}/devicesinlan-linux-{0}.x86_64.tar.gz/download".format(r.version) ))
            r.appendDistfile(DistFile(False, "Windows", "https://sourceforge.net/projects/devicesinlan/files/devicesinlan/{0}/devicesinlan-windows-{0}.amd64.exe/download".format(r.version) ))
            p.releases.append(r)
            r=Release(datetime.datetime(2017,2,26,6,0),"1.1.0", 119)
            r.appendDistfile(DistFile(True, "Linux", "http://sourceforge.net/projects/devicesinlan/files/devicesinlan/{0}/devicesinlan-{0}.tar.gz/download".format(r.version) ))
            r.appendDistfile(DistFile(False, "Linux", "http://sourceforge.net/projects/devicesinlan/files/devicesinlan/{0}/devicesinlan-linux-{0}.x86_64.tar.gz/download".format(r.version) ))
            r.appendDistfile(DistFile(False, "Windows", "https://sourceforge.net/projects/devicesinlan/files/devicesinlan/{0}/devicesinlan-windows-{0}.amd64.exe/download".format(r.version) ))
            p.releases.append(r)
            r=Release(datetime.datetime(2017,12,28,6,0),"1.2.0", 136)
            r.appendDistfile(DistFile(True, "Linux", "http://sourceforge.net/projects/devicesinlan/files/devicesinlan/{0}/devicesinlan-{0}.tar.gz/download".format(r.version) ))
            r.appendDistfile(DistFile(False, "Windows", "https://sourceforge.net/projects/devicesinlan/files/devicesinlan/{0}/devicesinlan-windows-{0}.amd64.exe/download".format(r.version) ))
            p.releases.append(r)
            r=Release(datetime.datetime(2018,1,21,8,0),"1.3.0", 150)
            r.appendDistfile(DistFile(True, "Linux", "http://sourceforge.net/projects/devicesinlan/files/devicesinlan/{0}/devicesinlan-{0}.tar.gz/download".format(r.version) ))
            r.appendDistfile(DistFile(False, "Windows", "https://sourceforge.net/projects/devicesinlan/files/devicesinlan/{0}/devicesinlan-windows-{0}.amd64.exe/download".format(r.version) ))
            p.releases.append(r)

        def news():            
            p.news.append(News(datetime.datetime(2015,5,9,19,0),
                                                   _("Proyecto DevicesInLAN"), 
                                                   p.htmlImage(), 
                                                   _("""He publicado la primera versión de este proyecto:
<p>Los cambios más importantes son:
<ul>
   <li>Añadida la funcionalidad básica</li>
   <li>Traducción española</li>
</ul>""")))
            p.news.append(News(datetime.datetime(2015,5,24,8,14),
                                                    _("Proyecto DevicesInLAN. Versión")+" 0.4.0", 
                                                   p.htmlImage(), 
                                                   _("""Nueva versión del proyecto:
<p>Los cambios más importantes son:
<ul>
   <li>Los dispositivos conocidos son listados y ordenados por su alias</li>
   <li>Los dispositivos detectados en la red son listados ahora por su dirección IP</li>
   <li>Ya se puede añadir y borrar dispositivos conocidos desde la línea de comandos</li>
   <li>El listado de dispositivos de red no muestra más duplicados</li>
</ul>""")))
            p.news.append(News(datetime.datetime(2015,6,17,16,0),
                                                    _("Proyecto DevicesInLAN. Versión")+" 0.5.0", 
                                                   p.htmlImage(), 
                                                   _("""Nueva versión del proyecto.
<p>La salida por consola muestra ahora el número de dispositivos conectados en la red""")))            
            p.news.append(News(datetime.datetime(2015,8,19,16,10),
                                                    _("Proyecto DevicesInLAN. Versión")+" 0.6.0", 
                                                   p.htmlImage(), 
                                                   _("""Nueva versión del proyecto.
<p>Los cambios más importantes son:
<ul>
   <li>Añadida búsqueda de dispositivos por ping</li>
   <li>Añadido un escáner propio de ARP</li>
   <li>Añadido el fichero ieee-oui.txt con la base de datos de marcas de MAC con get-oui de arp-scan</li>
</ul>""")))            
            p.news.append(News(datetime.datetime(2017,2,5,15,10),
                                                    _("Proyecto DevicesInLAN. Versión")+" 0.9.0", 
                                                   p.htmlImage(), 
                                                   _("""Nueva versión del proyecto.
<p>Los cambios más importantes son:
<ul>
   <li>Mejorada la salida de lista en consola</li>
   <li>Se ha añadido los tipos de dispositivo a las listas</li>
</ul>"""))) 
            p.news.append(News(datetime.datetime(2017,2,6,6,10),
                                                    _("Proyecto DevicesInLAN. Versión")+" 0.10.0", 
                                                   p.htmlImage(), 
                                                   _("""Nueva versión del proyecto.
<p>Los cambios más importantes son:
<ul>
   <li>Sustituido la clase Color por el packete Colorama</li>
   <li>Ahora se ve Color en los informes de consola de windows</li>
</ul>""")))            
            p.news.append(News(datetime.datetime(2017,2,7,6,10),
                                                    _("Proyecto DevicesInLAN. Versión")+" 0.11.0", 
                                                   p.htmlImage(), 
                                                   _("""Nueva versión del proyecto.
<p>Los cambios más importantes son:
<ul>
   <li>Sustituido Threads por PoolThreadExecutor para la concurrencia de peticiones</li>
   <li>Añadido a las configuraciones la concurrencia</li>
   <li>Mejorados los informes de consola</li>
</ul>""")))
            p.news.append(News(datetime.datetime(2017,2,8,20,0),
                                                    _("Proyecto DevicesInLAN. Versión")+" 1.0.0", 
                                                   p.htmlImage(), 
                                                   _("""Nueva versión del proyecto.
<p>Los cambios más importantes son:
<ul>
   <li>Página man creada</li>
   <li>Carga y guarda listas de dispositivos</li>
   <li>Comprueba nuevas versiones</li>
   <li>Obtiene información estadística de instalaciones</li>
</ul>""")))
            p.news.append(News(datetime.datetime(2017,2,9,6,0),
                                                    _("Proyecto DevicesInLAN. Versión")+" 1.0.1", 
                                                   p.htmlImage(), 
                                                   _("""Nueva versión del proyecto.
<p>Los cambios más importantes son:
<ul>
   <li>Mejorado el sistema de estadísticas</li>
   <li>Arreglados pequeños bugs</li>
</ul>""")))     
            p.news.append(News(datetime.datetime(2017,2,22,6,0),
                                                    _("Proyecto DevicesInLAN. Versión")+" 1.0.2", 
                                                   p.htmlImage(), 
                                                   _("""Nueva versión del proyecto.
<p>Los cambios más importantes son:
<ul>
   <li>Añadido sistema de logs</li>
   <li>Las estadisticas funcionan también en modo consola</li>
   <li>Se puede añadir un tipo de dispositivo también en modo consola</li>
   <li>Se puede cargar un ficheros, guardar la lista de dispositivos conocidos y borrar la base de datostambién en modo consola</li>
</ul>""")))     
            p.news.append(News(datetime.datetime(2017,2,26,6,0),
                                                    _("Proyecto DevicesInLAN. Versión")+" 1.1.0", 
                                                   p.htmlImage(), 
                                                   _("""Nueva versión del proyecto.
<p>Los cambios más importantes son:
<ul>
   <li>Los logs de depuración están desactivados por defecto</li>
   <li>El sistema de estadísticas manda ahora la plataforma</li>
</ul>""")))   
            p.news.append(News(datetime.datetime(2017,12,28,6,0),
                                                    _("Proyecto DevicesInLAN. Versión")+" 1.2.0", 
                                                   p.htmlImage(), 
                                                   _("""Nueva versión del proyecto.
<p>Los cambios más importantes son:
<ul>
   <li>Ya no se necesita ser superusuario para ejecutar el programa</li>
   <li>Mejorada la documentación y la traducción al español</li>
   <li>Se ha quitado la dependencia de netifaces</li>
   <li>Eliminado un acceso directo erróneo</li>
   <li>Añadida busqueda por socket más rápida</li>
   <li>Cambiado el sistema de distribución de innoreader al nativo de python</li>
</ul>
ANTES DE INSTALAR ESTA VERSION EN WINDOWS ELIMINE LA ANTERIOR DESDE PROGRAMAS DE WINDOWS
""")))   
            p.news.append(News(datetime.datetime(2018,1,21,8,0),
                                                    _("Proyecto DevicesInLAN. Versión")+" 1.3.0", 
                                                   p.htmlImage(), 
                                                   _("""Nueva versión del proyecto.
<p>Los cambios más importantes son:
<ul>
   <li>Arreglado un error con el directorio de las traducciones</li>
   <li>El dispositivo usado para lanzarr DevicesInLAN se muestra en azul</li>
   <li>Ahora hay dos ejecutables uno para consola y otro para el interfaz gráfico</li>
   <li>Se ha creado documentación para ambos ejecutables</li>
   <li>Se ha eliminado la dependencia de man2html</li>
</ul>
""")))   
        ##############################
        p=Project("devicesinlan", "DevicesInLAN", "images/devicesinlan.jpg", "net-analyzer/devicesinlan")
        p.brief=_('Muestra dispositivos en una red LAN. Puedes introducir dispositivos conocidos,  para detectar dispositivos extraños.') + "\n" + \
                    '   <p>'+_('Puedes consultar las estadísticas de instalaciones en este ') + ' <a href="http://devicesinlan.sourceforge.net/php/devicesinlan_statistics.php">'+_('enlace')+'</a>\n'
        news()
        releases()
        screenshots()
        p.writePage()
        self.append(p)

class SetNews(SetCommons):
    def __init__(self):
        SetCommons.__init__(self)
        
    def sort(self, reversed=True):
        self.arr=sorted(self.arr, key=lambda n: n.datetime,  reverse=reversed) 
        
        
    def year_subarr(self, year):
        """Returns an arr with News Object of the year passed as parameter"""
        r=[]
        for n in self.arr:
            if n.datetime.year==year:
                r.append(n)
        return r
        
    def writePageAllNews(self, title, htmlpage):
        """title is the page title
        htmlpage name of the page.html"""
        p=Page(title, htmlpage)
        
        #Gets max and min years
        self.sort(False)
        minn=self.arr[0]
        maxn=self.arr[self.length()-1]
        years=range(minn.datetime.year, maxn.datetime.year+1)


        #Javascript code
        bo="<h1>{}</h1>".format(title)
        bo=bo+"""
<script type="text/javascript">
    function optionCheck(){
        var option = document.getElementById("combo").value;
        var combo= document.getElementById("combo");

        //Cambia a ocultas todos
        for (var i=0;i<combo.options.length;i++){
            document.getElementById(combo.options[i].value).style.display="none";
        }
        //Muestra la seleccionada
        document.getElementById(option).style.display ="inline-block";

    }
</SCRIPT>"""

        #Genera el select con los años
        bo=bo+'\n<p><center>'+_('Seleccione un año:')+' \n'
        bo=bo+'    <select  onchange="optionCheck()" id="combo" size="1" class="form-select">\n'
        
        for year in years:
            if year==maxn.datetime.year:
                selected="selected"
            else:
                selected=""
            bo=bo+'        <option value="{0}" {1}>{0}</option>\n'.format(year,selected)
        bo=bo+'    </select></center>\n'
        bo=bo+'<p>\n'

        #Genera el listado de noticias
        for year in years:
            if year==maxn.datetime.year:
                display="inline-block"
            else:
                display="none"
            bo=bo+'\n<div id="{0}" style="display:{1}">\n'.format(year,display)
            for n in self.year_subarr(year):
                bo=bo+n.html()
            bo=bo+'</div id="{0}">\n'.format(year)

        p.write(bo)  
        
    def linkToPageAllNews(self, page):
        return _("Para ver noticias anteriores pulse {}aquí{}").format('<a href="'+page+'">', '</a>')

class SetReleases(SetCommons):
    def __init__(self):
        SetCommons.__init__(self)
        
    def html(self):
        self.sort()
        body=""
        body=body+'<center><table border="1">\n'
        body=body+'  <THEAD align="center">\n'
        body=body+'     <TR>\n'
        body=body+'         <TH >'+_('Fecha y hora')+'</TH>\n'
        body=body+'         <TH >'+_('Versión del programa')+'</TH>\n'
        body=body+'         <TH>'+_('Versión de subversión')+'</TH>\n'
        body=body+'         <TH>'+_('Código fuente')+'</TH>\n'
        body=body+'         <TH>'+_('Binario')+'</TH>\n'
        body=body+'     </TR>\n'
        body=body+'   </THEAD>\n'
        for r in self.arr:
            body=body+r.html()
        body=body+'</table></center><p>\n'
        return body
        
    def sort(self):
        self.arr=sorted(self.arr, key=lambda n: n.subversion,  reverse=True) 
        
class Project:
    def __init__(self, name,  beauty, image,  portagepath=None):
        self.name=name
        self.beauty=beauty
        self.portagepath=portagepath
        self.releases=SetReleases()
        self.news=SetNews()
        self.screenshots=SetScreenshots()
        self.image=image
        self.brief=""
        self.installation=""#instructions, dependencies request. HTML text. titles start by h3
        self.manual=""#instructions. HTML text

    def url_project(self):
        return "https://sourceforge.net/projects/{}".format(self.name)


    def htmlImage(self):
        return htmlImage(self.image, 90, 90)

    def writePage(self):
        """Write project page"""
        p=Page(_("Proyecto {}").format(self.beauty), self.name+".html")
        body='<a href="{}"><img src="http://sourceforge.net/sflogo.php?group_id=158664&amp;type=12" alt="SourceForge.net" title="Project page" id="sflogo"/></a>\n'.format(self.url_project())
        
        body=body+'   <h1>'+_('Proyecto {}').format(self.beauty)+'</h1>\n'
        body=body+'   <p>'+ self.brief+'<p>\n'
        body=body+'   <p>'+_('Puedes consultar las {}estadísticas históricas{} del proyecto o las de {}los últimos 12 meses{} en Sourceforge.').format('<a id="statistics" >','</a>','<a id="statistics12" >','</a>') +'\n'
        body=body+"""
   <script  type="text/javascript">
        var today=new Date();
        var start=new Date(today);
        start.setDate(today.getDate()-365);
        document.getElementById('statistics').setAttribute('href', 'https://sourceforge.net/projects/{0}/files/stats/timeline?dates=2000-01-01+to+'+today.toISOString().slice(0,10));
        document.getElementById('statistics12').setAttribute('href', 'https://sourceforge.net/projects/{0}/files/stats/timeline?dates='+start.toISOString().slice(0,10)+'+to+'+today.toISOString().slice(0,10));
   </script>
""".format(self.name)

        body=body+'   <div class="tabber">\n'
        
        if self.news.length()>0:
            self.news.sort()
            body=body+'   <div class="tabbertab"><h2>'+_('Noticias')+'</h2>\n'
            for n in self.news.arr[0:5]:#Only last 5
                body=body +n.html()
            body=body+"<p>"+self.news.linkToPageAllNews("allnews_"+self.name+".html")        

            self.news.writePageAllNews(_("Todas las noticias del proyecto {}").format(self.beauty), "allnews_"+self.name+".html")
        
            body=body+'   </div class="tabbertab">\n'
            
        if self.screenshots.length()>0:
            self.screenshots.sort()
            body=body+'   <div class="tabbertab"><h2>'+_('Capturas de pantalla')+'</h2>\n'
            for s in self.screenshots.arr:
                body=body +s.html()
            body=body+'   </div class="tabbertab">\n'
            
        
        body=body+'   <div class="tabbertab"><h2>Releases</h2>\n'
        body=body+'   '+_('En esta sección se muestran las distintas versiones del programa y sus correspondencias con el subversión.')+'<p>\n'        
        body=body+self.releases.html()
        
        if self.portagepath!=None:
            body=body+'   '+_('Si utilizas gentoo puedes usar el siguiente {}ebuild{}.').format('<a href="https://sourceforge.net/p/xulpymoney/code/HEAD/tree/myportage/'+ self.portagepath+'/">','</a>')+'<p>\n'
        body=body+'   </div class="tabbertab">\n'
                    
        if self.installation!="":
            body=body+'   <div class="tabbertab"><h2>'+_('Instalación')+'</h2>\n'
            body=body+self.installation
            body=body+'   </div class="tabbertab">\n'          
            
        if self.manual!="":
            body=body+'   <div class="tabbertab"><h2>'+_('Manual de usuario')+'</h2>\n'
            body=body+self.manual
            body=body+'   </div class="tabbertab">\n'
            
        body=body+'   <div class="tabbertab"><h2>'+_('Código fuente')+'</h2>\n'
        body=body+_('El código fuente en desarrollo te lo puedes bajar del subversion de {}.').format('<a href="https://sourceforge.net/p/'+self.name+'/code/HEAD/tree/">Sourceforge</a>')+'<p>\n'
        
        body=body+_('La documentación del código es generada automáticamente con la herramienta {}Doxygen{}.').format('<a href="../doxygen/{}/index.html">'.format(self.name), "</a>")+'\n'
        
        body=body+'   </div class="tabbertab">\n'
        body=body+'    </div class="tabber">\n'

        p.write(body)

class News:
   def __init__(self, dt,  title,    htmlimage, text):
      self.title=title
      self.datetime=dt
      self.htmlimage=htmlimage
      self.text=text

   def html(self):
      body='   <div id="news">\n'
      body=body + '      <div id="news-title">'+ self.title +'</div>\n'
      body=body + '      <div id="news-date">'+ str(self.datetime)[:16] +'</div>\n'
      body=body + '      <table><tr><td style="padding-right:30px;"><div id="news-img">' + self.htmlimage +'</div></td><td>'+self.text+'</td></tr></table>\n'
#      body=body + '      <table><tr><td>'+self.text+'</td><td style="padding-left:30px;"><div id="news-img">' + self.htmlimage +'</div></td></tr></table>\n'
      body=body + '   </div id> <!-- Closing div news -->\n'
      return body

class Page:
    def __init__(self, title, file):
        self.title=title
        self.file=file
        self.dirsalida="publico/{0}".format(_("es"))
        self.generateSVG()
        
        
    def generateSVG(self):
        s='<?xml version="1.0" encoding="utf-8"  standalone="no"?>\n'
        s=s+'<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN"  "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">\n'
        s=s+'<svg flex="2" id="gi" width="800" height="50"  viewBox="0 0 800 50"  xmlns="http://www.w3.org/2000/svg" version="1.1" xmlns:xlink="http://www.w3.org/1999/xlink" >\n'
        s=s+'<defs>\n'
        s=s+'   <linearGradient id="two_hues">\n'
        s=s+'      <stop offset="0%" style="stop-color: #8799c7;"/>\n'
        s=s+'      <stop offset="100%" style="stop-color: #e3e3e3;"/>\n'
        s=s+'   </linearGradient>\n'
        s=s+'</defs>\n'
        s=s+'<rect x="0" y="0" width="800" height="50" style="fill: url(#two_hues);"/>\n'
        s=s+'<text x="20" y="40" style="font-weight:bold; fill: white; font-size: 14pt;">' + self.title + '</text>\n'
        s=s+'<a target="_top" xlink:href="http://turulomio.users.sourceforge.net/es/' + self.file+ '"><image xlink:href="spanish.png" x="698" y="10" width="50" height="30"/></a>\n'
        s=s+'<a target="_top" xlink:href="http://turulomio.users.sourceforge.net/en/' + self.file+ '"><image xlink:href="english.png" x="750" y="10" width="50" height="30"/></a>\n'
        s=s+'</svg>\n'
        f=codecs.open(self.dirsalida + "/images/"+self.file+".svg",'w','utf-8')
        f.write(s)
        f.close()
        
        
    def footer(self):
        s=  '<div id="footer">Copyright © 1998-{0} Mariano Muñoz. <span class="modified">{1}: {2}.<span></div>\n'.format( datetime.date.today().year ,_("Última actualización"), datetime.datetime.now())
        s=s+'</body>\n'
        return s

    def header(self):
       s=  '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">\n'
       s=s+'<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en">\n'
       s=s+'<head>\n'
       s=s+'   <title>Mariano Muñoz > ' + self.title+ '</title>\n'
       s=s+'   <meta http-equiv="Content-Type" content="text/html;charset=UTF-8">\n'
       s=s+'   <meta name="robots" content="index, follow"/>\n'
       s=s+'   <meta name="revisit-after" content="5 days"/>\n'
       s=s+'   <link rel="shortcut icon" href="/images/penguin.png"/>\n'
       s=s+'   <link rel="stylesheet" type="text/css" href="mariano.css"/>\n'
       s=s+'   <script type="text/javascript" src="tabber.js"></script><link rel="stylesheet" href="example.css" TYPE="text/css" MEDIA="screen">\n'
       s=s+'      <link rel="stylesheet" href="example-print.css" TYPE="text/css" MEDIA="print">\n'
       s=s+'   <script type="text/javascript">document.write(\'<style type="text/css">.tabber{display:none;}<\/style>\');</script>\n'
    
       s=s+'</head>\n'
       s=s+'<body>\n'
       return s

  


    def toc(self, noticias, descargas):
        toc=    '<div id="toc">\n'
        toc=toc+'<div id="toc-header">Tabla de contenidos</div>\n'
        if len(noticias)>0:
          toc=toc+'<ol>Noticias\n'
          for i in noticias:
             toc=toc+'<li>' + i + '</li>\n'
          toc=toc+'</ol>\n'
        if len(descargas)>0:
          toc=toc+'<ol>Descargas\n'
          for i in descargas:
             toc=toc+'<li>' + i + '</li>\n'
          toc=toc+'</ol>\n'
        toc=toc+'</div>\n'
        return toc
        
    def menu(self):
        s=  '<div id="teaser"><object width="800" height="50" data="images/' + self.file+".svg"+ '" type="image/svg+xml">Uses SVG web standard, Internet Explorer has not. Use Firefox or Chromium.</object></div>\n'
        s=s+'<div id="hbar">\n'
        s=s+'   <div> </div>\n'
        s=s+'   <div id="menu">\n'
        s=s+'      <ul id="menu-list">\n'
        s=s+'         <li><a href="index.html">'+_('Inicio')+'</a></li>\n'
        s=s+'         <li><a href="quiensoy.html">'+_('¿Quién soy?')+'</a></li>\n'
        s=s+'         <li><a href="proyectos.html">'+_('Mis proyectos')+'</a></li>\n'
        s=s+'      </ul>\n'
        s=s+'   </div>\n'
        s=s+'</div>\n'
        return s
        
    def body(self, bo):
        bod=     '<div id="main">\n'
        bod=bod+bo
        bod=bod+'</div>\n'
        return bod


    def write(self, bo):
        res=self.header() + self.menu() + self.body(bo) + self.footer()
        f=codecs.open(self.dirsalida + "/"+self.file,'w','utf-8')
        f.write(res)
        f.close()

def htmlImage(file, height=90, width=90):
    return '<img src="{}" height="{}" width="{}"></img>'.format(file, height, width)

def redirect_index_html(output):
    body=     '<HTML><HEAD>\n'
    body=body + '<META HTTP-EQUIV="refresh" CONTENT="0;URL=http://turulomio.users.sourceforge.net/es/index.html">\n'
    body=body + '</HEAD><BODY></BODY></HTML>\n'
    f=codecs.open(output + "/index.html",'w','utf-8')
    f.write(body)
    f.close()


def redirect_projects():
    os.system("find redirects -type d -exec chmod -c 755 {} \;")
    os.system("find redirects -type f -exec chmod -c 644 {} \;")

    os.system("rsync -avzP -e 'ssh -l turulomio,devicesinlan' redirects/devicesinlan/ web.sourceforge.net:/home/groups/d/de/devicesinlan/htdocs/ --delete-after")
    os.system("rsync -avzP -e 'ssh -l turulomio,glparchis' redirects/glparchis/ web.sourceforge.net:/home/groups/g/gl/glparchis/htdocs/ --delete-after")
    os.system("rsync -avzP -e 'ssh -l turulomio,recovermypartit' redirects/recovermypartit/ web.sourceforge.net:/home/groups/r/re/recovermypartit/htdocs/ --delete-after")
    os.system("rsync -avzP -e 'ssh -l turulomio,didyoureadme' redirects/didyoureadme/ web.sourceforge.net:/home/groups/d/di/didyoureadme/htdocs/ --delete-after")
    os.system("rsync -avzP -e 'ssh -l turulomio,kdepim2google' redirects/kdepim2google/ web.sourceforge.net:/home/groups/k/kd/kdepim2google/htdocs/ --delete-after")




## This function generates myweb in a specific language
## @param language. Can be en or es
def generate_myweb(output, language):
    if language=="es":
        gettext.install('myweb', 'badlocale')
    else:
        lang1=gettext.translation('myweb', 'po/locale', languages=[language])
        lang1.install()
    print(_("  - Página generada con idioma '{}'").format(language))


    projects=SetProjects(output, language)
    projects.write()
    pages=SetPages(output, language, projects)
    pages.write()
    redirect_index_html(output)

def main():
    parser=argparse.ArgumentParser(prog='myweb', description=_('Genera una página web personal, estática y multilingue'), epilog=_("Desarrollado por Mariano Muñoz 1998-{}".format(datetime.date.today().year)), formatter_class=argparse.RawTextHelpFormatter)
    group= parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--redirects', help=_("Redirects several project pages to my personal web page"),  action='store_true', default=False)
    group.add_argument('--upload', help=_("Sube la página web a SourceForge"),  action='store_true', default=False)
    parser.add_argument('--output', help=_("Directorio de salida de la página web estática"),  action='store', default="publico/")
    args=parser.parse_args()
    
    if args.redirects==True:
        redirect_projects()
        sys.exit(0)


    if args.upload==True:
        os.system("xgettext -L Python --no-wrap --no-location --from-code UTF-8 -o po/myweb.pot myweb.py ")
        os.system("msgmerge -N --no-wrap -U po/en.po po/myweb.pot")
        os.system("mcedit po/en.po")
        os.system("msgfmt -cv -o po/locale/en/LC_MESSAGES/myweb.mo po/en.po")

    os.system("rm -rf {}".format(args.output))
    os.mkdir(args.output)
    os.mkdir("{}/es/".format(args.output))
    os.mkdir("{}/en/".format(args.output))
    os.mkdir("{}/es/images".format(args.output))
    os.mkdir("{}/en/images".format(args.output))
    shutil.copy("mariano.css", args.output)
    os.system("cp --preserve=all images/* {}/es/images/".format(args.output))
    os.system("cp --preserve=all images/* {}/en/images/".format(args.output))
    os.system("cp --preserve=all *.css js/tab/*.js js/tab/*.css {}/es".format(args.output))
    os.system("cp --preserve=all *.css js/tab/*.js js/tab/*.css {}/en".format(args.output))

    for language in ['es', 'en']:
        generate_myweb(args.output, language)

    if args.upload==True:
        os.system("find publico/ -type d -exec chmod 755 {} \;")
        os.system("find publico/ -type f -exec chmod 644 {} \;")
        os.system("rsync -avzP -e 'ssh -l turulomio' publico/ frs.sourceforge.net:/home/users/t/tu/turulomio/userweb/htdocs/ --exclude=doxygen --delete-after")

if __name__ == '__main__':
    main()

_=gettext.gettext#To avoid warnings in eric


