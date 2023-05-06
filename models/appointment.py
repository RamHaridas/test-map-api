from db import db
from datetime import datetime
from pytz import timezone


class AppointmentModel(db.Model):

    id = db.Column(db.Integer,primary_key=True)
    customer_name = db.Column(db.String(80))
    address = db.Column(db.String(length=None))
    customer_mobile = db.Column(db.String(80))
    alternate_mobile = db.Column(db.String(80))
    added_on = db.Column(db.DateTime,default=datetime.utcnow)
    start = db.Column(db.String(80))
    end = db.Column(db.String(80))
    time = db.Column(db.String(80))

    #relations
    owner_id = db.Column(db.Integer,db.ForeignKey('owners.id'))
    owner_rel = db.relationship("OwnerModel",backref=db.backref('owner_appt',uselist=False))
    vehicle_id = db.Column(db.Integer,db.ForeignKey('vehicle_tbl.id'))
    vehicle_rel = db.relationship("VehicleModel",backref=db.backref('vehicle_appt',uselist=False))


    def __init__(self,customer_name,address,customer_mobile,alternate_mobile,owner_id,vehicle_id,start,end,time):
        self.customer_name = customer_name
        self.address = address
        self.customer_mobile = customer_mobile
        self.alternate_mobile = alternate_mobile
        self.owner_id = owner_id
        self.vehicle_id = vehicle_id
        self.start = start
        self.end = end
        self.time = time


    def save_to_db(self):
        db.session.add(self)
        db.session.commit()


    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    
    def json(self):
        local = self.added_on.astimezone(timezone('Asia/Kolkata')) 
        added = local.strftime('%d/%m/%Y, %H:%M:%S')
        owner_name = ""
        if self.owner_rel:
            owner_name = self.owner_rel.name
            
        return {
            'id':self.id,
            'created_on':added,
            'customer_name':self.customer_name,
            'address':self.address,
            'customer_mobile':self.customer_mobile,
            'alternate_mobile':self.alternate_mobile,
            'owner_id':self.owner_id,
            'owner_name':owner_name,
            'vehicle_id':self.vehicle_id,
            'start_day':self.start,
            'end_day':self.end,
            'time':self.time
        }


    @classmethod
    def get_by_owner(cls,owner_id):
        return cls.query.filter_by(owner_id=owner_id).all()

    
    @classmethod
    def get_by_vehicle(cls,vehicle_id):
        return cls.query.filter_by(vehicle_id=vehicle_id).all()

    @classmethod
    def find_by_id(cls,id):
        return cls.query.filter_by(id=id).first()

    def update(self,id,customer_name,address,customer_mobile,alternate_mobile,owner_id,vehicle_id,start,end,time):
        check = ['',0,None]
        
        if customer_name not in check:
            self.customer_name = customer_name
        if address not in check:
            self.address = address
        if customer_mobile not in check:
            self.customer_mobile = customer_mobile
        if alternate_mobile not in check:
            self.alternate_mobile = alternate_mobile
        if owner_id not in check:
            self.owner_id = owner_id
        if vehicle_id not in check:
            self.vehicle_id = vehicle_id
        if start not in check:
            self.start = start
        if end not in check:
            self.end = end
        if time not in check:
            self.time = time
        db.session.commit()


    