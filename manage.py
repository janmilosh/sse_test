#!/usr/bin/env python
import os
from app import create_app
from flask.ext.script import Manager, Shell

import gevent
from gevent.wsgi import WSGIServer

app = create_app(os.getenv('FLASK_CONFIG') or 'default')

if __name__ == '__main__':
    
    app.debug = True
    http_server = WSGIServer(('', 5000), app)
    http_server.serve_forever()