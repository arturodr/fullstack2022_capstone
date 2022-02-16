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
            })

        except Exception as e:
            print(e)
            user.rollback()
            abort(422)

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

    @app.route("/users/<int:user_id>", methods=["DELETE"])
    def delete_user(user_id):
        user = User.query.filter(User.id == user_id).one_or_none()
        if not user:
            abort(404)

        user.delete()

        return jsonify({
            "success": True,
            "delete": user_id
        }), 200

    @app.route("/users/<int:user_id>", methods=['GET'])
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

    @app.route("/tags/<int:tag_id>", methods=['GET'])
    def get_tag(tag_id):
        if not tag_id:
            abort(422)

        tag = Tag.query.get(tag_id)

        return jsonify(
            {
                "success": True,
                "user": tag.format()
            }
        )

    @app.route('/tags', methods=['POST'])
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
            })

        except Exception as e:
            print(e)
            tag.rollback()
            abort(422)

    @app.route("/tags/<int:tag_id>", methods=["PATCH"])
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
    def delete_tag(tag_id):
        tag = Tag.query.get(tag_id).one_or_none()
        if not tag:
            abort(404)

        tag.delete()

        return jsonify({
            "success": True,
            "delete": tag_id
        }), 200

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

    return app


app = create_app()

if __name__ == '__main__':
    app.debug = True
    app.run()
