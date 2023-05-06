from flask_restful import Resource,reqparse
from models.vehicle_type import VehicleTypeModel
from models.master_vehicle import MasterVehicleModel


class VehicleTypeResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'master_id',
        type=int,
        required=True,
        help='master id is mandatory'
    )
    parser.add_argument(
        'vehicle_type_name',
        type=str,
        required=True,
        help='name is mandatory'
    )
    parser.add_argument(
        'status',
        type=bool,
        required=True,
        help='status is mandatory'
    )
    parser.add_argument(
        'ip_address',
        type=str,
        required=True,
        help='ip address is mandatory'
    )
    parser.add_argument(
        'image_url',
        type=str,
        required=False
    )
    
    def post(self):
        data = VehicleTypeResource.parser.parse_args()

        if VehicleTypeModel.find_by_name(data['vehicle_type_name']):
            return {'message':'same type name already exist'}

        vehicle = VehicleTypeModel(**data)
        vehicle.save_to_db()
        return vehicle.json()

    def get(self):
        local = reqparse.RequestParser()
        local.add_argument(
            'id',
            type=int,
            required=False,
        )
        local.add_argument(
            'master_id',
            type=int,
            required=False,
        )
        data = local.parse_args()
        if data['id']:
            v = VehicleTypeModel.find_by_id(data['id'])
            return v.json()
        elif data['master_id']:
            return {'masters':[v.json() for v in VehicleTypeModel.find_by_master(data['master_id'])]}


        return {'types':[v.json() for v in VehicleTypeModel.query.all()]}
    
    def put(self):
        local = reqparse.RequestParser()
        local.add_argument(
            'id',
            type=int,
            required=True,
            help='id is mandatory'
        )
        local.add_argument(
            'vehicle_type_name',
            type=str,
            required=False
        )
        local.add_argument(
            'status',
            type=bool,
            required=False,
        )
        local.add_argument(
            'master_id',
            type=int,
            required=False,
        )
        local.add_argument(
            'ip_address',
            type=str,
            required=True,
            help='ip address is mandatory'
        )
        local.add_argument(
            'image_url',
            type=str,
            required=False
        )
        data = local.parse_args()
        if data['master_id']:
            if MasterVehicleModel.find_by_id(data['master_id']) is None:
                return {'message':'master id does not exist'}
        v = VehicleTypeModel.find_by_id(data['id'])
        if v:
            v.update(**data)
            return v.json()

        return {'message':'vehicle type does not exist'}

    def delete(self):
        local = reqparse.RequestParser()
        local.add_argument(
            'id',
            type=int,
            required=True
        )
        data = local.parse_args()
        vtype = VehicleTypeModel.find_by_id(**data)
        if vtype:
            vtype.delete_from_db()
            return "DELETED SUCCESSFULLY"
        return "NOT FOUND",404