from flask import Flask, render_template

app = Flask(__name__)

# NOTE: It is advised to load the config ASAP, so we put 
# it here before resuming the other imports (See more below)
app.config.from_object('lghs_website.default_config')
app.config.from_envvar('LGHS_WEBSITE_CONFIG', silent=True)

# Example: https://github.com/mitsuhiko/flask-website/blob/master/flask_website/__init__.py It's been done here too
# Source: http://flask.pocoo.org/docs/0.10/config/#configuring-from-files (at the bottom of the section)

from .views import general
from .utils import hs_is_open


@app.errorhandler(404)
def not_found(error):
	return render_template('404.html'), 404


# NOTE: Let's try to avoid renew the cache too often if we can.
# Here we only inject the boolean is_open so that the cache isn't
# renewed as often as if we injected the time directly instead.
# (so it only does when the HS switches between open/close status)
app.context_processor(lambda: {'hs_is_open': hs_is_open()})  # Can be used as a decorator

app.register_blueprint(general.mod)
