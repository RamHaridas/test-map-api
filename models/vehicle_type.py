from db import db
from datetime import datetime
import enum
from pytz import timezone


class VehicleTypeModel(db.Model):
    __tablename__ = 'vehicle_type_tbl'

    id = db.Column(db.Integer,primary_key=True)
    master_id = db.Column(db.Integer,db.ForeignKey('master_vehicle_tbl.id'))
    master_rel = db.relationship('MasterVehicleModel',backref=db.backref('master_vehicle_tbl',uselist=False))
    vehicle_type_name = db.Column(db.String(80))
    status = db.Column(db.Boolean)
    added_on = db.Column(db.DateTime,default=datetime.utcnow)
    modified_on = db.Column(db.DateTime)
    ip_address = db.Column(db.String(length=None))
    image_url = db.Column(db.String(length=None))
    

    def __init__(self,master_id,vehicle_type_name,status,ip_address,image_url):
        self.master_id = master_id
        self.vehicle_type_name = vehicle_type_name
        self.status = status
        self.modified_on = datetime.utcnow()
        self.ip_address = ip_address
        if image_url:
            self.image_url = image_url

    def json(self):
        #converting utcnow to indian time zone
        local = self.added_on.astimezone(timezone('Asia/Kolkata'))
        local2 = self.modified_on.astimezone(timezone('Asia/Kolkata'))
        modified = local2.strftime('%d/%m/%Y, %H:%M:%S') 
        added = local.strftime('%d/%m/%Y, %H:%M:%S')
        master_name = ""
        if self.master_rel:
            master_name = self.master_rel.name
        return {
            'id':self.id,
            'master_id':self.master_id,
            'vehicle_type_name':self.vehicle_type_name,
            'vehicle_master':master_name,
            'status':self.status,
            'modified_on':modified,
            'added_on':added,
            'image_url':self.image_url,
            'ip_address':self.ip_address,
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_id(cls,id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_by_name(cls,vehicle_type_name):
        return cls.query.filter_by(vehicle_type_name=vehicle_type_name).first()

    @classmethod
    def find_by_master(cls,master_id):
        return cls.query.filter_by(master_id=master_id).all()

    def update(self,id,vehicle_type_name,status,master_id,ip_address,image_url):
        if vehicle_type_name not in ['',None]:
            self.vehicle_type_name = vehicle_type_name
        
        if status in [True,False]:
            self.status = status

        if master_id:
            self.master_id = master_id
            
        if image_url:
            self.image_url = image_url
        
        self.ip_address = ip_address
        self.modified_on = datetime.utcnow()
        db.session.commit()

    




