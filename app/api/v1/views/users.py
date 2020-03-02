"""
    This module holds the views for the users
"""
from flask_restplus import Resource, reqparse, Api
from flask import request, Flask, jsonify
from app.api.v1.models.users import UserModel
from app.api.v1.validators.validators import Validate

app = Flask(__name__)
api = Api(app)


class Users(Resource):
    """
        This class defines methods for getting all users and signing up
    """

    @api.doc(params={
                    'username': 'Enter a unique username',
                    'email': 'Enter email',
                    'phoneNumber': 'Enter phone number',
                    'password': 'Enter password'
                    })
    def post(self):
        """
            This method registers a user to the database.
        """

        parser = reqparse.RequestParser(bundle_errors=True)

        parser.add_argument("username",
                            type=str,
                            required=True,
                            help="Username field is required.")
        parser.add_argument("password",
                            type=str,
                            required=True,
                            help="Password field is required.")
        parser.add_argument("email",
                            type=str,
                            required = True,
                            help="Email field is required.")
        parser.add_argument("phoneNumber",
                            type=int,
                            help="Phone number field is optional.")
        parser.add_argument("role",
                            type=str,
                            help="Role field is optional.")

        self.args = parser.parse_args()
        user = UserModel(**self.args)
        Valid = Validate()
        username = self.args['username'].strip()
        email = self.args['email'].strip()
        password = self.args['password'].strip()
        if not request.json:
            return jsonify({"error" : "check your request type"})
        if not email or not Valid.valid_string(username) or not bool(username) :
            return {"error" : "Username is invalid or empty"}, 400
        if not Valid.valid_email(email) or not bool(email):
            return {"error" : "Email is invalid or empty!"}, 400
        if not Valid.valid_password(password) or not bool(password):
            return {"error" : "Passord is should contain atleast 8 characters, a letter, a number and a special character"}, 400

        if user.find_by_username():
            return {"status": 400,  "error": "Username already in use." }, 400
        user.save_to_db()
        return {"status": 201,
                "data": [
                    {
                        "id": user.id
                    }],
                    "message": 'User created Succesfully.'
                }, 201


class User(Resource):
    """
        This class defines mthods for login in
    """
    @api.doc(params={'Username': 'Enter a unique username',
                    'password': 'Enter password'})
    def post(self):
        """
            This method logs in the user
        """

        parser = reqparse.RequestParser(bundle_errors=True)

        parser.add_argument("username",
                            type=str,
                            required=True,
                            help="Username field is required.")
        parser.add_argument("password",
                            type=str,
                            required=True,
                            help="Password field is required.")
        args = parser.parse_args()
        users = UserModel(**args)
        Valid = Validate()
        username = args['username'].strip()
        password =args['password'].strip()
        if not request.json:
            return jsonify({"error" : "check your request type"})
        if not Valid.valid_string(username) or not bool(username) :
            return {"error" : "Username is invalid or empty"}, 400
        if not Valid.valid_password(password) or not bool(password):
            return {
                "error" : "Passord is should contain atleast 8 characters, a letter, a number and a special character"}, 400
        user = users.find_by_username()
        if user:
            token = users.login_user()
            if token:
                return {"status": 200,
                            "data": [{
                                "token": "Bearer"+" "+token
                            }],
                            "message": "successful"}, 201
            return {"status": 401, "error": "wrong credntials!"}, 401
        return {"status": 404, "error": "user not found"}, 404