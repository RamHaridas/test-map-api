from models.user import UserModel
from models.enquiries import EnquiryModel
from models.owner import OwnerModel
from models.vehicle import VehicleModel
from flask_restful import reqparse,Resource
import requests

class EnquiryResource(Resource):
    parser = reqparse.RequestParser()

    parser.add_argument(
        'uid',
        type=int,
        required=True
    )
    parser.add_argument(
        'owner_id',
        type=int,
        required=True
    )
    parser.add_argument(
        'v_id',
        type=int,
        required=True
    )
    parser.add_argument(
        'lat',
        type=float,
        required=False
    )
    parser.add_argument(
        'lon',
        type=float,
        required=False
    )

    def post(self):
        data = EnquiryResource.parser.parse_args()
        vehicle = VehicleModel.find_by_id(data['v_id'])
        owner = OwnerModel.find_by_id(data['owner_id'])
        user = UserModel.find_by_id(data['uid'])
        if vehicle is None:
            return {'message':'vehicle id does not exist'}
        elif owner is None:
            return {'message':'owner id does not exist'}
        elif user is None:
            return {'message':'user id does not exist'}

        message = f"{user.name} recently checked your {vehicle.name}. For Service, You can directly contact for work on {user.mobile}. \n - Hire On Map (App)"
        url = f"http://103.16.142.249/api/mt/SendSMS?user=mdrentals&password=india123&senderid=HIREOM&channel=Trans&DCS=0&flashsms=0&number=91{owner.mobile}&text={message}&route=07"

        r = requests.get(url)
        
        print (message)
        print (r.json())

        enquiry = EnquiryModel(**data)
        enquiry.save_to_db()
        return enquiry.json()

    
    def get(self):
        local = reqparse.RequestParser()
        local.add_argument(
            'owner_id',
            type=int,
            required=False
        )
        local.add_argument(
            'list',
            type=str,
            required=False
        )
        data = local.parse_args()
        if data['owner_id']:
            return {'enquiries':[e.json() for e in EnquiryModel.find_by_owner(data['owner_id'])]}
        elif data['list'] == 'list':
            return {'enquiries':[e.json() for e in EnquiryModel.get_all()]}
			

    def delete(self):
        local = reqparse.RequestParser()

        local.add_argument(
            'id',
            type=int,
            required=True,
            help = 'id is mandatory'
        )

        data = local.parse_args()
        enquiry = EnquiryModel.find_by_id(data['id'])
        if enquiry:
            enquiry.delete_from_db()
            return {'message':'deleted successfully'}
        return {'message':'not found'}
    		
	
