Requires Python 2.7

To run, create virtual environment and install requirements.

Start server: 

```
$ gunicorn -b 0.0.0.0:5000 -k gevent application:app
```

Open a browser window to: ```localhost:5000```

Open another browser window to: ```localhost:5000/receive```

Click on the sender map and the location will appear on the receiver map.