from flask.helpers import make_response
from db import db
from flask import Response,send_file
from io import BytesIO
from sqlalchemy import BLOB


class ImageModel(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    filename = db.Column(db.String(length=None))
    img = db.Column(db.LargeBinary)
    name = db.Column(db.Text,nullable=False)
    mimetype = db.Column(db.Text,nullable=False)


    def __init__(self,img,name,mimetype,filename):
        self.img = img
        self.name = name
        self.mimetype = mimetype
        self.filename = filename

    def save(self):
        db.session.add(self)
        db.session.commit()
    

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def response(self): 
        return send_file(BytesIO(self.img),as_attachment=False,attachment_filename=self.name)


    def json(self):
        return{
            'id':self.id,
            'name':self.name,
            'mimetype':self.mimetype,
            'filename':self.filename
        }

    @classmethod
    def find(cls,id):
        return cls.query.filter_by(id=id).first()