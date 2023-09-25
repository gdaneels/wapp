import json

class Configuration:
    def __init__(self, path_configuration_file=""):
        print("Initializing Configuration.")
        self.configuration = self._parse(path_configuration_file)
        print("Parsed configuration file.")

    def _parse(self, path_configuration_file=""):
        configuration = None
        with open(path_configuration_file) as json_file:
            configuration = json.load(json_file)
        return configuration

    def get(self):
        return self.configuration

    def metrics(self):
        return self.configuration["metrics"]

    def plots(self):
        return self.configuration["plots"]
