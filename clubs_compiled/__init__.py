import os

from flask import Flask

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        API_KEY=os.path.join(app.instance_path, 'key.json'),
        FORM_ID=os.path.join(app.instance_path, 'form_id.txt')
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from . import views
    app.register_blueprint(views.blueprint)

    return app