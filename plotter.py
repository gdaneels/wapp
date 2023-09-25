import os

class Plotter:
    def __init__(self, configuration_data, dataframe, path_output_dir, plots_dir):
        print("Initializing Plotter.")

        self.path_output_dir = path_output_dir
        self.plots_dir = self.path_output_dir + "/" + plots_dir
        if not os.path.exists(self.plots_dir):
            os.mkdir(self.plots_dir)

        # initialize configuration and dataframe
        self.configuration_data = configuration_data
        self.dataframe = dataframe

    def generate(self):
        pass
