Requires Python 2.7

To run, create virtual environment and install requirements.

Start server: 

```
$ python manage.py runserver --debug
```

Open a browser window to: ```localhost:5000```

Open another browser window to: ```localhost:5000/publish```

Every time you refresh the publish browser, a random hex color value is sent to the other window and the background will change to that color.