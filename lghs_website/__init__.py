from flask import Flask, render_template
from .config import default_config

app = Flask(__name__)

# NOTE: It is advised to load the config ASAP, so we put 
# it here before resuming the other imports
# Example: https://github.com/mitsuhiko/flask-website/blob/master/flask_website/__init__.py It's been done here too
# Source: http://flask.pocoo.org/docs/0.10/config/#configuring-from-files (at the bottom of the section)
app.config.from_object(default_config)

# Provides config from the user environment, if set.
# The user can chose to provide its own config path
# or chose one made available in config/
# Eg: LGHS_WEB_CONFIG='config/dev_config.py'
app.config.from_envvar('LGHS_WEB_CONFIG', silent=True)

try:
	# user_config.py is situated at the same level as run.py and must contain a SECRET_KEY
	app.config.from_object('user_config')
except ImportError:
	import os
	
	# Generate the SECRET_KEY as per recommended in the doc
	# http://flask.pocoo.org/docs/0.10/quickstart/
	app.secret_key = os.urandom(24)

	with open('user_config.py', 'w', encoding='utf-8') as f:
		f.write('# Keep this really secret!\nSECRET_KEY = {}\n'.format(repr(app.secret_key)))
	
	print('Created the SECRET_KEY and stored it in user_config.py .')
	print()

from .views import general
from .utils import hs_is_open


@app.errorhandler(404)
def not_found(error):
	return render_template('404.html'), 404


# NOTE: Let's try to avoid renew the cache too often if we can.
# Here we only inject the boolean is_open so that the cache isn't
# renewed as often as if we injected the time directly instead.
# (so it only does when the HS switches between open/close status)
# NOTE: context_processor can also be used as a decorator.
app.context_processor(lambda: {'hs_is_open': hs_is_open()})

app.register_blueprint(general.mod)
