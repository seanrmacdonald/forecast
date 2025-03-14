import os

from flask import Flask, render_template, request
from .model import MonteCarlo

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    @app.route('/')
    def home():
        return render_template('index.html')
    
    @app.route('/form', methods =["GET", "POST"])
    def form():
        if request.method == "POST":
            config = {
                'initial_value': request.form.get("initial_value"),
                'rate': request.form.get("rate"),
                'years': request.form.get("years")
            }
            monte_carlo = MonteCarlo(100, config)
            monte_carlo_results = monte_carlo.run_simulation()
            combined = {**config, **monte_carlo_results}
            return render_template("results.html", **combined)
        return render_template("forms.html")

    return app