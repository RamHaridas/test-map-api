from flask_restful import Resource,reqparse
from models.master_vehicle import MasterVehicleModel


class MasterVehicleResource(Resource):
    
    parser = reqparse.RequestParser()
    parser.add_argument(
        'name',
        type=str,
        required=True,
        help='name is mandatory'
    )
    parser.add_argument(
        'ip_address',
        type=str,
        required=True,
        help='IP is mandatory'
    )
    parser.add_argument(
        'image_url',
        type=str,
        required=False
    )
    def post(self):
        data = MasterVehicleResource.parser.parse_args()
        if data['name'] in ['',None]:
            return {'message':'Name cant be empty'}

        if MasterVehicleModel.find_by_name(data['name']):
            return {'message':'Name already exists'}

        master = MasterVehicleModel(**data)
        master.save()
        return master.json()

    
    def get(self):

        local = reqparse.RequestParser()
        local.add_argument(
            'id',
            type=int,
            required=False
        )
        data = local.parse_args()
        master = MasterVehicleModel.find_by_id(**data)
        if master:
            return master.json()

        return {'masters':[master.json() for master in MasterVehicleModel.query.all()]}


    def delete(self):
        local = reqparse.RequestParser()
        local.add_argument(
            'id',
            type=int,
            required=False
        )

        data = local.parse_args()
        master = MasterVehicleModel.find_by_id(**data)
        if master:
            master.delete()
            return {'message':'deleted successfully'}

        return {'message':'does not exist'}


    def put(self):
        local = reqparse.RequestParser()
        local.add_argument(
            'id',
            type=int,
            required=True,
            help="ID is mandatory"
        )
        local.add_argument(
            'name',
            type=str,
            required=False
        )
        local.add_argument(
            'status',
            type=bool,
            required=False
        )
        local.add_argument(
            'ip_address',
            type=str,
            required=True,
            help="IP is mandatory"
        )
        local.add_argument(
            'image_url',
            type=str,
            required=False
        )
        data = local.parse_args()

        master = MasterVehicleModel.find_by_id(data['id'])
        if master:
            master.update(**data)
            return master.json()
        return "NOT FOUND", 404