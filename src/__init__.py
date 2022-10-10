from flask import Flask, jsonify
from flask_cors import CORS
from src.config import FlaskConfig
from src.db import create_metadata, session
from flask_jwt_extended import JWTManager
from src.services.user_service import UserService
from flask_caching import Cache

cache = Cache()


def create_app():
    app = Flask(__name__)
    cors = CORS(app=app, resources={"*": {"origins": "*"}}, supports_credentials=True)
    app.config.from_object(FlaskConfig)
    jwt = JWTManager(app)
    cache.init_app(app)

    @app.teardown_appcontext
    def teardown(exception):
        session.close()

    @app.errorhandler(400)
    def error_400(error):
        print("eee", error)

    @app.errorhandler(422)
    def error_422(error):
        headers = error.data.get('headers', None)
        messages = error.data.get('messages', 'Invalid request')
        if 'json' in messages:
            messages = messages['json']
        return jsonify({'message': messages}), 422

    @jwt.token_verification_loader
    def revoked_token(*args):
        return UserService.verification_token(*args)

    @jwt.token_verification_failed_loader
    def verification_jwt_error(*args):
        return jsonify({"message": "Error verification"}), 401

    @jwt.invalid_token_loader
    def invalid_jwt_error(*args):
        return jsonify({"message": "Invalid payload"}), 401

    from src.controllers.Comment.views import comment
    from src.controllers.User.views import user
    from src.controllers.Post.views import posts
    from src.controllers.Member.views import member

    app.register_blueprint(comment, url_prefix=f"{FlaskConfig.URL_PREFIX}/comments")
    app.register_blueprint(user, url_prefix=f"{FlaskConfig.URL_PREFIX}/user")
    app.register_blueprint(posts, url_prefix=f"{FlaskConfig.URL_PREFIX}/posts")
    app.register_blueprint(member, url_prefix=f"{FlaskConfig.URL_PREFIX}/members")

    create_metadata()
    return app



