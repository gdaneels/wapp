import json

class Parser:
    def __init__(self, data=None):
        print("Initializing Parser.")
        if data is None:
            raise Exception("Parser should be given a data argument to stored parsed data.")
        self.data = data

    def parse(self, configuration_data):
        data_files = configuration_data.keys()
        for data_file in data_files:
            self.parse_data_file()

    def parse_data_file(self, path, parse_configurations):
        print(f"Parsing file {path} with following configuration:")
        print(json.dumps(parse_configurations, indent=4))
        with open(path, errors='ignore') as f:
            for line in f:
                for config in parse_configurations:
                    # parse timestamp
                    timestamp = None
                    if "parse_timestamp" in config:
                        parse_timestamp = config["parse_timestamp"]
                        timestamp = getattr(parse_functions, parse_timestamp)(line)

                    # parse metric
                    parse_function = config["parse_function"]
                    metric = config["metric"]
                    metric_val = getattr(parse_functions, parse_function)(line)
                    if metric_val:
                        parsed_data.append({"timestamp": timestamp, "file": path, "metric": metric, "value": metric_val})
        print("Parsing done.")
