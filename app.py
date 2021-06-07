import traceback
import logging.config
from flask import Flask
from flask import render_template, request, redirect, url_for

from src.recommend import predict as predict
from src.recommend import recommend as rec
import uuid

import yaml
# Load configuration file for parameters and tmo path
with open('config/project.yaml', "r") as f:
    config = yaml.load(f, Loader=yaml.FullLoader)


# Initialize the Flask application
app = Flask(__name__, template_folder="app/templates", static_folder="app/static")

# Configure flask app from flask_config.py
app.config.from_pyfile('config/flaskconfig.py')

# Define LOGGING_CONFIG in flask_config.py - path to config file for setting
# up the logger (e.g. config/logging/local.conf)
logging.config.fileConfig(app.config["LOGGING_CONFIG"])
logger = logging.getLogger(app.config["APP_NAME"])
logger.debug('Web app log')

# Initialize the database session
from src.create_db import Trails, TrailManager

trail_manager = TrailManager(app)


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        try:
            return render_template('index.html')
            logger.info("Index page accessed")
        except:
            return render_template('error.html')
            logger.warning('Error page')

    if request.method == 'POST':
        try:
            length = request.form['length']
            elevation_gain = request.form['elevation_gain']
            route_type = request.form['route_type']
            features = request.form.getlist('features')
            activities = request.form.getlist('activities')
            url_for_post = url_for('my_template', length=length, elevation_gain=elevation_gain, route_type=route_type,
                                   features=features, activities=activities)
            print(length)
            print(elevation_gain)
            if (length == "") | (elevation_gain == ""):
                return render_template('error.html')

            return redirect(url_for_post)
        except:
            return render_template('error.html')
            logger.warning('Error page')


@app.route('/my_template/<length>/<elevation_gain>/<route_type>/<features>/<activities>', methods=['GET', 'POST'])
def my_template(length, elevation_gain, route_type, features, activities):
    if request.method == 'GET':

        # Add to database
        input_id = str(uuid.uuid1())
        trail_manager.add_input(input_id, length, elevation_gain, route_type, features, activities)
        trail_manager.close()

        # Predict and recommend
        prediction = predict(length, elevation_gain, route_type, features, activities,
                             **config['recommend']['predict'])

        recommend_ids = rec(length, elevation_gain, route_type, features, activities,
                            **config['recommend']['recommend'])

        try:
            trails = trail_manager.session.query(Trails).filter(Trails.trail_id.in_(recommend_ids))\
                    .order_by(Trails.length)
            logger.debug("Index page accessed")
            return render_template('result.html', prediction=prediction, trails=trails)
        except:
            traceback.print_exc()
            logger.warning("Not able to display tracks, error page returned")
            return render_template('error.html')


if __name__ == '__main__':
    app.run(debug=app.config["DEBUG"], port=app.config["PORT"], host=app.config["HOST"])
