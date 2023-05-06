from db import db

class CitiesModel(db.Model):
    __tablename__ = 'cities'

    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(100))
    state_id = db.Column(db.Integer)


    def __init__(self,name,state):
        self.name = name
        self.state = state

    def json(self):
        return {'id':self.id,'name':self.name,'state':self.state_id}

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_city_by_state(cls,state_id):
        return cls.query.filter_by(state_id=state_id).all()