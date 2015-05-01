# original author: oskar.blom@gmail.com (with changes added here)
# from: http://flask.pocoo.org/snippets/116/
#
# Make sure your gevent version is >= 1.0
import gevent
from gevent.wsgi import WSGIServer
from gevent.queue import Queue

from flask import Flask, Response, render_template, request
from flask.ext.cors import CORS

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
cors = CORS(app)
subscriptions = []

# Client code consumes like this.
@app.route("/")
def index():
    event_receiver_page = """
    <html>
      <head>
        <style>
          h1 {
            color: white;
            text-shadow: 0 0 4px rgba(0,0,0,0.3);
            font-family: helvetica, sans-serif;
            text-align: center;
            font-weight: normal;
          }
          h1 span#color {
            font-family: Monaco, monospace;
          }
          body {
            background: #ccc;
            padding: 50px;
          }
        </style>
      </head>
      <body id="changeBackground">
        
        <h1>Server sent background color: <span id="color"></span></h1>
        
        <script type="text/javascript">
          var evtSrc = new EventSource("/subscribe");
          
          var eventOutputContainer = document.getElementById("color");
          var pageBody = document.getElementById("changeBackground");
          
          evtSrc.onmessage = function(e) {
            console.log(e.data);
            eventOutputContainer.innerHTML = e.data;
            pageBody.style.backgroundColor = e.data;
          };
        </script>
      </body>
    </html>
    """
    return(event_receiver_page)

@app.route("/debug")
def debug():
    return "Currently %d subscriptions" % len(subscriptions)

@app.route("/publish", methods = ['GET', 'POST'])
def publish():

    msg = str(request.json);
    msg = string.replace(msg, '\'', '\"')
    msg = string.replace(msg, 'u', '')

    def notify():
        for sub in subscriptions[:]:
            sub.put(msg)
    
    gevent.spawn(notify)
    
    return render_template('index.html')

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
        except GeneratorExit: # Or maybe use flask signals
            subscriptions.remove(q)

    return Response(gen(), mimetype="text/event-stream")

if __name__ == "__main__":
    app.debug = True
    server = WSGIServer(("", 5000), app)
    server.serve_forever()
    # Then visit http://localhost:5000 to subscribe 
    # and send messages by visiting http://localhost:5000/publish