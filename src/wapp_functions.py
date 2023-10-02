import re
from datetime import datetime

def parse_timestamp(line):
    timestamp_pattern = re.compile("\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}")
    match = timestamp_pattern.search(line)
    if match:
        return datetime.strptime(str(match.group(0)), '%Y-%m-%d %H:%M:%S')
    else:
        # print("Didn't find correct timestamp in line: {0}".format(line.strip()))
        raise Exception(f"Could not parse timestamp in line: {line}")

def parse_cpu(line):
    pattern = re.compile("CPU usage is (\d+.\d+) %")
    is_match = pattern.search(line)
    if (is_match):
        return float(is_match.group(1))
    else:
        return None

def parse_memory(line):
    pattern = re.compile("RAM memory usage is (\d+.\d+) %.")
    is_match = pattern.search(line)
    if (is_match):
        return float(is_match.group(1))
    else:
        return None

def parse_throughput(line):
    pattern = re.compile("RX throughput received is (\d+.\d+) Mbit/s.")
    is_match = pattern.search(line)
    if (is_match):
        return float(is_match.group(1))
    else:
        return None
