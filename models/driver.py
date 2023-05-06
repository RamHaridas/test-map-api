from db import db
from datetime import datetime
from pytz import timezone
from flask import send_file,request
from io import BytesIO
import urllib
import base64
import boto3
import uuid

class DriverModel(db.Model):
    __tablename__ = 'drivers'

    session = boto3.session.Session()
    client = session.client('s3', region_name='fra1', endpoint_url='https://fra1.digitaloceanspaces.com', aws_access_key_id='42JV7NAFNKRDF55WPPMW', aws_secret_access_key='aUzFHhgW8MEUQ0RWawV7a/M40VlSfCOqC50ThRhUC48')


    id = db.Column(db.Integer,primary_key=True)
    email = db.Column(db.String(80))
    password = db.Column(db.String(80))
    name = db.Column(db.String(80))
    mobile = db.Column(db.String(80))
    # image = db.Column(db.LargeBinary) #image
    image_filename = db.Column(db.String(length=None)) 
    image_url = db.Column(db.String(length=None)) 
    # license = db.Column(db.LargeBinary)  #image
    license_filename = db.Column(db.String(length=None))
    license_url = db.Column(db.String(length=None))
    adhaar = db.Column(db.String(80))
    mobile2 = db.Column(db.String(80))
    ip_address = db.Column(db.String(length=None))
    added_on = db.Column(db.DateTime,default=datetime.utcnow)
    vehicle_id = db.Column(db.Integer,db.ForeignKey('vehicle_tbl.id'))
    vehicle_rel = db.relationship("VehicleModel",backref=db.backref('vehicle_tbl',uselist=False))
    owner_id = db.Column(db.Integer,db.ForeignKey('owners.id'))
    owner_rel = db.relationship('OwnerModel',backref=db.backref('onwers',uselist=False))


    def __init__(self,email,password,name,mobile,adhaar,mobile2,ip_address,vehicle_id,owner_id):
        self.email = email
        self.password = password
        self.name = name
        self.mobile = mobile
        self.adhaar = adhaar
        self.mobile2 = mobile2
        self.ip_address = ip_address
        self.vehicle_id = vehicle_id
        self.owner_id = owner_id
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def update_vehicle(self,vehicle):
        self.vehicle = vehicle
        db.session.commit()

    def get_image(self):
        name = "image.jpg"
        if self.image_filename is not None:
            name = self.image_filename
        contents = urllib.request.urlopen(self.image_url).read()
        data = base64.b64decode(base64.b64encode(contents))
        return send_file(BytesIO(data),as_attachment=False,attachment_filename=name)    
        
    def get_license(self):
        name = "image.jpg"
        if self.license_filename:
            name = self.license_filename
        contents = urllib.request.urlopen(self.license_url).read()
        data = base64.b64decode(base64.b64encode(contents))
        return send_file(BytesIO(data),as_attachment=False,attachment_filename=name)
        
    def update_image(self,image,image_name):
        # self.image = image
        filename = f'drivers/{self.id}/{str(uuid.uuid4().hex)}.png'
        self.client.put_object(Body=base64.b64decode(base64.b64encode(image)), Bucket='hire-on-map', Key=filename, ContentType='image/png', ACL='public-read')
        self.image_url = f'https://hire-on-map.fra1.digitaloceanspaces.com/{filename}'
        self.image_filename = image_name
        db.session.commit()

    def update_license(self,license_image,license_name):
        # self.license = license_image
        filename = f'drivers/{self.id}/{str(uuid.uuid4().hex)}.png'
        self.client.put_object(Body=base64.b64decode(base64.b64encode(license_image)), Bucket='hire-on-map', Key=filename, ContentType='image/png', ACL='public-read')
        self.license_url = f'https://hire-on-map.fra1.digitaloceanspaces.com/{filename}'
        self.license_filename = license_name
        db.session.commit()

    def json(self):
        owner_name = ""
        plate_no = ""
        if self.owner_rel:
            owner_name = self.owner_rel.name
        if self.vehicle_rel:
            if self.vehicle_rel.plate_no:
                plate_no = self.vehicle_rel.plate_no
            else:
                plate_no = self.vehicle_rel.name
        
        return {
            'id':self.id,
            'email':self.email,
            'name':self.name,
            'mobile':self.mobile,
            'vehicle_id':self.vehicle_id,
            'vehicle_plate':plate_no,
            'adhaar':self.adhaar,
            'mobile2':self.mobile2,
            'owner_id':self.owner_id,
            'owner_name':owner_name,
            'image_url':request.base_url+'?driver_image='+str(self.id),
            'license_url':request.base_url+'?driver_license='+str(self.id)
        }

    def update(self,id,name,adhaar,mobile2,vehicle_id,password,history):
        #db.session.flush()
        check = ['',None]
        if name not in check:
            self.name = name
        if adhaar not in check:
            self.adhaar = adhaar
        if mobile2 not in check:
            self.mobile2 = mobile2
        if vehicle_id:
            self.vehicle_id = vehicle_id  
        if password not in check:
            self.password = password 
        db.session.commit()


    def update_password(self, password):
        self.password = password
        db.session.commit()

    @classmethod
    def find_by_email(cls,email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def login_driver(cls,email,password):
        return cls.query.filter_by(email=email,password=password).first()
    
    @classmethod
    def login_by_mobile(cls,mobile,password):
        return cls.query.filter_by(mobile=mobile,password=password).first()

    @classmethod
    def find_driver_by_owner(cls,owner_id):
        return cls.query.filter_by(owner_id=owner_id).all()

    @classmethod
    def search(cls, query):
        return cls.query.filter((cls.name.ilike(f'%{query}%'))|cls.email.ilike(f'%{query}%')|cls.mobile.ilike(f'%{query}%')|cls.adhaar.ilike(f'%{query}%'))

    @classmethod
    def find_driver_by_vehicle(cls,vehicle_id):
        return cls.query.filter_by(vehicle_id=vehicle_id).all()

    @classmethod
    def find_by_id(cls,id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_by_mobile(cls,mobile):
        return cls.query.filter_by(mobile=mobile).first()