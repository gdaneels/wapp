# wapp
Wrapper-Around-Python-Parsing: small Python library to quickly parse log files

# How to use?

Run:
```
python wapp.py [configuration.json]
```

with `configuration.json` describing the available data and graphs to plot.

# JSON configuration file

An example JSON:
```
{
    "metrics":{
        "data/CPU_C.log":[
            {
                "name":"cpu_c",
                "parse_function:"parse_cpu",
                "metric":"cpu_usage",
                "report":1,
                "plot":1
            }
            {
                "name":"memory_c",
                "parse_function:"parse_memory",
                "metric":"memory_usage",
                "report":1,
                "plot":1
            }
        ],
        "data/CPU_Java.log":[
            {
                "name":"cpu_java",
                "parse_function":"parse_cpu",
                "metric":"cpu_usage",
                "report":1,
                "plot":1
            }
        ],
    },
    "plots":{
        "cpu_comparison":{
            "data":[
                "cpu_c",
                "cpu_java",
            ],
            "title": "CPU usage (%) over measurement",
            "y_label":"CPU usage (%)",
            "x_label":"Measurement"
        }
    }
}
```

### Output
