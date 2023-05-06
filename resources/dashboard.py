from models.appointment import AppointmentModel
from flask_restful import Resource,reqparse
from models.vehicle import VehicleModel
from models.owner import OwnerModel
from models.driver import DriverModel
from models.enquiries import EnquiryModel
from models.subscription import SubscriptionModel
from models.user import UserModel
from models.vehicle_type import VehicleTypeModel
from models.vehicles_model import ModelVehicle
from models.master_vehicle import MasterVehicleModel
from models.history import HistoryModel


class DashboardResource(Resource):
    parser = reqparse.RequestParser()
    
    def get(self):
        local = reqparse.RequestParser()
        local.add_argument(
            'search',
            type=str,
            required=False
        )
        local.add_argument(
            'type',
            type=str,
            required=False
        )
        # local.add_argument(
        #     'vehicle_id',
        #     type=int,
        #     required=False
        # )
        # local.add_argument(
        #     'list',
        #     type=str,
        #     required=False
        # )
        
        data = local.parse_args()

        agencyCount = OwnerModel.query.count()
        subsCount = SubscriptionModel.query.count()
        masterCount = MasterVehicleModel.query.count()
        typeCount = VehicleTypeModel.query.count()
        modelCount = ModelVehicle.query.count()
        vehicleCount = VehicleModel.query.count()
        appointCount = AppointmentModel.query.count()
        driverCount = DriverModel.query.count()
        userCount = UserModel.query.count()
        if data['search']:
            return {
                'agencies':[agency.json() for agency in OwnerModel.search(data['search'])],
                'drivers':[driver.json() for driver in DriverModel.search(data['search'])],
                'vehicles':[vehicle.json() for vehicle in VehicleModel.search(data['search'])]
            }

        if data['type'] == 'history':
            return {
                'history': [history.json() for history in HistoryModel.query.order_by(HistoryModel.created_on.desc()).all()]
            }

        # elif data['vehicle_id']:
        #     return {'appointments':[app.json() for app in AppointmentModel.get_by_vehicle(data['vehicle_id'])]}
        
        # if data['list'] == 'list':
        return {
            'agencies': agencyCount,
            'subs': subsCount,
            'masters': masterCount,
            'types': typeCount,
            'models': modelCount,
            'vehicles': vehicleCount,
            'appointments': appointCount,
            'drivers': driverCount,
            'users': userCount
        }

        # return {'message':'no appointments'}
