import os
from flask import Flask, abort, jsonify, request

from models import setup_db, User, Tag

from flask_cors import CORS


def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)

    CORS(app)

    @app.route("/users", methods=['GET'])
    def get_users():
        page = request.args.get("page", 1, type=int)
        current_index = page - 1

        users = User.query.order_by(User.id)\
            .limit(10) \
            .offset(current_index * 10).all()

        if not users:
            abort(404)

        formatted_users = [user.format() for user in users]

        return jsonify(
            {
                "success": True,
                "users": formatted_users
            }
        )

    @app.route("/users/<int:user_id>", methods=['GET'])
    def get_user_by_id(user_id):
        if not user_id:
            abort(422)

        user = User.query.get(user_id)

        if not user:
            abort(404)

        return jsonify(
            {
                "success": True,
                "user": user.format()
            }
        )

    @app.route("/tags/<int:user_id>", methods=['GET'])
    def get_user(user_id):
        if not user_id:
            abort(422)

        user = User.query.get(user_id)

        return jsonify(
            {
                "success": True,
                "user": user.format()
            }
        )

    return app


app = create_app()

if __name__ == '__main__':
    app.debug = True
    app.run()
