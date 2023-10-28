import json
import os

class Configuration:
    def __init__(self, path_configuration_file=""):
        print("Initializing Configuration.")

        if not os.path.exists(path_configuration_file):
            raise Exception(f"Input JSON configuration {path_configuration_file} does not exist.")

        self.configuration = self._parse(path_configuration_file)
        self._check_metric_configurations(self.configuration["metrics"])

        print("Parsed configuration file.")

    def _parse_paths_data(self, configuration):
        data_files = configuration.keys()
        for file in data_files:
            if not os.path.exists(file):
                raise Exception(f"Data file {file} does not exist.")

    def _check_timestamp(self, data_file, metric_configuration):
        # don't bother if not needed
        if "parse_timestamp" not in metric_configuration:
            return True

        if "function" not in metric_configuration["parse_timestamp"]:
            name = metric_configuration["name"]
            raise Exception(f"No function name in parse_timestamp configuration for metric {name} in {metric_configuration}.")

    def _check_metric_configurations(self, metric_configurations):
        for data_file, metric_configuration_per_data_file in metric_configurations.items():
            for metric_configuration in metric_configuration_per_data_file:
                self._check_timestamp(data_file, metric_configuration)

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

    def metrics(self):
        return self.configuration["metrics"]

    def plots(self):
        if "plots" in self.configuration:
            return self.configuration["plots"]
        return None
