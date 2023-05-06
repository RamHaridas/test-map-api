from db import db
from datetime import datetime
import enum
from pytz import timezone


class Status(enum.Enum):
    active = 'active'
    inactive = 'inactive'

    def __str__(self):
        return super().__str__()


class SubscriptionModel(db.Model):
    __tablename__ = 'subscriptions'

    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(80))
    cost = db.Column(db.String(80))
    days = db.Column(db.Integer)
    vehicles_alloted = db.Column(db.Integer)
    added_on = db.Column(db.DateTime,default=datetime.utcnow)
    modified_on = db.Column(db.DateTime)
    ip_address = db.Column(db.String(length=None))
    status = db.Column(db.Enum(Status))

    
    def __init__(self,name,cost,days,vehicles_alloted,status,ip_address):
        self.name = name
        self.cost = cost
        self.days = days
        self.status = status
        self.modified_on = datetime.utcnow()
        self.vehicles_alloted = vehicles_alloted
        if ip_address:
            self.ip_address = ip_address

    def json(self):
        local = self.added_on.astimezone(timezone('Asia/Kolkata'))
        local2 = self.modified_on.astimezone(timezone('Asia/Kolkata'))
        modified = local2.strftime('%d/%m/%Y, %H:%M:%S') 
        added = local.strftime('%d/%m/%Y, %H:%M:%S')
        return {
            'id':self.id,
            'name':self.name,
            'cost':self.cost,
            'added_on':added,
            'modified_on':modified,
            'status':self.status.__str__(),
            'vehicles_alloted':self.vehicles_alloted,
            'ip_address':self.ip_address,
            'days':self.days
        }
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def update(self,id,name,cost,days,status,vehicles_alloted,ip_address):
        if name:
            self.name = name
        if cost:
            self.cost = cost
        if days != 0:
            self.days = days
        if status in ['active','inactive']:
            self.status = status
        if vehicles_alloted != 0:
            self.vehicles_alloted = vehicles_alloted
        if ip_address:
            self.ip_address = ip_address
        self.id = self.id
        self.modified_on = datetime.utcnow()
        db.session.commit()

    
    @classmethod
    def find_by_id(cls,id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_by_name(cls,name):
        return cls.query.filter_by(name=name).first()

    