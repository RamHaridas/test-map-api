from flask_restful import Resource,reqparse
from models.subscription import SubscriptionModel
from datetime import date,datetime, timedelta
from models.owner import OwnerModel
from pytz import timezone

class SubscriptionResource(Resource):

    parser = reqparse.RequestParser()

    parser.add_argument(
        'name',
        type=str,
        required=True,
        help='name of subscription is mandatory'
    )
    parser.add_argument(
        'cost',
        type=str,
        required=True,
        help='cost of subscription is mandatory'
    )
    parser.add_argument(
        'days',
        type=int,
        required=True,
        help='days are mandatory'
    )
    parser.add_argument(
        'vehicles_alloted',
        type=int,
        required=True,
        help='vehicle count is mandatory'
    )
    parser.add_argument(
        'status',
        type=str,
        required=True,
        help='status is mandatory'
    )
    parser.add_argument(
        'ip_address',
        type=str,
        required=False
    )

    def post(self):
        data = SubscriptionResource.parser.parse_args()

        if data['status'] not in ['active','inactive']:
            return {'message':'status should be either active or inactive'}
        
        if SubscriptionModel.find_by_name(data['name']):
            return {'message':'subscritpion of same name alredy exist'}

        new_sub = SubscriptionModel(**data)
        new_sub.save_to_db()
        return new_sub.json()
        
    
    def get(self):
        local = reqparse.RequestParser()
        local.add_argument(
            'id',
            type=str,
            required=False
        )
        local.add_argument(
            'validity',
            type=int,
            required=False
        )
        data = local.parse_args()

        if data['validity'] is not None:
            owner = OwnerModel.find_by_id(data['validity'])
            if owner is None:
                return {'message':'owner not found'}
            start_date = owner.added_on
            sub = SubscriptionModel.find_by_id(owner.sub_id)
            days = sub.days
            end_date = start_date + timedelta(days=days)
            #local = end_date.astimezone(timezone('Asia/Kolkata'))
            #added = local.strftime('%d/%m/%Y, %H:%M:%S')
            isTrue = 0
            delta = end_date - datetime.utcnow()
            return {'message':end_date>datetime.utcnow(),'days_left': delta.days}

        sub = SubscriptionModel.find_by_id(data['id'])
        if sub:
            return sub.json()
    
        s_list = []

        for sub in SubscriptionModel.query.all():
            s_list.append(sub.json())

        return {'subs':s_list}


    def put(self):
        local = reqparse.RequestParser()
        local.add_argument(
            'id',
            type=int,
            required=True,
            help='id is mandatory'
        )
        local.add_argument(
            'name',
            type=str,
            required=False
        )
        local.add_argument(
            'cost',
            type=str,
            required=False
        )
        local.add_argument(
            'days',
            type=int,
            required=False,
            default=0
        )
        local.add_argument(
            'status',
            type=str,
            required=False
        )
        local.add_argument(
            'vehicles_alloted',
            type=int,
            required=False,
            default=0
        )
        local.add_argument(
            'ip_address',
            type=int,
            required=False
        )

        data = local.parse_args()
        
        sub = SubscriptionModel.find_by_id(data['id'])

        if sub:
            sub.update(**data)
            return sub.json()
        
        return {'message':'subscription does not exist'}


    def delete(self):
        local = reqparse.RequestParser()
        local.add_argument(
            'id',
            type=int,
            required=True,
            help='id is mandatory'
        )
        data = local.parse_args()

        sub = SubscriptionModel.find_by_id(**data)
        if sub:
            sub.delete_from_db()
            return{'message':'deleted succesfully'}

        return{'message':'subscription does not exist'} 