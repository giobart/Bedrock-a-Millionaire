import os
from flakon import create_app
from myservice.views import blueprints
from  flask_profiler import Profiler



_HERE = os.path.dirname(__file__)
_SETTINGS = os.path.join(_HERE, 'settings.ini')

app = create_app(blueprints=blueprints, settings=_SETTINGS)
app.config["DEBUG"] = True

# You need to declare necessary configuration to initialize
# flask-profiler as follows:
app.config["flask_profiler"] = {
    "verbose": True,
    "enabled": app.config["DEBUG"],
    "storage": {
        "engine": "sqlite",
    },
    "basicAuth":{
        "enabled": True,
        "username": "admin",
        "password": "admin"
    },
    "ignore": [
        "/static/*",
        "/secrets/password/"
    ]
}

profiler = Profiler(app)

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5000)