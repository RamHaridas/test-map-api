from resources.password import PasswordResource
from flask import Flask
from flask_restful import Api
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
import psycopg2
import os
from resources.appointment import AppointmentResource
from resources.enquiries import EnquiryResource
from resources.vehicle import VehicleLocation, VehicleResource, VehicleMobileResource,VehicleDocumentResource,VehicleSearchResource
from resources.driver import DriverResource,DriverImage
from resources.user import UserResource,UserSearchResource
from resources.owner import OwnerResource, OwnerDocs
from resources.subscription import SubscriptionResource
from resources.admin import AdminResource
from resources.vehicle_type import VehicleTypeResource
from resources.vehicles_model import VehicleModelResource
from resources.master_vehicle import MasterVehicleResource
from resources.dashboard import DashboardResource
from resources.zones import CountryResource,CityResource,StateResource,ImageResource,ImageModel

normal = os.environ.get('MY_DATABASE_URL','sqlite:///data.db')
postgres_url = 'postgres://hireonmap:#123Mdassoc@localhost:5432/hireonmap'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = normal
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
api = Api(app)

# print(f"Running on {postgres_url}")

#add api references below here
api.add_resource(DashboardResource, '/dashboard')
api.add_resource(VehicleResource,'/vehicle')
api.add_resource(VehicleMobileResource,'/vimages')
api.add_resource(VehicleDocumentResource,'/vdocs')
api.add_resource(VehicleLocation,'/vgps')
api.add_resource(DriverResource,'/driver')
api.add_resource(DriverImage,'/dimages')
api.add_resource(UserResource,'/user')
api.add_resource(OwnerResource,'/regowner')
api.add_resource(SubscriptionResource,'/subs')
api.add_resource(CityResource,'/cities')
api.add_resource(StateResource,'/states')
api.add_resource(CountryResource,'/country')
api.add_resource(AdminResource,'/admin')
api.add_resource(VehicleTypeResource,'/vtype')
api.add_resource(VehicleModelResource,'/vmodel')
api.add_resource(MasterVehicleResource,'/vmaster')
api.add_resource(ImageResource,'/images')
api.add_resource(EnquiryResource,'/enquiry')
api.add_resource(AppointmentResource,'/appt')
api.add_resource(UserSearchResource,'/search')
api.add_resource(PasswordResource,'/password')
api.add_resource(OwnerDocs,'/ownerkyc')
api.add_resource(VehicleSearchResource,'/vsearch')


# keep this commented out for online
# @app.before_first_request
# def create_tables():
#     db.create_all()


if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)