from flask import Flask


def create_app(): # Create app using Flask with .env configurations
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')
    

    with app.app_context():
        # Importing of modules
        from .views import view
        from .filters import _slice
        from .database import DataBase

        # Registering of 'views.py' which handles all web routes
        app.register_blueprint(view, url_prefix="/")

        # Registering of processor that slices Flask templates
        @app.context_processor
        def slice():
            return dict(slice=_slice)

        return app
