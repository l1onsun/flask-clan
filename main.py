import peewee as pw
import datetime
import cherrypy
import json
import jinja2
import os
import pickle

cherrypy._cperror._HTTPErrorTemplate = """
<!DOCTYPE html PUBLIC\n"-//W3C//DTD XHTML 1.0 Transitional//EN"\n"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">\n
<html>\n
<head>\n
<meta http-equiv="Content-Type" content="text/html; charset=utf-8"></meta>\n
<title>%(status)s
</title>\n
<style type="text/css">\n    #powered_by {\n margin-top: 20px;\n border-top: 2px solid black;\n font-style: italic;\n }\n\n #traceback {\n color: red;\n}\n
</style>\n
</head>\n
<body>\n        <h2>%(status)s</h2>\n
<p>%(message)s</p>\n
<div id="powered_by">\n
<span>\n        Powered by <a href="http://www.cherrypy.org">CherryPy %(version)s</a>\n
</span>\n
</div>\n
</body>\n
</html>\n
"""

templateLoader = jinja2.FileSystemLoader(searchpath="./templates")
templateEnv = jinja2.Environment(loader=templateLoader)
template = templateEnv.get_template('index_moderated.html')


from db import db, Player, handle_memberList

class Clan:
    def __init__(self):
        self._index = "no information"
        with open('last_update.pickle', 'rb') as f:
            self._update = pickle.load(f)

        with db:
            db.create_tables([Player])

    @cherrypy.expose
    def index(self):
        return template.render(players=self._update["memberList"])

    @cherrypy.expose
    def tag(self):
        return self._update["tag"]

    @cherrypy.expose
    @cherrypy.tools.json_in()
    def update(self):
        self._update = cherrypy.request.json
        handle_memberList(self._update["memberList"])
        with open('last_update.pickle', 'wb') as f:
            pickle.dump(self._update, f)
        return "updated"


conf = {
        '/': {
            'tools.sessions.on': True,
            'tools.staticdir.root': os.path.abspath(os.getcwd())
        },
        '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': './public'
        }
    }

application = cherrypy.Application(Clan(), '/', conf)