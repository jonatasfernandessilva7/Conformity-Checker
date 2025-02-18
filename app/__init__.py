from flask import Flask


def create_app():
    """Inicializa e configura a aplicação Flask."""
    app = Flask(__name__)

    with app.app_context():
        from app.main import app as main_blueprint
        app.register_blueprint(main_blueprint)

    return app
