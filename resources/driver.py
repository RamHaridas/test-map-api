from flask_restful import Resource,reqparse,request
from models.driver import DriverModel
from models.owner import OwnerModel
from models.vehicle import VehicleModel


class DriverResource(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument(
        'email',
        type=str,
        required=True,
        help='email is mandatory'
    )
    parser.add_argument(
        'password',
        type=str,
        required=True,
        help='password is mandatory'
    )
    parser.add_argument(
        'name',
        type=str,
        required=True,
        help='name is mandatory'
    )
    parser.add_argument(
        'mobile',
        type=str,
        required=True,
        help='mobile is mandatory'
    )
    parser.add_argument(
        'adhaar',
        type=str,
        required=True,
        help='adhaar number is mandatory'
    )
    parser.add_argument(
        'mobile2',
        type=str,
        required=False,
        help='alternate mobile number is mandatory'
    )
    parser.add_argument(
        'ip_address',
        type=str,
        required=True,
        help='IP is mandatory'
    )
    parser.add_argument(
        'vehicle_id',
        type=int,
        required=True,
        help='vehicle ID is mandatory'
    )
    parser.add_argument(
        'owner_id',
        type=int,
        required=True,
        help='owner ID is mandatory'
    )

    #register driver 
    def post(self):
        data = DriverResource.parser.parse_args()

        if DriverModel.find_by_email(data['email']):
            return {'message':'driver already registered'}
        elif DriverModel.find_by_mobile(data['mobile']):
            return {'message':'driver with same mobile number already registered'}
        elif VehicleModel.find_by_id(data['vehicle_id']) is None:
            return {'message':'selected vehicle is not available'}
        elif OwnerModel.find_by_id(data['owner_id']) is None:
            return {'message':'selected owner is not present'}

        driver = DriverModel(**data)
        driver.save_to_db()
        return driver.json()

    
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
            'adhaar',
            type=str,
            required=False
        )
        local.add_argument(
            'password',
            type=str,
            required=False
        )
        local.add_argument(
            'mobile2',
            type=str,
            required=False
        )
        local.add_argument(
            'vehicle_id',
            type=int,
            required=False
        )
        local.add_argument(
            'password',
            type=str,
            required=False
        )
        local.add_argument(
            'history',
            type=str,
            required=False
        )
        data = local.parse_args()
        driver = DriverModel.find_by_id(data['id'])
        if data['vehicle_id']:
            if VehicleModel.find_by_id(data['vehicle_id']) is None:
                return {'message':'selected vehicle does not exist'}
        if driver:
            driver.update(**data)
            if data['history']:
                history = HistoryModel(log=data['history'])
                # print(history)
                history.save_to_db()
            return driver.json()

        return {'message':'driver not found'}

    def patch(self):
        local = reqparse.RequestParser()
        local.add_argument(
            'id',
            type=int,
            required=False
        )
        local.add_argument(
            'mobile',
            type=str,
            required=False
        )
        local.add_argument(
            'password',
            type=str,
            required=False
        )
        local.add_argument(
            'type',
            type=str,
            required=False
        )
        data = local.parse_args()

        if data['type'] == 'password':
            driver = DriverModel.find_by_mobile(data['mobile'])
            if driver:
                driver.update_password(data['password'])
                return {'message': 'Password Updated!'}
            else:
                return {'message': 'Driver not found'}

        return {'message': 'Driver not found'}
            


    #delete driver account
    def delete(self):

        local = reqparse.RequestParser()
        local.add_argument(
            'id',
            type=int,
            required=True,
            help='id is mandatory'
        )
        data = local.parse_args()
        driver = DriverModel.find_by_id(data['id'])

        if driver:
            driver.delete_from_db()
            return {'message':'deleted successfully'}
        
        return {'message':'driver does not exist'}
    
    
    #login driver 
    def get(self):
        local = reqparse.RequestParser()
        local.add_argument(
            'username',
            type=str,
            required=False
        )
        local.add_argument(
            'password',
            type=str,
            required=False
        )
        local.add_argument(
            'id',
            type=int,
            required=False
        )
        local.add_argument(
            'driver_image',
            type=int,
            required=False
        )
        local.add_argument(
            'driver_license',
            type=int,
            required=False
        )
        local.add_argument(
            'list',
            type=str,
            required=False
        )
        local.add_argument(
            'owner_id',
            type=int,
            required=False
        )

        data = local.parse_args()

        if data['driver_image']:
            driver = DriverModel.find_by_id(data['driver_image'])
            if driver:
                if driver.image_url:
                    return driver.get_image()

        elif data['driver_license']:
            driver = DriverModel.find_by_id(data['driver_license'])
            if driver:
                if driver.license_url:
                    return driver.get_license()

        elif data['id']:
            driver = DriverModel.find_by_id(data['id'])
            if driver:
                return driver.json()

        elif data['list'] == 'list':
            return {'drivers':[driver.json() for driver in DriverModel.query.order_by(DriverModel.added_on.desc()).all()]}
        
        elif data['owner_id']:
            return {'drivers':[driver.json() for driver in DriverModel.find_driver_by_owner(data['owner_id'])]}
 
        email = DriverModel.login_driver(data['username'],data['password'])
        mobile = DriverModel.login_by_mobile(data['username'],data['password'])

        if email:
            return email.json()
        elif mobile:
            return mobile.json()
        
        return {'message':'driver not found'}
    


class DriverImage(Resource):


    def post(self):
        pic = request.files['image']
        if not pic:
            return {'message':'please add image'}
        local = reqparse.RequestParser()
        local.add_argument(
            'id',
            type=int,
            required=False
        )
        local.add_argument(
            'email',
            type=str,
            required=False
        )
        data = local.parse_args()
        driver = DriverModel.find_by_id(data['id'])
        email = DriverModel.find_by_email(data['email'])
        if driver:
            try:
                driver.update_image(image=pic.read(),image_name=pic.filename)
                return {'message':'Image Saved'}
            except:
                return {'message':'Please reduce image size'}
        elif email:
            try:
                email.update_image(image=pic.read(),image_name=pic.filename)
                return {'message':'Image Saved'}
            except Exception as e:
                return {'message':str(e)}
        
        return {'message':'Driver not found'}

    

    def put(self):
        pic = request.files['license']
        if not pic:
            return {'message':'please add image'}
        local = reqparse.RequestParser()
        local.add_argument(
            'id',
            type=int,
            required=False
        )
        local.add_argument(
            'email',
            type=str,
            required=False
        )
        data = local.parse_args()

        driver = DriverModel.find_by_id(data['id'])
        email = DriverModel.find_by_email(data['email'])
        if driver:
            try:
                driver.update_license(license_image=pic.read(),license_name=pic.filename)
                return {'message':'License Saved'}
            except:
                return {'message':'Please reduce image size'}
        elif email:
            try:
                email.update_license(license_image=pic.read(),license_name=pic.filename)
                return {'message':'License Saved'}
            except:
                return {'message':'Please reduce image size'}
            
        return {'message':'Driver not found'}   


    
