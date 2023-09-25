import wapp_functions

class Parser:
    def __init__(self, parsed_data=None):
        print("Initializing Parser.")
        if parsed_data is None:
            raise Exception("Parser should be given a data argument to stored parsed data.")
        self.parsed_data = parsed_data

    def parse(self, configuration_data):
        data_files = configuration_data.keys()
        for data_file in data_files:
            self.parse_data_file(data_file, configuration_data[data_file])

    def parse_data_file(self, data_file, data_file_parse_config):
        print(f"Parsing file {data_file} with following configuration:")
        # print(json.dumps(data_file_parse_config, indent=4))
        with open(data_file, errors='ignore') as f:
            for line in f:
                # a parse configuration per data file can have multiple parse configurations per metric
                for metric_parse_config in data_file_parse_config:
                    # parse timestamp
                    timestamp = None
                    if "parse_timestamp" in metric_parse_config:
                        parse_timestamp = metric_parse_config["parse_timestamp"]
                        timestamp = getattr(wapp_functions, parse_timestamp)(line)
                    # parse metric
                    parse_function = metric_parse_config["parse_function"]
                    metric = metric_parse_config["metric"]
                    metric_val = getattr(wapp_functions, parse_function)(line)
                    if metric_val:
                         self.parsed_data.append({"timestamp": timestamp, "file": data_file, "metric": metric, "value": metric_val})
        print("Parsing done.")
