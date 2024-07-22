def parse_event_x(line):
    pattern_event_x = "--- EVENT X ---"
    return (pattern_event_x in line)

def parse_event_y(line):
    pattern_event_y = "--- EVENT Y ---"
    return (pattern_event_y in line)
