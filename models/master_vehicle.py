from jinja2.environment import Template
from db import db
from datetime import datetime
from pytz import timezone



class MasterVehicleModel(db.Model):
    __tablename__ = 'master_vehicle_tbl'

    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(80))
    status = db.Column(db.Boolean,default=True)
    added_on = db.Column(db.DateTime,default=datetime.utcnow)
    modified_on = db.Column(db.DateTime)
    ip_address = db.Column(db.String(length=None))
    image_url = db.Column(db.String(length=None),nullable=True)

    def __init__(self,name,ip_address,image_url):
        self.name = name
        self.ip_address = ip_address
        self.modified_on = datetime.utcnow()
        if image_url:
            self.image_url = image_url

    def json(self):
        local = self.added_on.astimezone(timezone('Asia/Kolkata'))
        local2 = self.modified_on.astimezone(timezone('Asia/Kolkata'))
        modified = local2.strftime('%d/%m/%Y, %H:%M:%S') 
        added = local.strftime('%d/%m/%Y, %H:%M:%S')
        
        return{
            'id':self.id,
            'name':self.name,
            'status':self.status,
            'added_on':added,
            'modifed_on':modified,
            'ip_address':self.ip_address,
            'image':self.image_url
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self,id,name,status,ip_address,image_url):
        if name:
            self.name = name
        if status:
            self.status = status
        if image_url:
            self.image_url = image_url
        self.ip_address = ip_address
        db.session.commit()

    @classmethod
    def find_by_name(cls,name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_by_id(cls,id):
        return cls.query.filter_by(id=id).first()

    