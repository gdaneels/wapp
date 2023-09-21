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

def parse(path, parse_configurations):
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

def generate_report(output_dir_path, report_name, df, data_file, metric):
    output_dir_report = output_dir_path
    output_dir_report += "/reports/"
    if not os.path.exists(output_dir_report):
        try:
            os.mkdir(output_dir_report)
        except OSError as error:
            raise Exception(error)
    output_dir_summary = output_dir_report + f"{report_name}-summary.csv"
    output_dir_data = output_dir_report + f"{report_name}-data.csv"

    # save all data
    df_metric = df.loc[(df["file"] == data_file) & (df["metric"] == metric)]
    df_metric.to_csv(output_dir_data)

    # save the summary
    description = df_metric["value"].describe()
    description.to_csv(output_dir_summary)

def generate_reports(full_configuration, output_dir_path, df):
    for data_file, parse_configuration in full_configuration.items():
        for config in parse_configuration:
            print(config)
            if "report" in config and config["report"] is not None:
                metric = config["metric"]
                print(f"Generating report for metric \"{metric}\" in data file \"{data_file}\".")
                # parse the data frame for the metric and data file you want to be reported
                generate_report(output_dir_path, report_name=config["report"], df=df, data_file=data_file, metric=metric)

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
    full_configuration = parse_json(path=path_json)
    print("Parsed JSON configuration.")
    data_files = parse_data_files(full_configuration)
    print("Parsed and checked data files.")
    for data_file in data_files:
        parse(path=data_file, parse_configurations=full_configuration[data_file])

    # first convert it to a Pandas dataframe for easy manipulation and plotting
    df = pd.DataFrame.from_records(parsed_data)
    generate_reports(full_configuration, output_dir_path, df)
    # print(df.to_string())
    # generate_report(df.drop('timestamp', axis=1, inplace=False), current_timestamp)
