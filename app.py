import logging.config
import traceback
import uuid

import yaml
from flask import Flask
from flask import render_template, request, redirect, url_for

from src.create_db import Trails, TrailManager
from src.recommend import predict as predict
from src.recommend import recommend as rec

# Load configuration file for parameters and tmo path
with open('config/project.yaml', "r") as f:
    config = yaml.load(f, Loader=yaml.FullLoader)

# Initialize the Flask application
app = Flask(__name__, template_folder="app/templates",
            static_folder="app/static")

# Configure flask app from flask_config.py
app.config.from_pyfile('config/flaskconfig.py')

# Define LOGGING_CONFIG in flask_config.py - path to config file for setting
# up the logger (e.g. config/logging/local.conf)
logging.config.fileConfig(app.config["LOGGING_CONFIG"])
logger = logging.getLogger(app.config["APP_NAME"])
logger.debug('Web app log')

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
            # Get user inputs
            length = request.form['length']
            elevation_gain = request.form['elevation_gain']
            route_type = request.form['route_type']
            features = request.form.getlist('features')
            activities = request.form.getlist('activities')
            url_for_post = url_for('my_template',
                                   length=length,
                                   elevation_gain=elevation_gain,
                                   route_type=route_type,
                                   features=features,
                                   activities=activities)
            if (length == "") | (elevation_gain == ""):
                logger.debug("No input for length or elevation gain")
                return render_template('error.html')

            if (length.isnumeric() is False) | (elevation_gain.isnumeric() is
                                                False):
                logger.debug("Input for length or elevation gain is not "
                             "numeric")
                return render_template('error.html')


            return redirect(url_for_post)
        except:
            return render_template('error.html')
            logger.warning('Error page')


@app.route('/my_template/<length>/<elevation_gain>/<route_type>/<features>/'
           '<activities>', methods=['GET', 'POST'])
def my_template(length, elevation_gain, route_type, features, activities):
    if request.method == 'GET':

        # Add to database
        input_id = str(uuid.uuid1())
        trail_manager.add_input(input_id, length, elevation_gain, route_type,
                                features, activities)
        trail_manager.close()
        logger.info("User input added to database")

        # Predict and recommend
        prediction = predict(length, elevation_gain, route_type, features,
                             activities, **config['recommend']['predict'])
        logger.debug("Web app successfully used prediction function")

        recommend_ids = rec(length, elevation_gain, route_type, features,
                            activities, **config['recommend']['recommend'])
        logger.debug("Web app successfully used recommendation function")

        try:
            trails = trail_manager.session.query(Trails)\
                    .filter(Trails.trail_id.in_(recommend_ids))\
                    .order_by(Trails.length)
            logger.debug("Web app successfully queried from database")
            logger.debug("Index page accessed")
            return render_template('result.html', prediction=prediction,
                                   trails=trails)
        except:
            traceback.print_exc()
            logger.warning("Not able to display trails, error page returned")
            return render_template('error.html')


if __name__ == '__main__':
    app.run(debug=app.config["DEBUG"], port=app.config["PORT"],
            host=app.config["HOST"])
