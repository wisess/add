from flask import Flask, jsonify
from flask_cors import CORS
from flask import abort
from flask import request
from services import add_role, delete_role, add_user, delete_user, add_role_for_user, delete_user_role, \
    user_is_exist, role_is_exist, update_user_data, get_user_data, get_all_users_data, user_has_role

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

CORS(app)


@app.route('/')
def index():
    return jsonify("This is simple api service")


@app.errorhandler(404)
def not_found(error):
    return jsonify(error=str(error)), 404


@app.route('/api/get_users', methods=['GET'])
def get_users():
    users_data = get_all_users_data()
    return jsonify({"users": users_data})


@app.route('/api/get_user/<user_name>', methods=['GET'])
def get_user_data_by_name(user_name):
    if user_is_exist(user_name) is None:
        abort(404)
    user_data = get_user_data(user_name)
    return jsonify({"user": user_data})


@app.route('/api/add_user', methods=['POST'])
def create_user():
    if not request.json or not ('user_name' in request.json):
        abort(400)
    user_name = request.json['user_name']
    if user_is_exist(user_name):
        return jsonify({'user_name': 'exist'})
    user_phone_number = request.json['phone_number']
    user_role = request.json['role']
    if role_is_exist(user_role) is None:
        abort(400)
    add_user(user_name, user_phone_number, user_role)
    return jsonify({'user_name': user_name}), 201


@app.route('/api/delete_user', methods=['DELETE'])
def delete_user_by_name():
    if not request.json or not ('user_name' in request.json):
        abort(400)
    user_name = request.json['user_name']
    if user_is_exist(user_name) is None:
        abort(400)
    delete_user(user_name)
    return jsonify({'result': True})


@app.route('/api/update_user', methods=['PUT'])
def update_user():
    if not request.json or not ('user_name' in request.json):
        abort(400)
    user_name = request.json['user_name']
    if user_is_exist(user_name) is None:
        abort(400)
    if 'new_user_name' in request.json:
        new_user_name = request.json['new_user_name']
    else:
        new_user_name = user_name
    if 'new_phone_number' in request.json:
        new_user_phone_number = request.json['new_phone_number']
    else:
        new_user_phone_number = ""
    new_data = {"new_user_name": new_user_name, "new_user_phone_number": new_user_phone_number}
    update_user_data(user_name, new_data)
    return jsonify({'user_data': 'updated'})


@app.route('/api/add_user_role', methods=['POST'])
def create_user_role():
    if not request.json or not ('user_name' in request.json):
        abort(400)
    user_name = request.json['user_name']
    if user_is_exist(user_name) is None:
        abort(400)
    user_role = request.json['role']
    if user_has_role(user_name, user_role):
        return jsonify({'user_has_role': True})
    add_role_for_user(user_name, user_role)
    return jsonify({'user_name': user_name, 'new_role': user_role}), 201


@app.route('/api/delete_user_role', methods=['DELETE'])
def delete_user_role_by_name():
    if not request.json or not ('user_name' in request.json):
        abort(400)
    user_name = request.json['user_name']
    if user_is_exist(user_name) is None:
        abort(400)
    user_role = request.json['role']
    if not user_has_role(user_name, user_role):
        return jsonify({'user_has_role': False})
    delete_user_role(user_name, user_role)
    return jsonify({'result': True})


@app.route('/api/add_role', methods=['POST'])
def create_role():
    if not request.json or not ('role_name' in request.json):
        abort(400)
    role_name = request.json['role_name']
    if role_is_exist(role_name):
        return jsonify({'role': 'exist'})
    add_role(role_name)
    return jsonify({'role': role_name}), 201


@app.route('/api/delete_role', methods=['DELETE'])
def delete_role_by_name():
    if not request.json or not ('role_name' in request.json):
        abort(400)
    role_name = request.json['role_name']
    if role_is_exist(role_name) is None:
        abort(400)
    delete_role(role_name)
    return jsonify({'result': True})


if __name__ == '__main__':
    app.run(debug=True)
