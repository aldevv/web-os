import os, sys
import falcon


class MachinaCompiler(object):


    def __init__(self, ch):
        self._storage_path = './uploaded_files'
        self.ch = ch
        self.files = set()

    def on_get(self, req, resp):
        data = {
            'acumulador': self.ch.getAcumulador(),
            'variables': self.ch.getVariablesHistory(),
            'tags': self.ch.getTagsHistory(),
            'programs': self.ch.getPrograms(),
            'registers': self.ch.getRegisters()
        }
        resp.media = data

    def on_post(self, req, resp):
        """
        POST file
        documentation
        https://github.com/yohanboniface/falcon-multipart
        """
        input_file = req.get_param('file')
        print("cargué: ", input_file.filename)
        if input_file.filename not in self.files:
            self.files.add(input_file.filename)
        else:
            print("segui derecho con ", input_file.filename)
            return

        # Test if the file was uploaded
        if input_file.filename:
            filename = input_file.filename
            self.ch.saveFilename(filename)

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
