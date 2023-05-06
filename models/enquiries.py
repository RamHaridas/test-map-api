from time import sleep
from db import db
from datetime import datetime
from pytz import timezone
from sqlalchemy import desc


class EnquiryModel(db.Model):
    __tablename__ = 'enquiry_tbl'

    id = db.Column(db.Integer,primary_key=True)
    uid = db.Column(db.Integer,db.ForeignKey('user.id'))
    user_rel = db.relationship('UserModel',backref=db.backref('user',uselist=False))
    owner_id = db.Column(db.Integer,db.ForeignKey('owners.id'))
    owners = db.relationship('OwnerModel',backref=db.backref('owners_new',uselist=False))
    v_id = db.Column(db.Integer,db.ForeignKey('vehicle_tbl.id'))
    v_rel = db.relationship('VehicleModel',backref=db.backref('vehicle_tbl_new',uselist=False))
    lat = db.Column(db.Float)
    lon = db.Column(db.Float)
    added_on = db.Column(db.DateTime,default=datetime.utcnow)


    def __init__(self,uid,owner_id,v_id,lat,lon):
        self.uid = uid
        self.owner_id = owner_id
        self.v_id = v_id
        if lat:
            self.lat = lat
        if lon:
            self.lon = lon
        self.added_on = datetime.utcnow()

    
    def json(self):
        local = self.added_on.astimezone(timezone('Asia/Kolkata'))
        added = local.strftime('%d/%m/%Y, %H:%M:%S')
        url = ""
        if self.lat not in [None,0.0]:
            url = "https://www.google.com/maps/search/?api=1&query="+str(self.lat)+","+str(self.lon)
        username = ""
        usermobile = ""
        useremail = ""
        ownername = ""
        owneremail = ""
        vname = ""
        vplate = ""
        if self.user_rel:
            username = self.user_rel.name
            usermobile = self.user_rel.mobile
            useremail = self.user_rel.email
        if self.owners:
            ownername = self.owners.name
            owneremail = self.owners.email
        if self.v_rel:
            vname = self.v_rel.name
            vplate = self.v_rel.plate_no
        return{
            'eid':self.id,
            'uid':self.uid,
            'user_name':username,
            'user_mobile':usermobile,
            'user_email':useremail,
            'owner_id':self.owner_id,
            'owner_name':ownername,
            'owner_email':owneremail,
            'vehicle_id':self.v_id,
            'vehicle_name':vname,
            'vehicle_plate':vplate,
            'date_of_enquiry':added,
            'location':url,
            'lat':self.lat,
            'lon':self.lon
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
    def find_by_owner(cls,owner_id):
        return cls.query.filter_by(owner_id=owner_id).order_by(desc(cls.added_on)).all()

    @classmethod
    def find_by_vehicle(cls, vehicle_id):
        return cls.query.filter_by(v_id=vehicle_id).order_by(desc(cls.added_on)).all()

    @classmethod 
    def get_all(cls):
        return cls.query.order_by(desc(cls.added_on)).all()

    # no need of this function, use the already existing function delete_from_db written above
    #def delete_for_id(id):
	#    x = cls.query.filter_by(id=id).delete()
    #    db.session.delete(x)
    #    db.session.commit()

    
