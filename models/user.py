from flask import send_file,request
from db import db
from datetime import datetime
from pytz import timezone
from io import BytesIO

class UserModel(db.Model):
    __tablename__ = 'user'
    
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(80))
    email = db.Column(db.String(80))
    state = db.Column(db.String(255))
    district = db.Column(db.String(255))
    password = db.Column(db.String(80))
    mobile = db.Column(db.String(80),nullable=True)
    added_on = db.Column(db.DateTime,default=datetime.utcnow)
    google_id = db.Column(db.String(length=None))
    facebook_id = db.Column(db.String(length=None))
    image = db.Column(db.LargeBinary,nullable=True)
    image_name = db.Column(db.String(length=None))
    google_image = db.Column(db.String(length=None))
    refcode = db.Column(db.String(length=100))

    
    def __init__(self,name,email,password,mobile,image,google_id,facebook_id,google_image,image_name,refcode):
        self.name = name
        self.email = email
        if password:
            self.password = password
        self.mobile = mobile
        if image:
            self.image = image
            self.image_name = image_name
        if google_id:
            self.google_id = google_id
        if facebook_id:
            self.facebook_id
        if google_image:
            self.google_image = google_image
        if refcode:
            self.refcode = refcode
        
    def json(self):
        local = self.added_on.astimezone(timezone('Asia/Kolkata'))
        added = local.strftime('%d/%m/%Y, %H:%M:%S')
        return {
            'id':self.id,
            'name':self.name,
            'email':self.email,
            'mobile':self.mobile,
            'state': self.state,
            'district': self.district,
            'password':self.password,
            'google_id':self.google_id,
            'facebook_id':self.facebook_id,
            'google_image':self.google_image,
            'added_on': added,
            'image_url':request.base_url+'?image='+str(self.id),
            'ref_code':self.refcode 
        }

    def small_json(self):
        return {
            'id':self.id,
            'name':self.name,
            'email':self.email,
            'state': self.state,
            'district': self.district,
            'password':self.password,
            'mobile':self.mobile,
            'google_id':self.google_id,
            'added_on': self.added_on.isoformat(),
            'facebook_id':self.facebook_id
        }
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def update(self,id,name,mobile,state,district):
        if name:
            self.name = name
        if mobile:
            self.mobile = mobile
        if state:
            self.state = state
        if district:
            self.district = district
        db.session.commit()

    def update_password(self, password):
        self.password = password
        db.session.commit()

    def update_image(self,image,image_name):
        if image:
            self.image = image
            self.image_name = image_name
            db.session.commit()

    def image_response(self):
        tempfilename = "image.jpg"
        if self.image_name:
            tempfilename = self.image_name
        return send_file(BytesIO(self.image),as_attachment=False,attachment_filename=tempfilename)

    def update_password(self, password):
        self.password = password
        db.session.commit()

    # def update_password(self,id,password,new_password):
    #     if self.password == password:
    #         self.password = new_password
    #         db.session.commit()
    #         return {'message':'password changed'}
    #     else:
    #         return {'message':'password did not match'}

    @classmethod
    def find_by_email(cls,email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_by_mobile(cls,mobile):
        return cls.query.filter_by(mobile=mobile).first()

    @classmethod
    def login_user(cls,email,password):
        return cls.query.filter_by(email=email,password=password).first()

    @classmethod
    def login_with_mobile(cls,mobile,password):
        return cls.query.filter_by(mobile=mobile,password=password).first()

    @classmethod
    def find_by_id(cls,id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def login_with_google(cls,google_id):
        return cls.query.filter_by(google_id=google_id).first()