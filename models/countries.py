from db import db


class CountryModel(db.Model):
    __tablename__ = 'countries_tbl'

    id = db.Column(db.Integer,primary_key=True)
    shortname = db.Column(db.String(10))
    name = db.Column(db.String(80))


    def __init__(self,id,shortname,name):
        self.id = id
        self.shortname = shortname
        self.name = name

    def json(self):
        return {'id':self.id,'shortname':self.shortname,'name':self.name}

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    

