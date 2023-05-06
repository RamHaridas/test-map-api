from flask.globals import request
from flask_restful import Resource,reqparse
from models.owner import OwnerModel
from models.subscription import SubscriptionModel
from models.history import HistoryModel


class OwnerResource(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument(
        'email',
        type=str,
        required=False,
        help='email is mandatory'
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
        'mobile',
        type=str,
        required=False,
        help='mobile number is mandatory'
    )
    parser.add_argument(
        'ip_address',
        type=str,
        required=True,
        help='IP is mandatory'
    )
    parser.add_argument(
        'sub_id',
        type=int,
        required=True,
        help='sub id is mandatory'
    )
    parser.add_argument(
        'full_address',
        type=str,
        required=True,
        help='address is mandatory'
    )
    parser.add_argument(
        'pin_code',
        type=str,
        required=False,
    )
    parser.add_argument(
        'pan',
        type=str,
        required=False,
        help='PAN is mandatory'
    )
    parser.add_argument(
        'tan',
        type=str,
        required=False,
    )
    parser.add_argument(
        'gst',
        type=str,
        required=False,
    )
    parser.add_argument(
        'gumasta',
        type=str,
        required=False
    )
    parser.add_argument(
        'mobile2',
        type=str,
        required=False
    )
    parser.add_argument(
        'state',
        type=str,
        required=True,
        help='State is mandatory'
    )
    parser.add_argument(
        'city',
        type=str,
        required=True,
        help='city is mandatory'
    )
    parser.add_argument(
        'tehsil',
        type=str,
        required=False
    )

    parser.add_argument(
        'refcode',
        type=str,
        required=False
    )

    def post(self):
        data = OwnerResource.parser.parse_args()

        if SubscriptionModel.find_by_id(data['sub_id']) is None:
            return {'message':'seubscription does not exist'}

        if OwnerModel.find_by_email(data['email']):
            return {'message':'owner alredy registered'}
        elif OwnerModel.find_by_number(data['mobile']):
            return {'message':'owner alredy registered'}

        owner = OwnerModel(**data)
        owner.save_to_db()
        return owner.json()


    def get(self):
        local = reqparse.RequestParser()
        local.add_argument(
            'email',
            type=str,
            required=False,
        )
        local.add_argument(
            'password',
            type=str,
            required=False
        )
        local.add_argument(
            'list',
            type=str,
            required=False
        )
        local.add_argument(
            'image',
            type=int,
            required=False
        )
        local.add_argument(
            'id',
            type=int,
            required=False
        )

        data = local.parse_args()

        if data['image']:
            owner = OwnerModel.find_by_id(data['image'])
            if owner:
                return owner.json()
        if data['id']:
            owner = OwnerModel.find_by_id(data['id'])
            if owner:
                return owner.json()

        owner = OwnerModel.login_owner(data['email'],data['password'])
        if owner:
            return owner.json()

        if data['list'] == 'list':
            return {'owners':[o.json() for o in OwnerModel.query.order_by(OwnerModel.added_on.desc()).all()]} 

        return {'message':'Does not Exists'}

    
    def delete(self):
        local = reqparse.RequestParser()
        local.add_argument(
            'id',
            type=int,
            required=True,
            help='ID is mandatory'
        )
        data = local.parse_args()
        owner = OwnerModel.find_by_id(**data)
        if owner:
            owner.delete_from_db()
            return {'message':'deleted successfully'}
        
        return {'message':'does not exist'}
        
    
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
            'ip_address',
            type=str,
            required=False
        )
        local.add_argument(
            'pin_code',
            type=str,
            required=False
        )
        local.add_argument(
            'full_address',
            type=str,
            required=False
        )
        local.add_argument(
            'password',
            type=str,
            required=False
        )
        local.add_argument(
            'pan',
            type=str,
            required=False
        )
        local.add_argument(
            'tan',
            type=str,
            required=False
        )
        local.add_argument(
            'gst',
            type=str,
            required=False
        )
        local.add_argument(
            'gumasta',
            type=str,
            required=False
        )
        local.add_argument(
            'mobile',
            type=str,
            required=False
        )
        local.add_argument(
            'email',
            type=str,
            required=False
        )
        local.add_argument(
            'mobile2',
            type=str,
            required=False
        )
        local.add_argument(
            'state',
            type=str,
            required=False
        )
        local.add_argument(
            'city',
            type=str,
            required=False
        )
        local.add_argument(
            'tehsil',
            type=str,
            required=False
        )
        local.add_argument(
            'status',
            type=int,
            required=False
        ) 
        local.add_argument(
            'history',
            type=str,
            required=False
        )
        data = local.parse_args()

        owner = OwnerModel.find_by_id(data['id'])
        if owner:
            owner.update_for_user(**data)
            
            if data['history']:
                history = HistoryModel(log=data['history'])
                # print(history)
                history.save_to_db()

            return owner.json()

        return {'message':'owner does not exist'}

    
    def patch(self):
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
            owner = OwnerModel.find_by_number(data['mobile'])
            if owner:
                owner.update_password(data['password'])
                return {'message': 'Password Updated!'}
            else:
                return {'message': 'Agency/Owner not found'}

        owner = OwnerModel.find_by_id(**data)

        if owner:
            owner.validity()
            return {'message':'Renewed'}
        return {'message':'Agency/Owner not found'}



class OwnerDocs(Resource):
    
    def post(self):
        local = reqparse.RequestParser()
        local.add_argument(
            'id',
            type=int,
            required=False
        )
        local.add_argument(
            'email',
            type=str,
            required=False
        )

        pic = request.files['image']

        if not pic:
            return {'message':'Image not added'}
        data = local.parse_args()
        oid = OwnerModel.find_by_id(data['id'])
        email = OwnerModel.find_by_email(data["email"])

        if oid:
            try:
                oid.update_pan(pan=pic.read(),pan_filename=pic.filename)
            except:
                return{'message':'image size too large'}
            return{'message':'PAN Image Saved'}
        elif email:
            try:
                email.update_pan(pan=pic.read(),pan_filename=pic.filename)
            except:
                return{'message':'image size too large'}
            return{'message':'PAN Image Saved'}

        return {'message':'owner not found'}
        
    
    def put(self):
        local = reqparse.RequestParser()
        local.add_argument(
            'id',
            type=int,
            required=False
        )
        local.add_argument(
            'email',
            type=str,
            required=False
        )

        pic = request.files['address_proof']

        if not pic:
            return {'message':'Image not added'}
        data = local.parse_args()
        oid = OwnerModel.find_by_id(data['id'])
        email = OwnerModel.find_by_email(data["email"])

        if oid:
            try:
                oid.update_address_proof(address_proof=pic.read(),address_proof_filename=pic.filename)
            except:
                return{'message':'image size too large'}
            return{'message':'Adress Proof Image Saved'}
        elif email:
            try:
                email.update_address_proof(address_proof=pic.read(),address_proof_filename=pic.filename)
            except:
                return{'message':'image size too large'}
            return{'message':'Address proof Image Saved'}

        
        return{'message':'owner not found'}


    
    def get(self):
        local = reqparse.RequestParser()
        local.add_argument(
            'pan',
            type=int,
            required=False
        )
        local.add_argument(
            'address_proof',
            type=int,
            required=False
        )

        data = local.parse_args()

        if data['pan']:
            owner = OwnerModel.find_by_id(data['pan'])
            if owner:
                if owner.pan_file_url:
                    return owner.get_pan()
        elif data['address_proof']:
            owner = OwnerModel.find_by_id(data['address_proof'])
            if owner:
                if owner.address_proof_url:
                    return owner.get_address_proof()

        return {'message':'Owner not found'}


    