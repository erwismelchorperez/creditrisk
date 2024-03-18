from flask import Flask 
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    # crear la aplicación
    app = Flask(__name__)

    app.config.from_object('config.Config')
    db.init_app(app)

    from flask_ckeditor import CKEditor 
    ckeditor = CKEditor(app)

    import locale
    locale.setlocale(locale.LC_ALL, 'es_MX.UTF-8')


    from creditrisk import home
    app.register_blueprint(home.bp)

    from creditrisk import auth
    app.register_blueprint(auth.bp)

    from creditrisk import post
    app.register_blueprint(post.bp)

    from creditrisk import evaluation
    app.register_blueprint(evaluation.bp)

    from .models import User, Post, Entidad
    
    with app.app_context():
        db.create_all()
    
    return app