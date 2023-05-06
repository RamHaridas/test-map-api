from db import db
from datetime import datetime
import enum
from pytz import timezone


class ModelVehicle(db.Model):
    __tablename__ = 'vehicle_model_tbl'

    id = db.Column(db.Integer,primary_key=True)
    vehicle_type_id = db.Column(db.Integer,db.ForeignKey('vehicle_type_tbl.id'))
    vehicle_type = db.relationship("VehicleTypeModel",backref=db.backref("vehicle_type_tbl",uselist=False)) #relationship for direct access
    vehicle_model_name = db.Column(db.String(80))
    status = db.Column(db.Boolean)
    added_on = db.Column(db.DateTime,default=datetime.utcnow)
    modified_on = db.Column(db.DateTime)
    ip_address = db.Column(db.String(length=None))

    def __init__(self,vehicle_type_id,vehicle_model_name,status,ip_address):
        self.vehicle_type_id = vehicle_type_id
        self.vehicle_model_name = vehicle_model_name
        self.status = status
        self.ip_address = ip_address
        self.modified_on = datetime.utcnow()

    def json(self):
        local = self.added_on.astimezone(timezone('Asia/Kolkata'))
        local2 = self.modified_on.astimezone(timezone('Asia/Kolkata'))
        modified = local2.strftime('%d/%m/%Y, %H:%M:%S') 
        added = local.strftime('%d/%m/%Y, %H:%M:%S')
        vehicle_type_name = ""
        master_name = ""
        if self.vehicle_type:
            vehicle_type_name = self.vehicle_type.vehicle_type_name
            if self.vehicle_type.master_rel:
                master_name = self.vehicle_type.master_rel.name
        return {
            'id':self.id,
            'vehicle_type_id':self.vehicle_type_id,
            'vehicle_type_name':vehicle_type_name,
            'model_name':self.vehicle_model_name,
            'master_name':master_name,
            'status':self.status,
            'added_on':added,
            'modified_on':modified,
            'ip_address':self.ip_address,
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def update(self,id,vehicle_type_id,vehicle_model_name,status,ip_address):
        self.modified_on = datetime.utcnow()
        self.ip_address = ip_address
        if vehicle_model_name:
            self.vehicle_model_name = vehicle_model_name

        if status in [True,False]:
            self.status = status

        if vehicle_type_id:
            self.vehicle_type_id = vehicle_type_id
            
        db.session.commit()

    @classmethod
    def find_by_id(cls,id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_by_name(cls,vehicle_model_name):
        return cls.query.filter_by(vehicle_model_name=vehicle_model_name).first()

    @classmethod
    def find_by_type(cls,vehicle_type_id):
        return cls.query.filter_by(vehicle_type_id=vehicle_type_id).all()
    