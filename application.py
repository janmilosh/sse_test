# original author: oskar.blom@gmail.com (with changes added here)
# from: http://flask.pocoo.org/snippets/116/
#
# Make sure your gevent version is >= 1.0
import gevent
from gevent.wsgi import WSGIServer
from gevent.queue import Queue

from flask_debugtoolbar import DebugToolbarExtension
from flask import Flask, Response, render_template, request
from flask.ext.cors import CORS

from config import BaseConfig

import time, random, json, string


# SSE "protocol" is described here: http://mzl.la/UPFyxY
class ServerSentEvent(object):

    def __init__(self, data):
        self.data = data
        self.event = None
        self.id = None
        self.desc_map = {
            self.data : "data",
            self.event : "event",
            self.id : "id"
        }

    def encode(self):
        if not self.data:
            return ""
        lines = ["%s: %s" % (v, k) 
                 for k, v in self.desc_map.iteritems() if k]
        
        return "%s\n\n" % "\n".join(lines)

app = Flask(__name__)

app.config.from_object(BaseConfig)

app.debug = True
toolbar = DebugToolbarExtension(app)

cors = CORS(app)
subscriptions = []


@app.route("/", methods = ['GET', 'POST'])
def send():

    msg = str(request.json);
    msg = string.replace(msg, '\'', '\"')
    msg = string.replace(msg, 'u', '')

    def notify():
        for sub in subscriptions[:]:
            sub.put(msg)
    
    gevent.spawn(notify)
    
    return render_template('index.html')

@app.route("/receive")
def receive():
    
    return render_template('receiver-map.html')

@app.route("/subscribe")
def subscribe():
    def gen():
        q = Queue()
        subscriptions.append(q)
        try:
            while True:
                result = q.get()
                ev = ServerSentEvent(str(result))
                yield ev.encode()
        except GeneratorExit:
            subscriptions.remove(q)

    return Response(gen(), mimetype="text/event-stream")

@app.route("/debug")
def debug():
    return "Currently %d subscriptions" % len(subscriptions)


if __name__ == "__main__":

    server = WSGIServer(("", 5000), app)
    server.serve_forever()
    