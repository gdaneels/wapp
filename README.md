# WAPP
Wrapper-Around-Python-Parsing: small Python library to quickly parse log files

# Usage

Run:
```
python wapp.py configuration.json
```

with `configuration.json` describing the available data, and reports and plots to generate.

# Features

We take an in-depth look at the different features of WAPP by using snippets of the `examples/configs/example.json` configuration file and discussing its contents and results.

## Parse a single metric per log file

You can specify a specific metric that you want to parse in a log file, by adding this snippet in your configuration file:
```
{
    "metrics":{
        "examples/data/cpu_ram_usage_device_1.log":[
            {
                "name":"cpu_device_1",
                "parse_function":"parse_cpu",
                "metric":"cpu_usage",
                "report":1,
                "plot":1
            }
        ]
    }
}
```

The metrics (in the log files) that you want to parse are put in the `metrics` part of the configuration file.

Subsequently, you specify the _path to the log file_ in which you want to parse the metric. The metric part contains (or can contain following fields):

* `name`: names this metric in a general way, coupled to this particular log file, so it can be reference in comparison with similar metrics in other log files. The name should be unique over the whole configuration file.
* `parse_function`: specifies the parsing function to be used in the `src/wapp_functions` source file.
* `metric`: names the data that is parsed in this log file. Should be unique for this particular log file.
* `report`: indicates a `summary` and `data` report should be generated out of the parsed data. Not obligatory.
* `plot`: indicates an individual plot for this metric should be generated. Not obligatory.

## Tailored parse function per metric

## Parse timestamp per line

## Parse multiple metrics per data file

## Parse multiple data file

## Filenames for individual plots and/or reports

## Multiple metrics on same graph

# Example

## Run example

To run the example, execute:

```
python wapp.py examples/configs/example.json
```

## Input files

The input files needed to run the example, are:
- the data files, to be found in `examples/data/`
- the JSON configuration file `example.json`, to be found in `examples/configs/`

## Output files

When WAPP is finished, it will make an `output` directory (if no such directory exists yet). In that directory, it will create a subdirectory with the name of the configuration JSON file. In our case, the `example` directory that contains:
- `plots` directory
- `reports` directory

## Graphs

