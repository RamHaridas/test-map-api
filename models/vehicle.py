from io import BytesIO
from flask.helpers import send_file
from flask_restful import Resource
from db import db
from flask import send_file,request
from datetime import date, datetime
from pytz import timezone
from models.vehicles_model import ModelVehicle
from models.vehicle_type import VehicleTypeModel
import urllib
import base64
import boto3
import uuid

class VehicleModel(db.Model):
    __tablename__ = 'vehicle_tbl'
        
    session = boto3.session.Session()
    client = session.client('s3', region_name='fra1', endpoint_url='https://fra1.digitaloceanspaces.com', aws_access_key_id='42JV7NAFNKRDF55WPPMW', aws_secret_access_key='aUzFHhgW8MEUQ0RWawV7a/M40VlSfCOqC50ThRhUC48')

    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(80))
    vehicle_model_id = db.Column(db.Integer,db.ForeignKey('vehicle_model_tbl.id'))
    model = db.relationship("ModelVehicle",backref=db.backref('vehicle_model_tbl',uselist=False)) #backref to model table
    yom = db.Column(db.String(80))
    total_run_hrs = db.Column(db.Integer)
    run_km_hr = db.Column(db.Integer)
    fuel_consumption_rate = db.Column(db.Integer)
    fuel_average_consumption_rate = db.Column(db.Integer)
    #vehicle images front,back and side
    # vehicle_image = db.Column(db.LargeBinary)
    vehicle_image_name = db.Column(db.String(length=None))
    vehicle_image_url = db.Column(db.String(length=None))
    # vehicle_image_back = db.Column(db.LargeBinary)
    vehicle_image_back_name = db.Column(db.String(length=None))
    vehicle_image_back_url = db.Column(db.String(length=None))
    # vehicle_image_side = db.Column(db.LargeBinary)
    vehicle_image_side_name = db.Column(db.String(length=None))
    vehicle_image_side_url = db.Column(db.String(length=None))
    #rent
    rent_per_day_with_fuel = db.Column(db.Integer)
    rent_per_hour_with_fuel = db.Column(db.Integer)
    rent_per_day_without_fuel = db.Column(db.Integer)
    rent_per_hour_without_fuel = db.Column(db.Integer)
    owner_id = db.Column(db.Integer,db.ForeignKey('owners.id'))
    owner_rel = db.relationship('OwnerModel',backref=db.backref('owners',uselist=False)) ##backref to owner table
    availibility = db.Column(db.Boolean)
    status = db.Column(db.Boolean)
    added_on = db.Column(db.DateTime,default=datetime.utcnow())
    modified_on = db.Column(db.DateTime)
    ip_address = db.Column(db.String(length=None))
    driver_id = db.Column(db.Integer,nullable=True)  #not necessary
    lat = db.Column(db.Float)
    lon = db.Column(db.Float)
    rotation = db.Column(db.Float)
    plate_no = db.Column(db.String(80),unique=True)
    aadhar = db.Column(db.String(30), unique=True)
    specialization = db.Column(db.String(80))
    #new
    # rc_doc = db.Column(db.LargeBinary)
    rc_doc_name = db.Column(db.String(length=None))
    rc_doc_url = db.Column(db.String(length=None))
    # invoice_doc = db.Column(db.LargeBinary)
    invoice_doc_name = db.Column(db.String(length=None))
    invoice_doc_url = db.Column(db.String(length=None))
    # insurance_doc = db.Column(db.LargeBinary)
    insurance_doc_name = db.Column(db.String(length=None))
    insurance_doc_url = db.Column(db.String(length=None))
    #for appointment
    busy_start = db.Column(db.String(80),nullable=True)
    busy_end = db.Column(db.String(80),nullable=True)
    #last moment changes are not appreciated that's why all of this look like a mess
    cost = db.Column(db.String(100))   #for specifying cost of vehicle

    def __init__(self,name,specialization, aadhar, vehicle_model_id,yom,total_run_hrs,run_km_hr,fuel_consumption_rate,fuel_average_consumption_rate,rent_per_day_with_fuel,rent_per_hour_with_fuel,rent_per_day_without_fuel,rent_per_hour_without_fuel,owner_id,availibility,ip_address,busy_start,busy_end,plate_no,cost):
        self.name = name
        self.vehicle_model_id = vehicle_model_id
        self.yom = yom
        self.total_run_hrs = total_run_hrs
        self.run_km_hr = run_km_hr
        self.fuel_consumption_rate = fuel_consumption_rate
        self.fuel_average_consumption_rate = fuel_average_consumption_rate
        self.rent_per_day_with_fuel = rent_per_day_with_fuel
        self.rent_per_day_without_fuel = rent_per_day_without_fuel
        self.rent_per_hour_with_fuel = rent_per_hour_with_fuel
        self.rent_per_hour_without_fuel = rent_per_hour_without_fuel
        self.owner_id = owner_id
        self.aadhar = aadhar
        self.specialization = specialization
        self.availibility = availibility
        self.ip_address = ip_address
        if plate_no:
            self.plate_no = plate_no
        if cost:
            self.cost = cost
        self.modified_on = datetime.utcnow()
        self.added_on = datetime.utcnow()
        if busy_start:
            self.busy_start = busy_start
        if busy_end:
            self.busy_end = busy_end


    def json(self):
        #all of these lines looks like a messa because of dynamic changes being introduced in between development cycle
        local = self.added_on.astimezone(timezone('Asia/Kolkata'))
        local2 = self.modified_on.astimezone(timezone('Asia/Kolkata'))
        modified = local2.strftime('%d/%m/%Y, %H:%M:%S') 
        added = local.strftime('%d/%m/%Y, %H:%M:%S')
        image = False
        doc = False
        if self.vehicle_image_url is None and self.vehicle_image_back_url is None and self.vehicle_image_side_url is None:
            image = True
        
        # if self.rc_doc is None or self.insurance_doc is None or self.invoice_doc is None:
        #     doc = True

        str_status = 'inactive'
        str_avail = 'busy'
        if self.status:
            str_status = 'active'
        if self.availibility:
            str_avail = 'free'
        url = ""
        if self.lat not in [None,0.0]:
            url = "https://www.google.com/maps/search/?api=1&query="+str(self.lat)+","+str(self.lon)
        cost = ""
        if self.cost:
            cost = self.cost

        modelname = ""
        ownername  = ""
        onwermobile = ""
        if self.model:
            modelname = self.model.vehicle_model_name
        if self.owner_rel:
            ownername = self.owner_rel.name
            onwermobile = self.owner_rel.mobile

        types = VehicleTypeModel.find_by_master(13)
        masters = []
        
        is_service = False

        for t in types:
            models = ModelVehicle.find_by_type(t.id)
            for model in models:
                masters.append(model.id)

        if self.vehicle_model_id in masters:
            is_service = True 

        return {
            'v_id':self.id,
            'name':self.name,
            'added_on':added,
            'modified_on':modified,
            'vehicle_model_id':self.vehicle_model_id,
            'model_name':modelname,
            'year_of_man':self.yom,
            'total_run_hrs':self.total_run_hrs,
            'run_km_hr':self.run_km_hr,
            'fuel_consumption':self.fuel_consumption_rate,
            'average_fuel_consumption':self.fuel_average_consumption_rate,
            'rent_per_day_with_fuel':self.rent_per_day_with_fuel,
            'rent_per_hour_with_fuel':self.rent_per_hour_with_fuel,
            'rent_per_hour_without_fuel':self.rent_per_hour_without_fuel,
            'rent_per_day_without_fuel':self.rent_per_day_without_fuel,
            'owner_id':self.owner_id,
            'owner_name':ownername,
            'specialization': self.specialization,
            'aadhar': self.aadhar,
            'owner_mobile':onwermobile,
            'rent_cost':cost,
            'availibility':self.availibility,
            'driver_id':self.driver_id,
            'lat':self.lat,
            'long':self.lon,
            'rotation':self.rotation,
            'plate_no':self.plate_no,
            'busy_start':self.busy_start,
            'busy_end':self.busy_end,
            'isService':is_service,
            'isDocument':doc,
            'isImage':image,
            'location':url,
            'image_url':self.vehicle_image_url,
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        
    def update(self,id,name,aadhar, specialization, vehicle_model_id,yom,total_run_hrs,run_km_hr,fuel_consumption_rate,fuel_average_consumption_rate,rent_per_day_with_fuel,rent_per_hour_with_fuel,rent_per_day_without_fuel,rent_per_hour_without_fuel,availibility,driver_id,plate_no,busy_start,busy_end,cost,history):
        #self.modified_on = datetime.utcnow()
        check = ['',0,None,True,False]
        if name not in check:
            self.name = name
        if vehicle_model_id not in check:
            self.vehicle_model_id = vehicle_model_id
        if yom not in check:
            self.yom = yom
        if total_run_hrs not in check:
            self.total_run_hrs = total_run_hrs
        if run_km_hr not in check:
            self.run_km_hr = run_km_hr
        if fuel_consumption_rate not in check:
            self.fuel_consumption_rate = fuel_consumption_rate
        if fuel_average_consumption_rate not in check:
            self.fuel_average_consumption_rate = fuel_average_consumption_rate
        if rent_per_day_with_fuel not in check:
            self.rent_per_day_with_fuel = rent_per_day_with_fuel
        if rent_per_hour_with_fuel not in check:
            self.rent_per_hour_with_fuel = rent_per_hour_with_fuel
        if rent_per_day_without_fuel not in check:
            self.rent_per_day_without_fuel = rent_per_day_without_fuel
        if rent_per_hour_without_fuel not in check:
            self.rent_per_hour_without_fuel = rent_per_hour_without_fuel
        if availibility == 0:
            self.availibility = False
        if availibility == 1:
            self.availibility = True
        if driver_id not in check:
            self.driver_id = driver_id
        if plate_no not in check:
            self.plate_no = plate_no
        if busy_start not in check:
            self.busy_start = busy_start
        if busy_end not in check:
            self.busy_end = busy_end
        if cost:
            self.cost = cost
        if aadhar:
            self.aadhar = aadhar
        if specialization:
            self.specialization = specialization
        self.modified_on = datetime.utcnow()
        db.session.commit()

    def get_image(self):
        name = "image.jpg"
        if self.vehicle_image_name:
            name = self.vehicle_image_name
        contents = urllib.request.urlopen(self.vehicle_image_url).read()
        data = base64.b64decode(base64.b64encode(contents))
        return send_file(BytesIO(data),as_attachment=False,attachment_filename=name)

    def get_back_image(self):
        name = "image.jpg"
        if self.vehicle_image_back_name:
            name = self.vehicle_image_back_name
        contents = urllib.request.urlopen(self.vehicle_image_back_url).read()
        data = base64.b64decode(base64.b64encode(contents))
        return send_file(BytesIO(data),as_attachment=False,attachment_filename=name)

    def get_side_image(self):
        name = "image.jpg"
        if self.vehicle_image_side_name:
            name = self.vehicle_image_side_name
        contents = urllib.request.urlopen(self.vehicle_image_side_url).read()
        data = base64.b64decode(base64.b64encode(contents))
        return send_file(BytesIO(data),as_attachment=False,attachment_filename=name)

    def get_rc(self):
        name = "image.jpg"
        if self.rc_doc_name:
            name = self.rc_doc_name
        contents = urllib.request.urlopen(self.rc_doc_url).read()
        data = base64.b64decode(base64.b64encode(contents))
        return send_file(BytesIO(data),as_attachment=False,attachment_filename=name)

    def get_invoice(self):
        name = "image.jpg"
        if self.invoice_doc_name:
            name = self.invoice_doc_name
        contents = urllib.request.urlopen(self.invoice_doc_url).read()
        data = base64.b64decode(base64.b64encode(contents))
        return send_file(BytesIO(data),as_attachment=False,attachment_filename=name)

    def get_insurance(self):
        name = "image.jpg"
        if self.insurance_doc_name:
            name = self.insurance_doc_name
        contents = urllib.request.urlopen(self.insurance_doc_url).read()
        data = base64.b64decode(base64.b64encode(contents))
        return send_file(BytesIO(data),as_attachment=False,attachment_filename=name)


    def update_location(self,id,lat,lon,driver_id):
        self.lat = lat
        self.lon = lon
        self.driver_id = driver_id
        db.session.commit()

    def get_location(self):
        id = ""
        if self.driver_id:
            id = self.driver_id
        return{
            'driver_id':id,
            'lat':self.lat,
            'lon':self.lon,
            'v_id':self.id
        }

    def update_current_driver(self,driver_id):
        self.driver_id = driver_id
        db.session.commit()

    def update_vehicle_front(self,vehicle_front,vehicle_front_name):
        # self.vehicle_image = vehicle_front
        filename = f'vehicles/{self.id}/{str(uuid.uuid4().hex)}.png'
        self.client.put_object(Body=base64.b64decode(base64.b64encode(vehicle_front)), Bucket='hire-on-map', Key=filename, ContentType='image/png', ACL='public-read')
        self.vehicle_image_url = f'https://hire-on-map.fra1.digitaloceanspaces.com/{filename}'
        self.vehicle_image_name = vehicle_front_name
        db.session.commit()

    def update_vehicle_back(self,vehicle_back_image,vehicle_back_image_name):
        # self.vehicle_image_back = vehicle_back_image
        filename = f'vehicles/{self.id}/{str(uuid.uuid4().hex)}.png'
        self.client.put_object(Body=base64.b64decode(base64.b64encode(vehicle_back_image)), Bucket='hire-on-map', Key=filename, ContentType='image/png', ACL='public-read')
        self.vehicle_image_back_url = f'https://hire-on-map.fra1.digitaloceanspaces.com/{filename}'
        self.vehicle_image_back_name = vehicle_back_image_name
        db.session.commit()

    def update_vehicle_side(self,vehicle_side_image,vehicle_side_image_name):
        # self.vehicle_image_side = vehicle_side_image
        filename = f'vehicles/{self.id}/{str(uuid.uuid4().hex)}.png'
        self.client.put_object(Body=base64.b64decode(base64.b64encode(vehicle_side_image)), Bucket='hire-on-map', Key=filename, ContentType='image/png', ACL='public-read')
        self.vehicle_image_side_url = f'https://hire-on-map.fra1.digitaloceanspaces.com/{filename}'        
        self.vehicle_image_side_name = vehicle_side_image_name
        db.session.commit()
    
    def update_rc(self,rc,rc_name):
        # self.rc_doc = rc
        filename = f'vehicles/{self.id}/{str(uuid.uuid4().hex)}.png'
        self.client.put_object(Body=base64.b64decode(base64.b64encode(rc)), Bucket='hire-on-map', Key=filename, ContentType='image/png', ACL='public-read')
        self.rc_doc_url = f'https://hire-on-map.fra1.digitaloceanspaces.com/{filename}'        
        self.rc_doc_name = rc_name
        db.session.commit()

    def update_invoice(self,invoice,invoice_name):
        # self.invoice_doc = invoice
        # print(client)
        filename = f'vehicles/{self.id}/{str(uuid.uuid4().hex)}.png'
        self.client.put_object(Body=base64.b64decode(base64.b64encode(invoice)), Bucket='hire-on-map', Key=filename, ContentType='image/png', ACL='public-read')
        self.invoice_doc_url = f'https://hire-on-map.fra1.digitaloceanspaces.com/{filename}' 
        self.invoice_doc_name = invoice_name
        db.session.commit()

    def update_insurance(self,insurance,insurance_name):
        # self.insurance_doc = insurance
        filename = f'vehicles/{self.id}/{str(uuid.uuid4().hex)}.png'
        self.client.put_object(Body=base64.b64decode(base64.b64encode(insurance)), Bucket='hire-on-map', Key=filename, ContentType='image/png', ACL='public-read')
        self.insurance_doc_url = f'https://hire-on-map.fra1.digitaloceanspaces.com/{filename}'    
        self.insurance_doc_name = insurance_name
        db.session.commit()
    
    @classmethod
    def find_by_id(cls,id):
        return cls.query.filter_by(id=id).first()


    @classmethod
    def find_by_plate(cls,plate_no):
        return cls.query.filter_by(plate_no=plate_no).first()


    @classmethod
    def find_vehicle_by_owner(cls,owner_id):
        return cls.query.filter_by(owner_id=owner_id).order_by(VehicleModel.added_on.desc()).all()


    @classmethod
    def find_vehicle_by_filter(cls,model_id,availibility,start_date,end_date,price_start,price_end):
        if availibility == 1:
            avail = True
            return cls.query.filter_by(vehicle_model_id=model_id,availibility=avail).all()

        return cls.query.filter_by(vehicle_model_id=model_id).all()

    @classmethod
    def search(cls, query):
        return cls.query.filter((cls.name.ilike(f'%{query}%'))|cls.specialization.ilike(f'%{query}%')|cls.plate_no.ilike(f'%{query}%')|cls.aadhar.ilike(f'%{query}%'))
    
    @classmethod
    def find_by_model(cls,vehicle_model_id):
        return cls.query.filter_by(vehicle_model_id=vehicle_model_id).all()
        
    

        

    


