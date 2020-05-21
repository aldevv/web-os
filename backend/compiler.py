import os, sys
import falcon


class MachinaCompiler(object):


    def __init__(self, ch):
        self._storage_path = './uploaded_files'
        self.ch = ch

    def on_get(self, req, resp):
        data = {
            'acumulador': self.ch.getAcumulador(),
            'variables': self.ch.getVariables(),
            'tags': self.ch.getTags(),
            'programs': self.ch.getPrograms(),
            'registers': self.ch.getRegisters(),
            'memoryAvailable': self.ch.getMemoryAvailable(),
            'memoryUsed': self.ch.getMemoryUsed(),
        }
        resp.media = data

    def on_post(self, req, resp):
        """
        POST file
        documentation
        https://github.com/yohanboniface/falcon-multipart
        """

        input_file = req.get_param('file')
        print("cargué el archivo: ", input_file.filename)
        if input_file.filename:
            filename = input_file.filename
            fileHandler = self.ch.fileInfo
            fileHandler.saveFilename(filename)

            # Define file_path to save
            file_path = os.path.join(self._storage_path, filename)

            # Write to a temporary file to prevent incomplete files
            # from being used.
            temp_file_path = file_path + '~'

            open(temp_file_path, 'wb').write(input_file.file.read())

            # Now that we know the file has been fully saved to disk
            # move it into place.
            os.rename(temp_file_path, file_path)


            self.ch.compileFile(file_path)

        resp.status = falcon.HTTP_201
