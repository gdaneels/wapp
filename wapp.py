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

PLOTS_SUBDIR = '/plots/'
REPORTS_SUBDIR = '/reports/'

# maps names to {metric, data_file}
configuration_names_mapping = dict()
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

def parse_name_mapping(metrics_configuration):
    for data_file, parse_configurations in metrics_configuration.items():
        for parse_config in parse_configurations:
            name = parse_config["name"] 
            if name in configuration_names_mapping:
                raise Exception(f"\"name\" {name} is not unique in JSON configuration.")
            configuration_names_mapping[name] = {"metric": parse_config["metric"], "data_file": data_file}
    # print(json.dumps(configuration_names_mapping, indent=4))
    return configuration_names_mapping

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
    output_dir_path = "output/" + os.path.basename(path_json).split(".")[0]
    if not os.path.exists(output_dir_path):
        os.makedirs(output_dir_path)
    else:
        raise Exception(f"Output directory {output_dir_path} exists already.")
    return output_dir_path

def generate_report(output_dir_path, report_name, df, data_file, metric):
    output_dir_report = output_dir_path + REPORTS_SUBDIR
    if not os.path.exists(output_dir_report):
        os.mkdir(output_dir_report)
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
            if "report" in config and (config["report"] == 1 or isinstance(config["report"], str)):
                report_name = config["name"]
                if isinstance(config["report"], str):
                    report_name = config["report"]
                metric = config["metric"]
                print(f"Generating report for metric \"{metric}\" in data file \"{data_file}\".")
                # parse the data frame for the metric and data file you want to be reported
                generate_report(output_dir_path, report_name=report_name, df=df, data_file=data_file, metric=metric)

def plot_data(df, metric, plot_path, y_lim_min=None, y_lim_max=None):
    plt.figure(figsize=(20, 5))

    sns.lineplot(df["value"], linewidth=1, marker=".", label=plot_path)
    
    plt.title("{0} over time".format(metric))
    plt.ylabel("{0}".format(metric))
    plt.xlabel('measurement')
    plt.legend(loc="upper left")
    plt.ylim(y_lim_min, y_lim_max)
    plt.tight_layout()

    plt.savefig(plot_path)
    # print(f"Plotted {metric} graph to {plot_path}.")

def generate_plot(output_dir_path, plot_name, df, data_file, metric):
    output_dir_plot = output_dir_path
    output_dir_plot += PLOTS_SUBDIR
    if not os.path.exists(output_dir_plot):
        try:
            os.mkdir(output_dir_plot)
        except OSError as error:
            raise Exception(error)
    output_plot_path = output_dir_plot + plot_name

    # select the data
    df_metric = df.loc[(df["file"] == data_file) & (df["metric"] == metric)]
    # make the plot
    plot_data(df_metric, metric, output_plot_path)

def generate_individual_plots(full_configuration, output_dir_path, df):
    for data_file, parse_configuration in full_configuration.items():
        for config in parse_configuration:
            if "plot" in config and (config["plot"] == 1 or isinstance(config["plot"], str)):
                plot_name = config["name"]
                if isinstance(config["plot"], str):
                    plot_name = config["plot"]

                metric = config["metric"]
                print(f"Generating plot for metric \"{metric}\" in data file \"{data_file}\".")
                # parse the data frame for the metric and data file you want to be reported
                generate_plot(output_dir_path, plot_name=plot_name, df=df, data_file=data_file, metric=metric)

def plot_combined(names_mapping, plot_name, plot_title, x_label, y_label, plot_lines, output_dir_path, df):
    output_dir_plot = output_dir_path
    output_dir_plot += PLOTS_SUBDIR
    if not os.path.exists(output_dir_plot):
        try:
            os.mkdir(output_dir_plot)
        except OSError as error:
            raise Exception(error)
    output_plot_path = output_dir_plot + plot_name

    plt.figure(figsize=(20, 5))

    for plot_line in plot_lines:
        df_metric = df.loc[(df["file"] == names_mapping[plot_line]["data_file"]) & (df["metric"] == names_mapping[plot_line]["metric"])]
        # reset the index
        # this ways the plots can be mapped over each other and are not sequential
        df_metric = df_metric.reset_index()
        sns.lineplot(df_metric["value"], linewidth=1, marker=".", label=plot_line)
    
    if plot_title:
        plt.title(plot_title)
    if x_label:
        plt.xlabel(x_label)
    if y_label:
        plt.ylabel(y_label)
    plt.legend(loc="upper left")
    # plt.ylim(y_lim_min, y_lim_max)
    plt.tight_layout()

    plt.savefig(output_plot_path)
    # print(f"Plotted {metric} graph to {plot_path}.")
     
def generate_combined_plots(plot_configuration, names_mapping, output_dir_path, df):
    for plot_name, plot_info in plot_configuration.items():
        # check if the plot lines are valid names of parse configs
        for plot_line in plot_info["data"]:
            if plot_line not in names_mapping:
                raise Exception(f"Can not find name {plot_line} of parse config.")

        plot_title = plot_info["title"] if "title" in plot_info else None
        x_label = plot_info["x_label"] if "x_label" in plot_info else None
        y_label = plot_info["y_label"] if "y_label" in plot_info else None
            
        plot_combined(names_mapping, plot_name, plot_title, x_label, y_label, plot_info["data"], output_dir_path, df)

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
    names_mapping = parse_name_mapping(full_configuration["metrics"])
    if "metrics" not in full_configuration:
        raise Exception("No \"metrics\" part in the JSON configuration.")
    metrics_configuration = full_configuration["metrics"]
    print("Parsed JSON configuration.")

    # parse data files
    data_files = parse_data_files(metrics_configuration)
    print("Parsed and checked data files.")
    for data_file in data_files:
        parse(path=data_file, parse_configurations=metrics_configuration[data_file])

    # first convert it to a Pandas dataframe for easy manipulation and plotting
    df = pd.DataFrame.from_records(parsed_data)
    generate_reports(metrics_configuration, output_dir_path, df)
    generate_individual_plots(metrics_configuration, output_dir_path, df)

    plots_configuration = None
    if "plots" in full_configuration:
        plot_configuration = full_configuration["plots"]
        generate_combined_plots(plot_configuration, names_mapping, output_dir_path, df)
