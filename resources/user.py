from datetime import date
from models.vehicle import VehicleModel
from flask_restful import Resource,reqparse,request
from models.user import UserModel
from models.vehicles_model import ModelVehicle


class UserResource(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument(
        'name',
        type=str,
        required=False,
    )
    parser.add_argument(
        'email',
        type=str,
        required=False,
    )
    parser.add_argument(
        'password',
        type=str,
        required=False,
    )
    parser.add_argument(
        'mobile',
        type=str,
        required=False,
    )
    parser.add_argument(
        'google_id',
        type=str,
        required=False,
    )
    parser.add_argument(
        'facebook_id',
        type=str,
        required=False,
    )
    parser.add_argument(
        'google_image',
        type=str,
        required=False,
    )
    parser.add_argument(
        'refcode',
        type=str,
        required=False
    )
    #register user
    def post(self):
        pic = request.files['pic']
        data = UserResource.parser.parse_args()
            
        #for google login
        if data['google_id']:
            user = UserModel.login_with_google(data['google_id'])
            if user:
                return user.json()
            user = UserModel(**data,image=pic.read(),image_name=pic.filename)
            user.save_to_db()
            return user.json()

        #for normal registration
        if UserModel.find_by_email(data['email']):
            return {'message':'User with same Email already registered'}
        elif UserModel.find_by_mobile(data['mobile']):
            return{'message':'User with same Mobile Number alredy exists'}
        else:
            if pic is not None:
                user = UserModel(**data,image=pic.read(),image_name=pic.filename)
                user.save_to_db()
                return user.json()

            user = UserModel(**data)
            user.save_to_db()
            return user.json()

    #login user
    def put(self):
        local = reqparse.RequestParser()
        local.add_argument(
            'id',
            type=int,
            required=True,
            help='ID is mandatory'
        )
        local.add_argument(
            'name',
            type=str,
            required=False
        )
        local.add_argument(
            'mobile',
            type=str,
            required=False
        )
        local.add_argument(
            'state',
            type=str,
            required=False
        )
        local.add_argument(
            'district',
            type=str,
            required=False
        )
        data = local.parse_args()
        if UserModel.find_by_mobile(data['mobile']):
            return {'message':'selected mobile number already exists'}
        elif UserModel.find_by_id(data['id']) is None:
            return {'message':'user not found'}

        user = UserModel.find_by_id(data['id'])
        if user:
            user.update(**data)
            return user.json()

        return "USER DOES NOT EXIST",404
    
    
    #get user details
    def get(self):
        local = reqparse.RequestParser()
        local.add_argument(
            'username',
            type=str,
            required=False
        )
        local.add_argument(
            'password',
            type=str,
            required=False
        )
        local.add_argument(
            'google',
            type=str,
            required=False
        )
        local.add_argument(
            'id',
            type=int,
            required=False
        )
        local.add_argument(
            'image',
            type=int,
            required=False
        )
        local.add_argument(
            'list',
            type=str,
            required=False
        )
        data = local.parse_args()
        email = UserModel.login_user(data['username'],data['password'])
        mobile = UserModel.login_with_mobile(data['username'],data['password'])
        if data['id']:
            profile = UserModel.find_by_id(data['id'])
            if profile:
                return profile.json()

        if data['google']:
            google = UserModel.login_with_google(data['google'])
            if google:
                return google.json()
        
        if email:
            return email.json()
        elif mobile:
            return mobile.json()        
        
        if data['image']:
            image = UserModel.find_by_id(data['image'])
            if image:
                return image.image_response()
        
        if data['list'] == 'list':
            return {'users':[u.json() for u in UserModel.query.order_by(UserModel.added_on.desc()).all()]}

        return {'message':'invalid credentials or user does not exists'}
    


    
    def delete(self):
        local = reqparse.RequestParser()
        local.add_argument(
            'id',
            type=int,
            required=True
        )

        data = local.parse_args()

        user = UserModel.find_by_id(**data)
        if user:
            user.delete_from_db()
            return {"message":"DELETED SUCCESSFULLY"}

        return {"message":"DOES NOT EXIST"}
        

    def patch(self):
        # pic = request.files['pic']
        local = reqparse.RequestParser()
        local.add_argument(
            'id',
            type=int,
            required=False
        )
        local.add_argument(
            'mobile',
            type=str,
            required=False
        )
        local.add_argument(
            'password',
            type=str,
            required=False
        )
        local.add_argument(
            'type',
            type=str,
            required=False
        )
        data = local.parse_args()

        if data['type'] == 'password':
            user = UserModel.find_by_mobile(data['mobile'])
            if user:
                user.update_password(data['password'])
                return {'message': 'Password Updated!'}
            else:
                return {'message': 'User not found'}

        # if not pic:
        #     return {"message":"Please Add Photo File"}
        
        # user = UserModel.find_by_id(**data)
        # if user:
        #     user.update_image(pic.read(),pic.filename)
        #     return user.image_response()
        
        return {"message":"USER NOT FOUND"}


class UserSearchResource(Resource):
    parser = reqparse.RequestParser()

    parser.add_argument(
        'model_id',
        type=int,
        required=True
    )
    parser.add_argument(
        'availibility',
        type=int,
        required=True
    )
    parser.add_argument(
        'start_date',
        type=str,
        required=False
    )
    parser.add_argument(
        'end_date',
        type=str,
        required=False
    )
    parser.add_argument(
        'price_start',
        type=str,
        required=False
    )
    parser.add_argument(
        'price_end',
        type=str,
        required=False
    )


    def get(self):
        data = UserSearchResource.parser.parse_args()

        if ModelVehicle.find_by_id(data['model_id']) is None:
            return {'message':'vehicle does not exist'}

        return {'vehicles':[v.json() for v in VehicleModel.find_vehicle_by_filter(**data)]}

            