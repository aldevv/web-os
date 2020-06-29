from buttons              import MachinaCompiler, MachinaRunner, MachinaClean, MachinaStep
from lea                  import MachinaInput
from chmaquina_settings   import MachinaSettings
import falcon, os, sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../src")
from scheduler import Scheduler
from falcon_multipart.middleware import MultipartMiddleware
from falcon_cors import CORS


cors = CORS(allow_origins_list=['*'],
            allow_all_origins=True,
            allow_all_headers=True,
            allow_all_methods=True)

api = application = falcon.API(middleware=[MultipartMiddleware(), cors.middleware])

ch = Scheduler()
# api.add_route('/api/leaCreateForm', MachinaInputCreate(ch))
api.add_route('/api/lea'          , MachinaInput(ch))
api.add_route('/api/compile'      , MachinaCompiler(ch))
api.add_route('/api/run'          , MachinaRunner(ch))
api.add_route('/api/nav'          , MachinaSettings(ch))
api.add_route('/api/clean'        , MachinaClean(ch))
api.add_route('/api/step'         , MachinaStep(ch))