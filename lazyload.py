import yaml


class FileLoader(object):
    def __init__(self, filename):
        self.filename = filename
        self._data = None

    @property
    def data(self):
        """
         Carga el archivo la primera vez sinó devuelve el precargado.
        :return: Regresa json del archivo cargado.
        """
        if self._data is None:
            self._build_data()
        return self._data

    def _build_data(self):
        """
         Carga archivos json o yaml recibido en el __init__
        :return: No retorna algun valor.
        """
        stream = open(self.filename)
        data_file = yaml.load(stream, yaml.SafeLoader)
        stream.close()
        self._data = data_file
