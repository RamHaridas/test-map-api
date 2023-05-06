from db import db
from datetime import date, datetime
from pytz import timezone

class HistoryModel(db.Model):
    __tablename__ = 'history'

    id = db.Column(db.Integer,primary_key=True)
    log = db.Column(db.String(100))
    created_on = db.Column(db.DateTime,default=datetime.utcnow)
    # state_id = db.Column(db.Integer)


    def __init__(self,log):
        self.log = log
        # self.state = state

    def json(self):
        local = self.created_on.astimezone(timezone('Asia/Kolkata'))
        created = local.strftime('%d/%m/%Y, %H:%M:%S')
        return {'id':self.id,'log':self.log, 'created_on': created}

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    # @classmethod
    # def get_city_by_state(cls,state_id):
    #     return cls.query.filter_by(state_id=state_id).all()