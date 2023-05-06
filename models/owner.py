from io import BytesIO
from os import stat
from flask.helpers import send_file
from db import db
from datetime import date, datetime
from pytz import timezone
import urllib
import base64
import boto3
import uuid
from sqlalchemy import or_

class OwnerModel(db.Model):
    __tablename__ = 'owners'

    session = boto3.session.Session()
    client = session.client('s3', region_name='fra1', endpoint_url='https://fra1.digitaloceanspaces.com', aws_access_key_id='42JV7NAFNKRDF55WPPMW', aws_secret_access_key='aUzFHhgW8MEUQ0RWawV7a/M40VlSfCOqC50ThRhUC48')

    id = db.Column(db.Integer,primary_key=True)
    email = db.Column(db.String(80),unique=True)
    password = db.Column(db.String(80))
    name = db.Column(db.String(80))
    mobile = db.Column(db.String(15),unique=True)
    added_on = db.Column(db.DateTime,default=datetime.utcnow)
    modified_on = db.Column(db.DateTime)
    ip_address = db.Column(db.String(80))
    status = db.Column(db.Boolean,default=True)
    sub_id = db.Column(db.Integer,db.ForeignKey('subscriptions.id'))
    sub = db.relationship("SubscriptionModel",backref=db.backref("subscriptions",uselist=False))
    full_address = db.Column(db.String(length=None))
    pin_code = db.Column(db.String(80))
    #kyc details
    pan = db.Column(db.String(100))
    tan = db.Column(db.String(100))
    gst = db.Column(db.String(100))
    gumasta = db.Column(db.String(100))

    # pan_file = db.Column(db.LargeBinary) #image
    pan_filename = db.Column(db.String(length=None))
    pan_file_url = db.Column(db.String(length=None))
    # address_proof = db.Column(db.LargeBinary) #image
    address_proof_filename = db.Column(db.String(length=None))
    address_proof_url = db.Column(db.String(length=None))
    mobile2 = db.Column(db.String(100))
    city = db.Column(db.String(80))
    state = db.Column(db.String(80))
    refcode = db.Column(db.String(length=100))
    tehsil = db.Column(db.String(length=100))


    def __init__(self,email,password,name,mobile,ip_address,sub_id,full_address,pin_code,pan,tan,gst,gumasta,mobile2,state,city,refcode,tehsil):
        self.email = email
        self.password = password
        self.name = name
        self.mobile = mobile
        self.modified_on = datetime.utcnow()
        self.ip_address = ip_address
        self.sub_id = sub_id
        self.full_address = full_address
        if pin_code:
            self.pin_code = pin_code
        self.pan = pan
        if self.tan:
            self.tan = tan
        if gst:
            self.gst = gst
        if gumasta:
            self.gumasta = gumasta
        if mobile2:
            self.mobile2 = mobile2
        self.city = city
        self.state = state
        if refcode:
            self.refcode = refcode
        if tehsil:
            self.tehsil = tehsil


    def json(self):
        #modified = self.modified_on.strftime('%d/%m/%Y, %H:%M:%S')
        #added = self.added_on.strftime('%d/%m/%Y, %H:%M:%S')
        #curr = datetime.now(tz=timezone('Asia/Kolkata')).strftime('%d/%m/%Y, %H:%M:%S')
        local = self.added_on.astimezone(timezone('Asia/Kolkata'))
        local2 = self.modified_on.astimezone(timezone('Asia/Kolkata'))
        modified = local2.strftime('%d/%m/%Y, %H:%M:%S') 
        added = local.strftime('%d/%m/%Y, %H:%M:%S')
        subname = ""
        isKYC = True
        num = 0

        if self.sub:
            subname = self.sub.name
            num = self.sub.vehicles_alloted
        
        if self.address_proof_url is None or self.pan_file_url is None:
            isKYC = False
        
        return {
            'id':self.id,
            'email':self.email,
            'name':self.name,
            'mobile':self.mobile,
            'added_on':added,
            'modified_on':modified,
            'sub_id':self.sub_id,
            'status':self.status,
            'ip_address':self.ip_address,
            'subscription_name':subname,
            'alloted_vehicles':num,
            'pin_code':self.pin_code,
            'full_address':self.full_address,
            'pan':self.pan,
            'gst':self.gst,
            'gumasta':self.gumasta,
            'mobile2':self.mobile2,
            'state':self.state,
            'city':self.city,
            'referral_code':self.refcode,
            'tehsil':self.tehsil,
            'isKYC':isKYC
        }
    
    def small_json(self):
        #modified = self.modified_on.strftime('%d/%m/%Y, %H:%M:%S')
        #added = self.added_on.strftime('%d/%m/%Y, %H:%M:%S')
        #curr = datetime.now(tz=timezone('Asia/Kolkata')).strftime('%d/%m/%Y, %H:%M:%S')
        local = self.added_on.astimezone(timezone('Asia/Kolkata'))
        local2 = self.modified_on.astimezone(timezone('Asia/Kolkata'))
        modified = local2.strftime('%d/%m/%Y, %H:%M:%S') 
        added = local.strftime('%d/%m/%Y, %H:%M:%S')
        return {
            'id':self.id,
            'email':self.email,
            'name':self.name,
            'mobile':self.mobile,
            'added_on':added,
            'modified_on':modified,
            'status':self.status,
            'ip_address':self.ip_address,
            'subscription_name':self.sub.name,
            'alloted_vehicles':self.sub.vehicles_alloted,
            'pin_code':self.pin_code,
            'full_address':self.full_address,
            'pan':self.pan,
            'gst':self.gst,
            'gumasta':self.gumasta,
            'mobile2':self.mobile2,
            'state':self.state,
            'city':self.city
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def update_for_user(self,id,name,ip_address,pin_code,full_address,pan,tan,gst,gumasta,mobile,mobile2,state,city,tehsil,status,password,email,history):
        check = ['',None]
        if name not in check:
            self.name = name
        if pin_code not in check:
            self.pin_code = pin_code
        if full_address not in check:
            self.full_address = full_address
        if pan not in check:
            self.pan = pan
        if tan not in check:
            self.tan = tan
        if gst not in check:
            self.gst = gst
        if gumasta not in check:
            self.gumasta = gumasta
        if mobile2 not in check:
            self.mobile2 = mobile2
        if mobile not in check:
            self.mobile = mobile
        if state not in check:
            self.state = state
        if city not in check:
            self.city = city
        if tehsil not in check:
            self.tehsil = tehsil
        if status == 1:
            self.status = True
        if status == 0:
            self.status = False
        if password not in check:
            self.password = password
        if email not in check:
            self.email = email

        self.ip_address = ip_address
        self.modified_on = datetime.now().astimezone(tz=timezone('Asia/Kolkata'))
        db.session.commit()

    def update_pan(self,pan,pan_filename):
        # self.pan_file = pan
        filename = f'owners/{self.id}/{str(uuid.uuid4().hex)}.png'
        self.client.put_object(Body=base64.b64decode(base64.b64encode(pan)), Bucket='hire-on-map', Key=filename, ContentType='image/png', ACL='public-read')
        self.pan_file_url = f'https://hire-on-map.fra1.digitaloceanspaces.com/{filename}'
        self.pan_filename = pan_filename
        db.session.commit()

    def update_password(self, password):
        self.password = password
        db.session.commit()

    def update_address_proof(self,address_proof,address_proof_filename):
        # self.address_proof = address_proof
        filename = f'owners/{self.id}/{str(uuid.uuid4().hex)}.png'
        self.client.put_object(Body=base64.b64decode(base64.b64encode(address_proof)), Bucket='hire-on-map', Key=filename, ContentType='image/png', ACL='public-read')
        self.address_proof_url = f'https://hire-on-map.fra1.digitaloceanspaces.com/{filename}'
        self.address_proof_filename = address_proof_filename
        db.session.commit()

    def get_pan(self):
        name = "image.jpg"
        if self.pan_filename:
            name = self.pan_filename
        contents = urllib.request.urlopen(self.pan_file_url).read()
        data = base64.b64decode(base64.b64encode(contents))
        return send_file(BytesIO(data),as_attachment=False,attachment_filename=name)    

    def get_address_proof(self):
        name = "image.jpg"
        if self.address_proof_filename:
            name = self.address_proof_filename
        contents = urllib.request.urlopen(self.address_proof_url).read()
        data = base64.b64decode(base64.b64encode(contents))
        return send_file(BytesIO(data),as_attachment=False,attachment_filename=name) 

    def validity(self):
        self.added_on = datetime.utcnow()
        db.session.commit()

    @classmethod
    def login_owner(cls,email,password):
        return cls.query.filter_by(email=email,password=password).first()

    
    @classmethod
    def find_by_email(cls,email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def search(cls, query):
        return cls.query.filter((cls.name.ilike(f'%{query}%'))|cls.email.ilike(f'%{query}%')|cls.mobile.ilike(f'%{query}%'))

    @classmethod
    def find_by_id(cls,id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_by_name(cls,name):
        return cls.query.filter_by(name=name).all()

    @classmethod
    def find_by_number(cls,mobile):
        return cls.query.filter_by(mobile=mobile).first()


    def utc_to_local(self,utc_dt):
        return utc_dt.replace(tzinfo=timezone.utc).astimezone(tz=timezone('Asia/Kolkata'))