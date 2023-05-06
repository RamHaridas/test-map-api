from flask_restful import Resource,reqparse
from models.admin import AdminModel


class AdminResource(Resource):

    parser = reqparse.RequestParser()

    parser.add_argument(
        'username',
        type=str,
        required=True,
        help='username is mandatory'
    )
    parser.add_argument(
        'password',
        type=str,
        required=True,
        help='password is mandatory'
    )
    parser.add_argument(
        'name',
        type=str,
        required=True,
        help='name is mandatory'
    )
    parser.add_argument(
        'email',
        type=str,
        required=True,
        help='email is mandatory'
    )
    parser.add_argument(
        'ip_address',
        type=str,
        required=True,
        help='ip address is mandatory'
    )
    parser.add_argument(
        'middle_name',
        type=str,
        required=True,
        help='middle_name is mandatory'
    )
    parser.add_argument(
        'last_name',
        type=str,
        required=True,
        help='last name is mandatory'
    )
    parser.add_argument(
        'admin_image',
        type=str,
        required=True,
        help='admin image is mandatory'
    )

    #register admin
    def post(self):
        data = AdminResource.parser.parse_args()

        if AdminModel.find_by_email(data['email']):
            return {'message':'admin alredy registered'}
        elif AdminModel.find_by_username(data['username']):
            return {'message':'username alredy registered'}
            
        admin = AdminModel(**data)
        admin.save_to_db()
        return admin.json()

    #login admin
    def get(self):
        local = reqparse.RequestParser()
        local.add_argument(
            'username',
            type=str,
            required=True,
            help='username is mandatory',
        )
        local.add_argument(
            'password',
            type=str,
            required=True,
            help='password is mandatory'
        )
        data = local.parse_args()
        
        admin = AdminModel.login_admin(**data)
        if admin:
            return admin.json()

        return {'message':'does not exists'}

    #delete admin
    def delete(self):
        local = reqparse.RequestParser()
        local.add_argument(
            'email',
            type=str,
            required=True,
            help='email is mandatory'
        )
        data = local.parse_args()
        
        admin = AdminModel.find_by_email(data['email'])
        if admin:
            admin.delete_from_db()
            return {'message':'deleted succesfully'}

        return {'message':'admin does not exist'}


    def put(self):
        local = reqparse.RequestParser()
        local.add_argument(
            'username',
            type=str,
            required=True,
            help='username is mandatory'
        )
        local.add_argument(
            'name',
            type=str,
            required=False
        )
        local.add_argument(
            'middle_name',
            type=str,
            required=False
        )
        local.add_argument(
            'last_name',
            type=str,
            required=False
        )
        local.add_argument(
            'admin_image',
            type=str,
            required=False
        )
        local.add_argument(
            'ip_address',
            type=str,
            required=True,
            help='IP is mandatory'
        )
        data = local.parse_args()
        admin = AdminModel.find_by_username(data['username'])
        if admin:
            admin.update(**data)
            return admin.json()

        return {'message':'user does not exist'}