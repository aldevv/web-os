from compiler import MachinaCompiler
from runner   import MachinaRunner
import falcon, os, sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../src")
from chmaquina import Chmaquina
from falcon_multipart.middleware import MultipartMiddleware
from falcon_cors import CORS

cors = CORS(allow_all_origins=True,
            allow_all_headers=True,
            allow_all_methods=True)

api = application = falcon.API(middleware=[MultipartMiddleware(), cors.middleware])

ch = Chmaquina()
api.add_route('/api/compile', MachinaCompiler(ch))
api.add_route('/api/run', MachinaRunner(ch))