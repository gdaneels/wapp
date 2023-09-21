import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
import os
from datetime import datetime
import json
import parse_functions

sns.set_style("ticks")
sns.despine()

parsed_data = []

def parse(path, parse_config):
    print(f"Parsing file {path} with following configuration:")
    print(json.dumps(parse_config, indent=4))
    with open(path, errors='ignore') as f:
        for line in f:
            for parse_info in parse_config:
                # parse timestamp
                timestamp = None
                if "parse_timestamp" in parse_info:
                    parse_timestamp = parse_info["parse_timestamp"]
                    timestamp = getattr(parse_functions, parse_timestamp)(line)

                # parse metric
                parse_function = parse_info["parse_function"]
                metric = parse_info["metric"]
                metric_val = getattr(parse_functions, parse_function)(line)
                if metric_val:
                    parsed_data.append({"timestamp": timestamp, "file": path, "metric": metric, "value": metric_val})
    print("Parsing done.")

def generate_report(df, suffix=None):
    dir_report = "./reports"
    if not os.path.exists(dir_report):
        try:
            os.mkdir(dir_report)
        except OSError as error:
            raise Exception(error)

    path_report = f"{dir_report}/report"
    if suffix:
        path_report += "-"
        path_report += suffix
    path_report += ".csv"
    
    # make description
    description = df.groupby("metric").describe()

    print(description)
    description.to_csv(path_report)

def parse_json(path=None):
    configuration = None
    with open(path) as json_file:
        configuration = json.load(json_file)
    return configuration

def parse_data_files(configuration):
    data_files = configuration.keys()
    for file in data_files:
        if not os.path.exists(file):
            raise Exception(f"Data file {file} does not exist.")
    return data_files

def make_output_dir(path_json):
    output_dir_path = "output/"
    output_dir_path += os.path.basename(path_json).split(".")[0]
    if not os.path.exists(output_dir_path):
        os.makedirs(output_dir_path)
    else:
        raise Exception(f"Could not create output directory {output_dir_path}.")
    return output_dir_path

def generate_reports(configuration):

if __name__ == "__main__":
    current_timestamp = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')

    import sys
    path_json = str(sys.argv[1])
    if not os.path.exists(path_json):
        raise Exception(f"Input JSON {path_json} does not exist.")

    # make output dir
    output_dir_path = make_output_dir(path_json)
    print(f"Created output directory at path {output_dir_path}.")
    # transform json configuration to Python dict
    configuration = parse_json(path=path_json)
    print("Parsed JSON configuration.")
    data_files = parse_data_files(configuration)
    print("Parsed and checked data files.")
    for data_file in data_files:
        parse(path=data_file, parse_config=configuration[data_file])
    # parse(data_file=path)

    # first convert it to a Pandas dataframe for easy manipulation and plotting
    df = pd.DataFrame.from_records(parsed_data)
    # print(df.to_string())
    # generate_report(df.drop('timestamp', axis=1, inplace=False), current_timestamp)
