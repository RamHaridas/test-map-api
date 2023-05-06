from models.user import UserModel
from models.driver import DriverModel
from models.owner import OwnerModel
from flask_restful import Resource,reqparse


class PasswordResource(Resource):

    #update user password
    def put(self):
        local = reqparse.RequestParser()
        local.add_argument(
            'id',
            type=int,
            required=True
        )
        local.add_argument(
            'password',
            type=str,
            required=True
        )
        local.add_argument(
            'new_password',
            type=str,
            required=True
        )
        data = local.parse_args()

        user = UserModel.find_by_id(data['id'])
        if user:
            return user.update_password(**data)

        return {'message':'user not found'}

        