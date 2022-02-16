import os
from flask import Flask, abort, jsonify, request
from psycopg2 import errors as dbe
from sqlalchemy.exc import IntegrityError

from models import setup_db, User, Tag
from auth.auth import AuthError, requires_auth

from flask_cors import CORS


def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)

    CORS(app)

    @app.route("/users", methods=['GET'])
    @requires_auth("get:users")
    def get_users():
        page = request.args.get("page", 1, type=int)
        current_index = page - 1

        users = User.query.order_by(User.id) \
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

    @app.route('/users', methods=['POST'])
    @requires_auth("post:users")
    def create_user():
        body = request.get_json()

        name = body.get('name', None)
        telephone = body.get('telephone', None)

        if name is None or telephone is None:
            abort(422)

        try:
            user = User(name=name,
                        telephone=telephone)
            user.insert()

            return jsonify({
                'success': True,
                'created': user.format()
            }), 201

        except Exception as e:
            print(e)
            user.rollback()
            abort(422)

    @app.route("/users/<int:user_id>", methods=['GET'])
    @requires_auth("get:users")
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

    @app.route("/users/<int:user_id>", methods=["DELETE"])
    @requires_auth("delete:users")
    def delete_user(user_id):
        user = User.query.filter(User.id == user_id).one_or_none()
        if not user:
            abort(404)

        try:
            user.delete()
        except IntegrityError as e:
            abort(422)

        return jsonify({
            "success": True,
            "delete": user_id
        }), 200

    @app.route("/tags/<int:tag_id>", methods=['GET'])
    @requires_auth("get:tags")
    def get_tag(tag_id):
        if not tag_id:
            abort(422)

        tag = Tag.query.get(tag_id)
        if not tag:
            abort(404)

        return jsonify(
            {
                "success": True,
                "tag": tag.format()
            }
        )

    @app.route('/tags', methods=['POST'])
    @requires_auth("post:tags")
    def create_tag():
        body = request.get_json()

        name = body.get('name', None)
        information = body.get('information', '')
        user_id = body.get('user_id', None)

        if name is None or user_id is None:
            abort(422)

        try:
            tag = Tag(name=name,
                      information=information,
                      user_id=user_id)
            tag.insert()

            return jsonify({
                'success': True,
                'created': tag.format()
            }), 201

        except Exception as e:
            print(e)
            tag.rollback()
            abort(422)

    @app.route("/tags/<int:tag_id>", methods=["PATCH"])
    @requires_auth("patch:tags")
    def patch_tag(tag_id):
        data = request.get_json()
        tag = Tag.query.filter(Tag.id == tag_id).one_or_none()
        if not tag:
            abort(404)

        tag.name = data.get("name", tag.name)
        tag.information = data.get("information", tag.information)
        tag.user_id = data.get("user_id", tag.user_id)

        tag.update()

        return jsonify({
            "success": True,
            "tag": tag.format()
        }), 200

    @app.route("/tags/<int:tag_id>", methods=["DELETE"])
    @requires_auth("delete:tags")
    def delete_tag(tag_id):
        tag = Tag.query.get(tag_id)
        if not tag:
            abort(404)

        tag.delete()

        return jsonify({
            "success": True,
            "delete": tag_id
        }), 200

    @app.route("/qr/<string:tag_id>", methods=['GET'])
    def get_qr_info(tag_id):
        if not tag_id:
            abort(422)

        tag = Tag.query.filter(Tag.tag_id == tag_id).one_or_none()
        if not tag:
            abort(404)

        return jsonify(
            {
                "success": True,
                "tag": tag.format()
            }
        )

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'error': 404,
            'message': 'Not Found'
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            'error': 422,
            'message': 'Unprocessable Entity'
        }), 422

    @app.errorhandler(401)
    def permission_error(error):
        return jsonify({
            "success": False,
            "error": 401,
            "message": "Authentication error"
        }), 401

    @app.errorhandler(AuthError)
    def auth_error(error):
        return jsonify({
            "success": False,
            "error": error.error['code'],
            "message": error.error['description']
        }), error.status_code

    return app


app = create_app()

if __name__ == '__main__':
    app.debug = True
    app.run()
