from models.appointment import AppointmentModel
from flask_restful import Resource,reqparse
from models.vehicle import VehicleModel
from models.owner import OwnerModel


class AppointmentResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'customer_name',
        type=str,
        required=True
    )
    parser.add_argument(
        'address',
        type=str,
        required=True
    )
    parser.add_argument(
        'customer_mobile',
        type=str,
        required=True
    )
    parser.add_argument(
        'alternate_mobile',
        type=str,
        required=True
    )
    parser.add_argument(
        'owner_id',
        type=int,
        required=True
    )
    parser.add_argument(
        'vehicle_id',
        type=int,
        required=True
    )
    parser.add_argument(
        'start',
        type=str,
        required=True
    )
    parser.add_argument(
        'end',
        type=str,
        required=True
    )
    parser.add_argument(
        'time',
        type=str,
        required=True
    )

    def post(self):
        data = AppointmentResource.parser.parse_args()

        if OwnerModel.find_by_id(data['owner_id']) is None:
            return {'message':'owner not found'}
        elif VehicleModel.find_by_id(data['vehicle_id']) is None:
            return {'message':'vehicle not found'}

        app = AppointmentModel(**data)
        app.save_to_db()
        return app.json()

    
    def get(self):
        local = reqparse.RequestParser()
        local.add_argument(
            'owner_id',
            type=int,
            required=False
        )
        local.add_argument(
            'vehicle_id',
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
            return {'appointments':[app.json() for app in AppointmentModel.get_by_owner(data['owner_id'])]}
        elif data['vehicle_id']:
            return {'appointments':[app.json() for app in AppointmentModel.get_by_vehicle(data['vehicle_id'])]}
        
        if data['list'] == 'list':
            return {'appointments':[app.json() for app in AppointmentModel.query.all()]}

        return {'message':'no appointments'}


    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument(
            'id',
            type=int,
            required=True
        )
        parser.add_argument(
            'customer_name',
            type=str,
            required=False
        )
        parser.add_argument(
            'address',
            type=str,
            required=False
        )
        parser.add_argument(
            'customer_mobile',
            type=str,
            required=False
        )
        parser.add_argument(
            'alternate_mobile',
            type=str,
            required=False
        )
        parser.add_argument(
            'owner_id',
            type=int,
            required=False
        )
        parser.add_argument(
            'vehicle_id',
            type=int,
            required=False
        )
        parser.add_argument(
            'start',
            type=str,
            required=False
        )
        parser.add_argument(
            'end',
            type=str,
            required=False
        )
        parser.add_argument(
            'time',
            type=str,
            required=False
        )
        data = parser.parse_args()

        if OwnerModel.find_by_id(data['owner_id']) is None:
            return {'message':'owner not found'}
        elif VehicleModel.find_by_id(data['vehicle_id']) is None:
            return {'message':'vehicle not found'}

        app = AppointmentModel.find_by_id(data['id'])  
        if app:
            app.update(**data)
            return app.json()

        return {'message':'appointment not found'}


    def delete(self):
        local = reqparse.RequestParser()
        local.add_argument(
            'id',
            type=int,
            required=True
        )

        data = local.parse_args()
        
        app = AppointmentModel.find_by_id(**data)

        if app:
            app.delete_from_db()
            return {'message':'Deletd Successfully'}

        return {'message':'Not found'}