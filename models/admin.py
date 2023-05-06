from db import db
from datetime import datetime
from pytz import timezone

class AdminModel(db.Model):
    __tablename__ = 'admin_tbl'

    admin_id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(80),unique=True)
    password = db.Column(db.String(80))
    name = db.Column(db.String(80))
    email = db.Column(db.String(80))
    added_on = db.Column(db.DateTime,default=datetime.utcnow)
    modified_on = db.Column(db.DateTime)
    ip_address = db.Column(db.String(length=None))
    middle_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    admin_image = db.Column(db.String(length=None))


    def __init__(self,username,password,name,email,ip_address,middle_name,last_name,admin_image):
        self.username = username
        self.password = password
        self.name = name
        self.email = email
        self.modified_on = datetime.utcnow()  #modified date
        self.ip_address = ip_address
        self.middle_name = middle_name
        self.last_name = last_name
        self.admin_image = admin_image

    def json(self):
        #modified = self.modified_on.strftime('%d/%m/%Y, %H:%M:%S')
        #added = self.added_on.strftime('%d/%m/%Y, %H:%M:%S')
        local = self.added_on.astimezone(timezone('Asia/Kolkata'))
        local2 = self.modified_on.astimezone(timezone('Asia/Kolkata'))
        modified = local2.strftime('%d/%m/%Y, %H:%M:%S') 
        added = local.strftime('%d/%m/%Y, %H:%M:%S')
        return {
            'id':self.admin_id,
            'username':self.username,
            'name':self.name,
            'email':self.email,
            'modified_on':modified,
            'added_on':added,
            'ip_address':self.ip_address,
            'middle_name':self.middle_name,
            'last_name':self.last_name,
            'admin_image':self.admin_image
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def update(self,username,name,middle_name,last_name,admin_image,ip_address):
        check = ['',None]
        if name not in check:
            self.name = name
        if middle_name not in check:
            self.middle_name = middle_name
        if last_name not in check:
            self.last_name = last_name
        if admin_image not in check:
            self.admin_image = admin_image
        self.ip_address = ip_address
        self.modified_on = datetime.utcnow()
        db.session.commit()


    @classmethod
    def find_by_email(cls,email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def login_admin(cls,username,password):
        return cls.query.filter_by(username=username,password=password).first()

    @classmethod
    def find_by_username(cls,username):
        return cls.query.filter_by(username=username).first()