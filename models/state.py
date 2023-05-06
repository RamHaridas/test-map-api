from db import db


class StateModel(db.Model):
    __tablename__ = 'states_tbl'

    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(80))
    country_id = db.Column(db.Integer)

    def __init__(self,id,name,country_id):
        self.id = id
        self.name = name
        self.country_id = country_id


    def json(self):
        return {'id':self.id,'name':self.name,'country_id':self.country_id}

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    
    @classmethod
    def get_by_country(cls,country_id):
        return cls.query.filter_by(country_id=country_id).all()
    