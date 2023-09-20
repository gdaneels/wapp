import re
import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
import os

sns.set_style("ticks")
sns.despine()

parsed_data = []

def parse_timestamp(line):
    timestamp_pattern = re.compile("\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}")
    match = timestamp_pattern.search(line)
    if match:
        return datetime.strptime(str(matcher.group(0)), '%Y-%m-%d %H:%M:%S')
    else:
        # print("Didn't find correct timestamp in line: {0}".format(line.strip()))
        return None

def parse_cpu(line):
    str_cpu_usage = line.strip().split()[6]

    if str_cpu_usage[-1] != "%":
        raise Exception("Could not find CPU usage.")

    cpu_usage = float(str_cpu_usage.split("%")[0])
    return cpu_usage

def parse_virtual_memory_usage(line):
    str_mem_usage = line.strip().split()[5]

    if str_mem_usage[-1] != "%":
        raise Exception("Could not find virtual memory usage.")

    mem_usage = float(str_mem_usage.split("%")[0])
    return mem_usage

def parse(data_file):
    with open(data_file, errors='ignore') as f:
        for line in f:
            # timestamp = parse_timestamp(line)
            # print(timestamp)
            cpu_usage = parse_cpu(line)
            parsed_data.append({"timestamp": None, "file": data_file, "metric": "cpu_usage", "value": cpu_usage})
            virtual_memory_usage = parse_virtual_memory_usage(line)
            parsed_data.append({"timestamp": None, "file": data_file, "metric": "virtual_memory_usage", "value": virtual_memory_usage})

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

if __name__ == "__main__":
    current_timestamp = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')

    import sys
    path = str(sys.argv[1])

    parse(data_file=path)

    # first convert it to a Pandas dataframe for easy manipulation and plotting
    df = pd.DataFrame.from_records(parsed_data)
    print(df.to_string())
    generate_report(df, current_timestamp)
