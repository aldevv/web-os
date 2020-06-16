import os, sys
import falcon


class MachinaCompiler(object):


    def __init__(self, ch):
        self._storage_path = './uploaded_files'
        self.files_uploaded_paths = []
        self.ch = ch

    def on_get(self, req, resp):
        data = {
            'acumulador': self.ch.getAcumulador(),
            'variables': self.ch.getVariables(),
            'tags': self.ch.getTags(),
            'programs': self.ch.getPrograms(),
            'registers': self.ch.getRegisters(),
            'memory': self.ch.getMemory(),
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


        num_programs_uploaded = len(req.params)
        for i in range(num_programs_uploaded):
            input_file = req.get_param('file['+str(i)+']')
            # print("files", input_files)
            # print("some", type(input_files))
            # print("dir", dir(input_files))

            print("cargué el archivo: ", input_file.filename)
            if input_file.filename:
                filename = input_file.filename

            # Define file_path to save
            file_path = os.path.join(self._storage_path, filename)
            fileHandler = self.ch.fileInfo
            fileHandler.saveFilename(filename)
            fileHandler.saveFilePath(file_path)

            # Write to a temporary file to prevent incomplete files
            # from being used.
            temp_file_path = file_path + '~'

            open(temp_file_path, 'wb').write(input_file.file.read())

            # Now that we know the file has been fully saved to disk
            # move it into place.
            os.rename(temp_file_path, file_path)
            self.files_uploaded_paths.append(file_path)

        for i in range(num_programs_uploaded):
            self.ch.compileFile(self.files_uploaded_paths.pop(0))

        resp.status = falcon.HTTP_201
