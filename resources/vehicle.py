from flask.globals import request
from flask.helpers import stream_with_context
from flask_restful import reqparse,Resource
from flask_restful.reqparse import RequestParser
from werkzeug.datastructures import FileStorage
from models.vehicle import VehicleModel
from models.vehicles_model import ModelVehicle
from models.owner import OwnerModel
from models.driver import DriverModel     
from models.vehicle_type import VehicleTypeModel
from models.enquiries import EnquiryModel
from models.master_vehicle import MasterVehicleModel      
import os
import sys

class VehicleResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument(
        'name',
        type=str,
        required=True,
        help='vehicle name is mandatory'
    )
    parser.add_argument(
        'vehicle_model_id',
        type=int,
        required=True,
        help='vehicle model id is mandatory'
    )
    parser.add_argument(
        'aadhar',
        type=str,
    )
    parser.add_argument(
        'specialization',
        type=str
    )
    parser.add_argument(
        'yom',
        type=str,
        required=True,
        help='year of manufacturing is mandatory'
    )
    parser.add_argument(
        'total_run_hrs',
        type=int,
        required=False
    )
    parser.add_argument(
        'run_km_hr',
        type=int,
        required=False
    )
    parser.add_argument(
        'fuel_consumption_rate',
        type=int,
        required=False
    )
    parser.add_argument(
        'fuel_average_consumption_rate',
        type=int,
        required=True,
        help='fuel average consumption is mandatory'
    )
    parser.add_argument(
        'rent_per_day_with_fuel',
        type=int,
        required=False
    )
    parser.add_argument(
        'rent_per_hour_with_fuel',
        type=int,
        required=False
    )
    parser.add_argument(
        'rent_per_hour_without_fuel',
        type=int,
        required=False
    )
    parser.add_argument(
        'rent_per_day_without_fuel',
        type=int,
        required=False
    )
    parser.add_argument(
        'owner_id',
        type=int,
        required=True,
        help='Owner id is mandatory'
    )
    parser.add_argument(
        'availibility',
        type=bool,
        required=True,
        help='availibility is mandatory'
    )
    parser.add_argument(
        'ip_address',
        type=str,
        required=True,
        help='ip_address is mandatory'
    )
    parser.add_argument(
        'plate_no',
        type=str,
        required=False
    )
    parser.add_argument(
        'busy_start',
        type=str,
        required=False
    )
    parser.add_argument(
        'busy_end',
        type=str,
        required=False
    )
    parser.add_argument(
        'cost',
        type=str,
        required=False
    )

    def post(self):

        #pic = request.files['vfront']
        data = VehicleResource.parser.parse_args()
        
        if ModelVehicle.find_by_id(data['vehicle_model_id']) is None:
            return {'message':'model does not exist'}

        if OwnerModel.find_by_id(data['owner_id']) is None:
            return {'message':'owner does not exist'}
        
        if VehicleModel.find_by_plate(data['plate_no']):
            return {'message':'same plate number already exist'}

        
        owner = OwnerModel.find_by_id(data['owner_id'])
        count = owner.sub.vehicles_alloted
        vlist = [o for o in VehicleModel.find_vehicle_by_owner(owner_id=data['owner_id'])]

        if len(vlist) == count:
            return {'message':'You have reached your limit for adding vehicles'}

        vehicle = VehicleModel(**data)
        vehicle.save()
        return vehicle.json()

    
    def get(self):
        local = reqparse.RequestParser()
        local.add_argument(
            'id',
            type=int,
            required=False
        )
        local.add_argument(
            'owner_id',
            type=int,
            required=False
        )
        local.add_argument(
            'specialization',
            type=str
        )
        local.add_argument(
            'aadhar',
            type=str
        )
        local.add_argument(
            'list',
            type=str,
            required=False
        )
        local.add_argument(
            'vehicle_image',
            type=int,
            required=False
        )
        local.add_argument(
            'vfront',
            type=int,
            required=False
        )
        local.add_argument(
            'count',
            type=int,
            required=False
        )
        data = local.parse_args()

        if data['vehicle_image']:
            vehicle = VehicleModel.find_by_id(data['vehicle_image'])
            if vehicle:
                return vehicle.get_image()

        if data['count']:
            owner = OwnerModel.find_by_id(data['count'])
            count = owner.sub.vehicles_alloted
            vlist = [o for o in VehicleModel.find_vehicle_by_owner(owner_id=data['count'])]
            return {
                    'count':len(vlist),
                    'alloted':count,
                }
            
        if data['owner_id']:
            return {'vehicles':[v.json() for v in VehicleModel.find_vehicle_by_owner(data['owner_id'])]}
        elif data['vfront']:
            v = VehicleModel.find_by_id(data['vfront'])
            if v:
                return v.get_image(data['vfront'])
        vehicle = VehicleModel.find_by_id(data['id'])
        if vehicle:
            return vehicle.json()
        if data['list'] == 'list':
            return {'vehicles':[v.json() for v in VehicleModel.query.order_by(VehicleModel.added_on.desc()).all()]}

        return {'message':'Please add respective Parameters'}

    
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
            'aadhar',
        )
        local.add_argument(
            'specialization',
            type=str
        )
        local.add_argument(
            'vehicle_model_id',
            type=int,
            required=False
        ) 
        local.add_argument(
            'yom',
            type=str,
            required=False
        )
        local.add_argument(
            'total_run_hrs',
            type=int,
            required=False
        )
        local.add_argument(
            'run_km_hr',
            type=int,
            required=False
        )
        local.add_argument(
            'fuel_consumption_rate',
            type=int,
            required=False
        )
        local.add_argument(
            'fuel_average_consumption_rate',
            type=int,
            required=False
        )
        local.add_argument(
            'rent_per_day_with_fuel',
            type=int,
            required=False
        )
        local.add_argument(
            'rent_per_hour_with_fuel',
            type=int,
            required=False
        )
        local.add_argument(
            'rent_per_day_without_fuel',
            type=int,
            required=False
        )
        local.add_argument(
            'rent_per_hour_without_fuel',
            type=int,
            required=False
        )
        local.add_argument(
            'availibility',
            type=int,
            required=False
        )
        local.add_argument(
            'driver_id',
            type=int,
            required=False
        )
        local.add_argument(
            'plate_no',
            type=str,
            required=False
        )
        local.add_argument(
            'busy_start',
            type=str,
            required=False
        )
        local.add_argument(
            'busy_end',
            type=str,
            required=False
        )
        local.add_argument(
            'cost',
            type=str,
            required=False
        )
        local.add_argument(
            'history',
            type=str,
            required=False
        )
        data = local.parse_args()

        if VehicleModel.find_by_id(data['id']) is None:
            return {'message':'vehicle does not exist'}
        elif data['vehicle_model_id']:
            if ModelVehicle.find_by_id(data['vehicle_model_id']) is None:
                return {'message':'model does not exist'}

        v = VehicleModel.find_by_id(data['id'])
        v.update(**data)
        if data['history']:
            history = HistoryModel(log=data['history'])
            # print(history)
            history.save_to_db()
        return v.json()

    
    def delete(self):
        local = reqparse.RequestParser()
        local.add_argument(
            'id',
            type=int,
            required=True,
            help='id is mandatory'
        )
        data = local.parse_args()
        v = VehicleModel.find_by_id(**data)
        d = DriverModel.find_driver_by_vehicle(data['id'])
        e = EnquiryModel.find_by_vehicle(data['id'])

        if v:
            if d:
                return {'message':'Please remove drivers assigned to this vehicle before deleting.'}
                # for driver in d:
                #     driver.update(vehicle_id=NULL)
            if e:
                for enq in e:
                    enq.delete()
            v.delete()
            return {'message':'deleted successfully'}
        
        return {'message':'does not exist'}



class VehicleMobileResource(Resource):
    
    def get(self):
        local = reqparse.RequestParser()
        local.add_argument(
            'owner_id',
            type=int,
            required=True,
            help='owner id is mandatory'
        )

        data = local.parse_args()

        return {'vehicles':[v.json() for v in VehicleModel.find_vehicle_by_owner(**data)]}


    def patch(self):
        vfront = request.files['vfront']
        local = reqparse.RequestParser()
        local.add_argument(
            'id',
            type=int,
            required=False
        )
        local.add_argument(
            'plate',
            type=str,
            required=False
        )
        if not vfront:
            return {'message':'front image not added'}

        data = local.parse_args()

        vehicle = VehicleModel.find_by_id(data['id'])
        plate = VehicleModel.find_by_plate(data['plate'])
        if vehicle:
            try:
                vehicle.update_vehicle_front(vfront.read(),vfront.filename)
                return {'message':"IMAGES SAVED"}
            except:
                return "ERROR, REDUCE IMAGE SIZE",400
        elif plate:
            try:
                plate.update_vehicle_front(vfront.read(),vfront.filename)
                return {'message':"IMAGES SAVED"}
            except:
                return "ERROR, REDUCE IMAGE SIZE",400

        
        return{'message':'vehicle id not found'}
        

    def post(self):
        vback = request.files['vback']
        local = reqparse.RequestParser()
        local.add_argument(
            'id',
            type=int,
            required=False
        )
        local.add_argument(
            'plate',
            type=str,
            required=False
        )
        if not vback:
            return {'message':'back image not added'}

        data = local.parse_args()

        vehicle = VehicleModel.find_by_id(data['id'])
        plate = VehicleModel.find_by_plate(data['plate'])
        if vehicle:
            try:
                vehicle.update_vehicle_back(vback.read(),vback.filename)
                return {'message':"IMAGES SAVED"}
            except:
                return "ERROR, REDUCE IMAGE SIZE",400
        elif plate:
            try:
                plate.update_vehicle_back(vback.read(),vback.filename)
                return {'message':"IMAGES SAVED"}
            except:
                return "ERROR, REDUCE IMAGE SIZE",400
        
        return{'message':'vehicle id not found'}

    
    def put(self):
        vside = request.files['vside']
        local = reqparse.RequestParser()
        
        local.add_argument(
            'id',
            type=int,
            required=False
        )
        local.add_argument(
            'plate',
            type=str,
            required=False
        )
        if not vside:
            return {'message':'image not added'}
        data = local.parse_args()
        vehicle = VehicleModel.find_by_id(data['id'])
        plate = VehicleModel.find_by_plate(data['plate'])
        if vehicle:
            try:
                vehicle.update_vehicle_side(vside.read(),vside.filename)
                return {'message':"IMAGES SAVED"}
            except:
                return {"message":"please reduce image size"}
        elif plate:
            try:
                plate.update_vehicle_side(vside.read(),vside.filename)
                return {'message':"IMAGES SAVED"}
            except:
                return {"message":"please reduce image size"}

        return{'message':'vehicle id not found'}


class VehicleDocumentResource(Resource):


    @classmethod
    def get_file_size(file):
        stat = os.stat(file)
        size = stat.st_size
        return (round(size / 1024, 3))

    def get(self):
        local = reqparse.RequestParser()
        local.add_argument(
            'vfront',
            type=int,
            required=False
        )
        local.add_argument(
            'vback',
            type=int,
            required=False
        )
        local.add_argument(
            'vside',
            type=int,
            required=False
        )
        local.add_argument(
            'rc',
            type=int,
            required=False
        )
        local.add_argument(
            'insurance',
            type=int,
            required=False
        )
        local.add_argument(
            'invoice',
            type=int,
            required=False
        )

        data = local.parse_args()
        if data['vfront']:
            vehicle = VehicleModel.find_by_id(data['vfront'])
            if(vehicle.vehicle_image_url):
                return vehicle.get_image()
        elif data['vback']:
            vehicle = VehicleModel.find_by_id(data['vback'])
            if(vehicle.vehicle_image_back_url):
                return vehicle.get_back_image()
        elif data['vside']:
            vehicle = VehicleModel.find_by_id(data['vside'])
            if(vehicle.vehicle_image_side_url):
                return vehicle.get_side_image()
        elif data['rc']:
            vehicle = VehicleModel.find_by_id(data['rc'])
            if(vehicle.rc_doc_url):
                return vehicle.get_rc()
        elif data['insurance']:
            vehicle = VehicleModel.find_by_id(data['insurance'])
            if(vehicle.insurance_doc_url):
                return vehicle.get_insurance()
        elif data['invoice']:
            vehicle = VehicleModel.find_by_id(data['invoice'])
            if(vehicle.invoice_doc_url):
                return vehicle.get_invoice()

        return {'message':'Vehicle does not exist'}

    def post(self):
        rc = request.files['rc']
        local = reqparse.RequestParser()
        
        local.add_argument(
            'id',
            type=int,
            required=False
        )
        local.add_argument(
            'plate',
            type=str,
            required=False
        )
        if not rc:
            return {'message':'RC not added'}

        data = local.parse_args()
        vehicle = VehicleModel.find_by_id(data['id'])
        plate = VehicleModel.find_by_plate(data['plate'])
        if vehicle:
            try:
                vehicle.update_rc(rc.read(),rc.filename)
                return {'message':"RC  SAVED"}
            except Exception as e:
                return {"message":str(e)}
        elif plate:
            try:
                plate.update_rc(rc.read(),rc.filename)
                return {'message':"RC  SAVED"}
            except Exception as e:
                return {"message":str(e)}

        return{'message':'vehicle id not found'}


    def put(self):
        invoice = request.files['invoice']
        local = reqparse.RequestParser()

        local.add_argument(
            'id',
            type=int,
            required=False
        )
        local.add_argument(
            'plate',
            type=str,
            required=False
        )
        if not invoice:
            return {'message':'invoice not added'}
        data = local.parse_args()
        vehicle = VehicleModel.find_by_id(data['id'])
        plate = VehicleModel.find_by_plate(data['plate'])
        if vehicle:
            try:
                vehicle.update_invoice(invoice.read(),invoice.filename)
                return {'message':"Invoice  SAVED"}
            except:
                print("Unexpected error:", sys.exc_info()[0])
                return {"message":"please reduce document size"}
        elif plate:
            try:
                plate.update_invoice(invoice.read(),invoice.filename)
                return {'message':"Invoice  SAVED"}
            except:
                return {"message":"please reduce document size"}

        return{'message':'vehicle not found'}        


    def patch(self):
        insurance = request.files['insurance']
        local = reqparse.RequestParser()

        local.add_argument(
            'id',
            type=int,
            required=False
        )
        local.add_argument(
            'plate',
            type=str,
            required=False
        )

        if not insurance:
            return {'message':'insurance not added'}
            
        data = local.parse_args()
        vehicle = VehicleModel.find_by_id(data['id'])
        plate = VehicleModel.find_by_plate(data['plate'])
        if vehicle:
            try:
                vehicle.update_insurance(insurance.read(),insurance.filename)
                return {'message':"Insurance  SAVED"}
            except:
                return {"message":"please reduce document size"}
        elif plate:
            try:
                plate.update_insurance(insurance.read(),insurance.filename)
                return {'message':"Insurance  SAVED"}
            except:
                return {"message":"please reduce document size"}

        return{'message':'vehicle id not found'} 



class VehicleLocation(Resource):
    
    def put(self):
        local = reqparse.RequestParser()
        local.add_argument(
            'lat',
            type=float,
            required=False
        )
        local.add_argument(
            'lon',
            type=float,
            required=False
        )
        local.add_argument(
            'id',
            type=int,
            required=True
        )
        local.add_argument(
            'driver_id',
            type=int,
            required=True
        )
        data = local.parse_args()
        if DriverModel.find_by_id(data['driver_id']) is None:
            return {'message':'driver not found'}

        vehicle = VehicleModel.find_by_id(data['id'])
        if vehicle:
            vehicle.update_location(**data)
            return {'message':'location updated'}
        
        return {'message':'vehicle not found'}


    def get(self):
        local = reqparse.RequestParser()

        local.add_argument(
            'id',
            type=int,
            required=True
        )
        data = local.parse_args()
        vehicle = VehicleModel.find_by_id(data['id'])
        if vehicle:
            return vehicle.get_location()

        return {'message':'vehicle not found'}



class VehicleSearchResource(Resource):

    def get(self):
        local = reqparse.RequestParser()

        local.add_argument(
            'name',
            type=str,
            required=False
        )
        local.add_argument(
            'namelist',
            type=str,
            required=False
        )

        data = local.parse_args()

        if data['namelist'] == 'list':
            names = [m.name if m.name else "" for m in MasterVehicleModel.query.all()]
            names += [t.vehicle_type_name if t.vehicle_type_name else "" for t in VehicleTypeModel.query.all()]
            # names += [v.plate_no if v.plate_no else "" for v in VehicleModel.query.all()]
            return {'names':names}

        master = MasterVehicleModel.find_by_name(data["name"])
        vtype = VehicleTypeModel.find_by_name(data["name"])
        # plate = VehicleModel.find_by_plate(data["name"])
        vmodel = ModelVehicle.find_by_name(data["name"])
        vehicles = []
        if master:
            v_type = VehicleTypeModel.find_by_master(master_id=master.id)
            model = []
            for v in v_type:
                model += [m.id for m in ModelVehicle.find_by_type(vehicle_type_id=v.id)]
            for m in model:
                vehicles += [v.json() for v in VehicleModel.find_by_model(vehicle_model_id=m)]
        elif vtype:
            model = ModelVehicle.find_by_type(vehicle_type_id=vtype.id)
            for m in model:
                vehicles += [v.json() for v in VehicleModel.find_by_model(vehicle_model_id=m.id)]
        elif plate:
            vehicles.append(plate.json())
        
                
        return {'vehicles':vehicles}        
            

