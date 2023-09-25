import json
import os

class Configuration:
    def __init__(self, path_configuration_file=""):
        print("Initializing Configuration.")

        if not os.path.exists(path_configuration_file):
            raise Exception(f"Input JSON configuration {path_configuration_file} does not exist.")

        self.configuration = self._parse(path_configuration_file)

        print("Parsed configuration file.")

    def _parse_paths_data(self, configuration):
        data_files = configuration.keys()
        for file in data_files:
            if not os.path.exists(file):
                raise Exception(f"Data file {file} does not exist.")

    def _parse(self, path_configuration_file=""):
        configuration = None
        with open(path_configuration_file) as json_file:
            configuration = json.load(json_file)

        if "metrics" not in configuration:
            raise Exception("Missing metrics part in configuration.")

        # check if all data paths exists
        self._parse_paths_data(configuration["metrics"])

        return configuration

    def get(self):
        return self.configuration

    def data(self):
        return self.configuration["metrics"]

    def plots(self):
        if "plots" in self.configuration:
            return self.configuration["plots"]
        return None
