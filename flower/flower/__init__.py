from flask import Flask
import os
import socket


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flower.sqlite'))
    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    print('当前ip：', socket.gethostbyname(socket.gethostname()))
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    @app.template_filter('split')
    def reverse_filter(s):
        return s.split('|')[:-1]

    app.config['JSON_AS_ASCII'] = False

    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import flower
    app.register_blueprint(flower.bp)

    from . import blog
    app.register_blueprint(blog.bp)
    return app
