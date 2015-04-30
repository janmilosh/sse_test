from flask import make_response, render_template
from flask import redirect, session, url_for


import gevent
from gevent.wsgi import WSGIServer
from gevent.queue import Queue

from flask import Flask, Response, render_template

subscriptions = []

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



@main.route('/')
def publish():
    msg = '{"lat": 39.9829514, "lon": -82.990829}';
    def notify():
        for sub in subscriptions[:]:
            sub.put(msg)
    
    gevent.spawn(notify)
    
    return render_template('index.html')

@main.route("/subscribe")
def subscribe():
    def gen():
        q = Queue()
        subscriptions.append(q)
        print len(subscriptions)
        try:
            while True:
                result = q.get()
                ev = ServerSentEvent(str(result))
                yield ev.encode()
        except GeneratorExit:
            subscriptions.remove(q)

    return Response(gen(), mimetype="text/event-stream")

@main.route("/debug")
def debug():
    return "Currently %d subscriptions" % len(subscriptions)
