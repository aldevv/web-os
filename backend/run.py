from files import MachinaData
import falcon
from falcon_multipart.middleware import MultipartMiddleware


api = application = falcon.API(middleware=[MultipartMiddleware()])
api.add_route('/api/prog', MachinaData())