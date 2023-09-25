import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt
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

    def _need_plot(self, metric_parse_configuration):
        return ("plot" in metric_parse_configuration and (metric_parse_configuration["plot"] == 1 or isinstance(metric_parse_configuration["plot"], str)))

    def _get_plot_name(self, metric_parse_configuration):
        plot_name = metric_parse_configuration["name"]
        if isinstance(metric_parse_configuration["plot"], str):
            plot_name = metric_parse_configuration["plot"]
        return plot_name

    def _generate_plot(self, plot_name, data_file, metric):
        path_plot = self.plots_dir + "/" + plot_name

        # save all data
        df_metric = self.dataframe.loc[(self.dataframe["file"] == data_file) & (self.dataframe["metric"] == metric)]

        # make the plot
        plt.figure(figsize=(20, 5))
        sns.lineplot(df_metric["value"], linewidth=1, marker=".", label=path_plot)
        plt.title("{0} over time".format(metric))
        plt.ylabel("{0}".format(metric))
        plt.xlabel('measurement')
        plt.legend(loc="upper left")
        plt.tight_layout()
        plt.savefig(path_plot)

    def _generate_plot_metric(self, data_file, metric_parse_configuration):
        if not self._need_plot(metric_parse_configuration):
            return
        
        plot_name = self._get_plot_name(metric_parse_configuration)
        metric = metric_parse_configuration["metric"]
        # parse the data frame for the metric and data file you want to be reported
        self._generate_plot(plot_name, data_file, metric)
        print(f"Generated plot for metric \"{metric}\" in data file \"{data_file}\".")

    def generate(self):
        if self.dataframe is None:
            raise Exception("No data(frame) yet to generate plots from.")

        data_files = self.configuration_data.keys()
        for data_file in data_files:
            for metric_parse_configuration in self.configuration_data[data_file]:
                self._generate_plot_metric(data_file, metric_parse_configuration)
