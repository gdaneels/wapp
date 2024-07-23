from src import wapp_functions
from src import wapp_event_functions
from datetime import datetime
import pandas as pd

class Parser:
    def __init__(self, parsed_data=None):
        print("Initializing Parser.")
        if parsed_data is None:
            raise Exception("Parser should be given a data argument to stored parsed data.")
        self.parsed_data = parsed_data

    def _parse_valid_timestamp(self, metric_parse_config, line):
        """
        Parses the line for the timestamp and check if it falls within the given range of the configuration.

        :param metric_parse_config: the configuration for the metric
        :param line: the line to be parsed
        :return: the parsed timestamp and a boolean indicating if the timestamp is within the range
        """ 

        timestamp_start = None
        timestamp_stop = None
        timestamp_within_range = True

        if "parse_timestamp" not in metric_parse_config:
            return pd.NaT, False

        # no need to check for "function" presence as this is checked by Configuration class
        parse_timestamp = metric_parse_config["parse_timestamp"]["function"]
        timestamp = getattr(wapp_functions, parse_timestamp)(line)
        if timestamp is None:
            return pd.NaT, False
        
        # check if the timestamp is within range
        if "start" in metric_parse_config["parse_timestamp"]:
            timestamp_start = getattr(wapp_functions, parse_timestamp)(metric_parse_config["parse_timestamp"]["start"])
            if timestamp.time() < timestamp_start.time():
                timestamp_within_range = False
        if "stop" in metric_parse_config["parse_timestamp"]:
            timestamp_stop = getattr(wapp_functions, parse_timestamp)(metric_parse_config["parse_timestamp"]["stop"])
            if timestamp.time() > timestamp_stop.time():
                timestamp_within_range = False

        return timestamp, timestamp_within_range

    def _parse_line(self, data_file, data_file_parse_config, line):
        # a parse configuration per data file can have multiple parse configurations per metric
        for metric_parse_config in data_file_parse_config:
            timestamp, timestamp_within_range = self._parse_valid_timestamp(metric_parse_config, line)
            if timestamp is not pd.NaT and not timestamp_within_range:
                return

            # parse metric
            parse_function = metric_parse_config["parse_function"]
            parse_function_arg = None
            metric = metric_parse_config["metric"]
            if "parse_function_arg" in metric_parse_config:
                parse_function_arg = metric_parse_config["parse_function_arg"]
                metric_val = getattr(wapp_functions, parse_function)(line, parse_function_arg)
            else:
                metric_val = getattr(wapp_functions, parse_function)(line)
            if metric_val is not None:
                self.parsed_data.append({"timestamp": timestamp, "file": data_file, "metric": metric, "value": metric_val, "event": None})

            # parse event
            if "parse_events" in metric_parse_config:
                for event_name, parse_event_function in metric_parse_config["parse_events"].items():
                    if getattr(wapp_event_functions, parse_event_function)(line):
                        self.parsed_data.append({"timestamp": timestamp, "file": data_file, "event": event_name, "value": None, "metric": metric})

    def _parse_data_file(self, data_file, data_file_metric_configurations):
        # print(json.dumps(data_file_parse_config, indent=4))
        with open(data_file, errors='ignore') as f:
            for line in f:
                self._parse_line(data_file, data_file_metric_configurations, line)
            print(f"Parsed file {data_file}.")

    def parse(self, configuration_data):
        data_files = configuration_data.keys()
        for data_file in data_files:
            self._parse_data_file(data_file, configuration_data[data_file])
