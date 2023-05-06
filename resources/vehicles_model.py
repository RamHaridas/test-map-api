from flask_restful import Resource,reqparse
from models.vehicles_model import ModelVehicle
from models.vehicle_type import VehicleTypeModel

class VehicleModelResource(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument(
        'vehicle_type_id',
        type=int,
        required=True,
        help='type id is mandatory'
    )
    parser.add_argument(
        'vehicle_model_name',
        type=str,
        required=True,
        help='model name is mandatory'
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

    def post(self):
        data = VehicleModelResource.parser.parse_args()

        if ModelVehicle.find_by_name(data['vehicle_model_name']):
            return {'message':'model with same name alredy exist'}
        elif VehicleTypeModel.find_by_id(data['vehicle_type_id']) is None:
            return {'message':'vehicle type id does not exist'}

        v = ModelVehicle(**data)
        v.save_to_db()
        return v.json()


    def get(self):
        local = reqparse.RequestParser()
        local.add_argument(
            'id',
            type=int,
            required=False
        )
        local.add_argument(
            'vehicle_type_id',
            type=int,
            required=False
        )
        data = local.parse_args()
        v = ModelVehicle.find_by_id(data['id'])
        if v:
            return v.json()
        if data['vehicle_type_id']:
            return {'models':[v.json() for v in ModelVehicle.find_by_type(data['vehicle_type_id'])]}

        models = []
        for v in ModelVehicle.query.all():
            models.append(v.json())
        
        return {'models':models}
    

    def put(self):
        local = reqparse.RequestParser()
        local.add_argument(
            'id',
            type=int,
            required=True,
            help='ID is mandatory'
        )
        local.add_argument(
            'vehicle_type_id',
            type=int,
            required=False
        )
        local.add_argument(
            'vehicle_model_name',
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
            help='ip address is mandatory'
        )

        data = local.parse_args()

        model = ModelVehicle.find_by_id(data['id'])
        if model:
            model.update(**data)
            return model.json()
        
        return {'message':'model name does not exist'},404

    
    def delete(self):
        local = reqparse.RequestParser()
        local.add_argument(
            'id',
            type=int,
            required=True,
            help='id is mandatory'
        )
        data = local.parse_args()
        model = ModelVehicle.find_by_id(**data)
        if model:
            model.delete_from_db()
            return {'message':'deleted successfully'}
        
        return {'message':'model does not exist'}
        

