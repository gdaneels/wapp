# WAPP
Wrapper-Around-Python-Parsing: small Python library to quickly parse log files

# Usage

Run:
```
python wapp.py configuration.json
```

with `configuration.json` describing the available data and graphs to plot.

# Features

We take an in-depth look at the different features of WAPP by using snippets of the `examples/configs/example.json` configuration file and discussing its contents and results.

## Parse multiple metrics per data file

## Parse multiple data file

## Tailored parse function per metric

## Parse timestamp per line

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

