from signal import signal, SIGHUP
from flask import Flask
from flask_cors import CORS
from application.ioc_container.container import container


def create_application():
    app = Flask(__name__)
    CORS(app)

    container.setup_components()

    from .routes.debug_routes import debug
    from .routes.domain_routes import domain
    from .routes.model_routes import model
    from .routes.control_routes import control

    app.register_blueprint(debug)
    app.register_blueprint(domain)
    app.register_blueprint(model)
    app.register_blueprint(control)

    signal(SIGHUP, lambda a, b: container.cleanup())

    return app
