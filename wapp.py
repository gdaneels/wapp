from parser import Parser 
from configuration import Configuration 
from report import Report 
from plotter import Plotter 
from datetime import datetime
import os
import sys

class Wapp:
    def __init__(self, path_configuration_file=""):
        print("Initializing WAPP.")
        self.execution_timestamp = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
        self.name_output_dir = "output"
        self.name_reports_dir = self.name_output_dir + "/" + "reports"
        self.name_plots_dir = self.name_output_dir + "/" + "plots"
        self.path_configuration_file = path_configuration_file
        self.path_output_dir = self._make_output_dir()
        self.parsed_data = []

        self.configuration = Configuration(path_configuration_file)
        self.parser = Parser(self.parsed_data)

    def _make_output_dir(self):
        path_output_dir = self.name_output_dir + "/" + os.path.basename(self.path_configuration_file).split(".")[0]
        if not os.path.exists(path_output_dir):
            os.makedirs(path_output_dir)
            print(f"Created output dir {path_output_dir}.")
        else:
            raise Exception(f"Output directory {path_output_dir} exists already.")
        return path_output_dir

    def parse(self):
        self.parser.parse(self.configuration.data())

if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise Exception("Not enough arguments.")
    
    path_configuration_file = str(sys.argv[1])
    wapp = Wapp(path_configuration_file)
    report = Report()
    plotter = Plotter()

    wapp.parse()
