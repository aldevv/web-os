import os, sys
import shutil
import falcon
import json
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../src")
from chmaquina import Chmaquina


class MachinaData(object):

    _storage_path = './uploaded_files'

    def __init__(self):
        self.ch = Chmaquina()
        self.ch.compileFile('programs/factorial.ch')
        self.ch.run_all()

    def on_get(self, req, resp):
        """Handles GET requests"""
        data = {
            'acumulador': self.ch.getAcumulador(),
            'variables': self.ch.getVariables(),
            'tags': self.ch.getTags(),
            'memory': self.ch.getMemory(),
            'stdout': self.ch.getStdin(),
        }
        resp.media = data

    def on_post(self, req, resp):
        """
        #! this is the saving code
        POST METHOD
        """
        # Retrieve input_file
        input_file = req.get_param('file')

        # Test if the file was uploaded
        if input_file.filename:
            # Retrieve filename
            filename = input_file.filename

            # Define file_path
            file_path = os.path.join(self._storage_path, filename)

            # Write to a temporary file to prevent incomplete files
            # from being used.
            temp_file_path = file_path + '~'

            open(temp_file_path, 'wb').write(input_file.file.read())

            # Now that we know the file has been fully saved to disk
            # move it into place.
            os.rename(temp_file_path, file_path)

        resp.status = falcon.HTTP_201
