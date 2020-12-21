from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

# database structure
class UserModel(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String, nullable = False)
    sex = db.Column(db.String, nullable = False)
    age = db.Column(db.Integer, nullable = True)

    def __repr__(self):
        return f"User(name = {name}, sex = {sex}, age = {age})"

# you want to run this method only once so your database wont be overwriten
# db.create_all()

user_info = reqparse.RequestParser()
user_info.add_argument("name", type=str, help="Name is required", required=True)
user_info.add_argument("sex", type=str, help="Gender is required", required=True)
user_info.add_argument("age", type=int, help="Age")

user_info_update = reqparse.RequestParser()
user_info_update.add_argument("name", type=str, help="Name")
user_info_update.add_argument("sex", type=str, help="Gender")
user_info_update.add_argument("age", type=int, help="Age")

resource_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'sex': fields.String,
    'age': fields.Integer
}

def NoUser(user_id):
    if user_id not in users:
        abort(404, message = "User id does not exist")

class HelloWorld(Resource):
    def get(self, name, age):
        return {"data" : name, "age" : age}
    
    def post(self):
        return {"data" : "Hello World"}

class User(Resource):
    @marshal_with(resource_fields) # it converts return result as a dict of resource_fields
    def get(self, user_id):

        # NoUser(user_id)
        # return users[user_id]

        result = UserModel.query.filter_by(id = user_id).first()
        if not result:
            abort(404, message="User id does not exist")
        return result

    @marshal_with(resource_fields)
    def put(self, user_id):
        args = user_info.parse_args() # read request body as user_info

        # users[user_id] = args
        # return users[user_id], 201

        result = UserModel.query.filter_by(id = user_id).first()
        if result:
            abort(409, message="user id already existed")

        user = UserModel()
        for key, value in args.items():
            if value:
                setattr(user, key, value)
        db.session.add(user)
        db.session.commit()
        return user, 201

    # method for updating the database
    @marshal_with(resource_fields)
    def patch(self, user_id):
        args = user_info_update.parse_args()
        result = UserModel.query.filter_by(id = user_id).first()
        if not result:
            abort(404, message="User info cannot update")


        for key, value in args.items():
            if value:
                setattr(result, key, value)

        db.session.commit()
        return result


    def delete(self, user_id):
        # NoUser(user_id)
        # del users[user_id]

        result = UserModel.query.filter_by(id = user_id).first()
        if not result:
            abort(404, message="User id does not exist")
        
        db.session.delete(result)
        db.session.commit()
        return '', 204


api.add_resource(HelloWorld, "/helloworld/<string:name>/<int:age>")

api.add_resource(User, "/user/<int:user_id>")

if __name__ == "__main__":
    # in production mode, you want to get rid of "debug=True"
    # when "debug=True", server updates automatically when you make changes
    # app.run(debug = True)
    app.run()