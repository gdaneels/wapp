
def parse_timestamp(line):
    timestamp_pattern = re.compile("\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}")
    match = timestamp_pattern.search(line)
    if match:
        return datetime.strptime(str(match.group(0)), '%Y-%m-%d %H:%M:%S')
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

def parse_mbps_milliseconds(line):
    pattern = re.compile("Throughput (\d+) bytes in the last (\d+) milliseconds.")
    is_match = pattern.search(line)
    if (is_match):
        bytes = float(is_match.group(1))
        ms = float(is_match.group(2))
        mbps = ((bytes * 8.0 / ms) * 1000.0) / 1000.0 / 1000.0
        # print(f"bytes = {bytes}, ms = {ms}, mbps = {mbps}")
        return mbps
    else:
        return None

def parse_mbps_microseconds(line):
    pattern = re.compile("Throughput (\d+) bytes in the last (\d+) microseconds.")
    is_match = pattern.search(line)
    if (is_match):
        bytes = float(is_match.group(1))
        ms = float(is_match.group(2))
        mbps = ((bytes * 8.0 / ms) * 1000000.0) / 1000.0 / 1000.0
        # print(f"bytes = {bytes}, ms = {ms}, mbps = {mbps}")
        return mbps
    else:
        return None
