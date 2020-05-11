from files import MachinaData
import falcon
from falcon_multipart.middleware import MultipartMiddleware
from falcon_cors import CORS

cors = CORS(allow_all_origins=True,
            allow_all_headers=True,
            allow_all_methods=True)

api = application = falcon.API(middleware=[MultipartMiddleware(), cors.middleware])
api.add_route('/api/prog', MachinaData())