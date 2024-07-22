import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt
import os

class Plotter:
    def __init__(self, configuration_data, configuration_plots, dataframe, path_output_dir, plots_dir):
        print("Initializing Plotter.")

        self.path_output_dir = path_output_dir
        self.plots_dir = self.path_output_dir + "/" + plots_dir
        if not os.path.exists(self.plots_dir):
            os.mkdir(self.plots_dir)

        # initialize configuration and dataframe
        self.configuration_data = configuration_data
        self.configuration_plots = configuration_plots
        self.dataframe = dataframe

    def _need_plot(self, metric_parse_configuration):
        return ("plot" in metric_parse_configuration and (metric_parse_configuration["plot"] == 1 or isinstance(metric_parse_configuration["plot"], str)))

    def _get_plot_name(self, metric_parse_configuration):
        plot_name = metric_parse_configuration["name"]
        if isinstance(metric_parse_configuration["plot"], str):
            plot_name = metric_parse_configuration["plot"]
        return plot_name

    def _generate_plot(self, plot_name, data_file, metric, plot_info, add_x_axis_timestamps):
        path_plot = self.plots_dir + "/" + plot_name

        # filter all events
        df_event = self.dataframe.loc[(self.dataframe["file"] == data_file) & (self.dataframe["metric"] == metric) & (self.dataframe["event"].notna())]
        df_event.reset_index()

        # save all data for the metric data
        df_metric = self.dataframe.loc[(self.dataframe["file"] == data_file) & (self.dataframe["metric"] == metric) & (self.dataframe["event"].isna())]
        # reset the index, so the graph x axis starts from 0
        df_metric = df_metric.reset_index()

        plot_title = metric
        x_label = "Measurement"
        y_label = metric
        if plot_info:
            plot_title = plot_info["title"]
            x_label = plot_info["x_label"]
            y_label = plot_info["y_label"]

        # make the plot
        plt.figure(figsize=(20, 5))

        # plot events
        if add_x_axis_timestamps:
            for event_timestamp, event_data in df_event.groupby("timestamp"):
                plt.axvline(event_timestamp, color='green')

        if add_x_axis_timestamps:
            sns.lineplot(x=df_metric["timestamp"], y=df_metric["value"], linewidth=2, marker=".", label=path_plot)
        else:
            sns.lineplot(df_metric["value"], linewidth=1, marker=".", label=path_plot)
        plt.title(plot_title)
        plt.ylabel(y_label)
        plt.xlabel(x_label)
        plt.legend(loc="upper left")
        plt.tight_layout()
        plt.savefig(path_plot)
        plt.close()

    def _generate_plot_metric(self, data_file, metric_parse_configuration):
        if not self._need_plot(metric_parse_configuration):
            return
        
        # extract plot details
        plot_name = self._get_plot_name(metric_parse_configuration)
        metric = metric_parse_configuration["metric"]
        plot_info = None
        if "plot_info" in metric_parse_configuration:
            plot_info = metric_parse_configuration["plot_info"]
        add_x_axis_timestamps = False
        if "parse_timestamp" in metric_parse_configuration:
            add_x_axis_timestamps = True

        # parse the data frame for the metric and data file you want to be reported
        self._generate_plot(plot_name, data_file, metric, plot_info, add_x_axis_timestamps)
        print(f"Generated plot for metric \"{metric}\" in data file \"{data_file}\".")

    # map the names to data files in which their data is to be found
    # @todo: it would be faster to do this only once for all plot lines at initialization 
    def _map_names_to_metric_info(self, names):
        names_to_metric_info = dict()
        for data_file, metrics in self.configuration_data.items(): 
            for metric in metrics:
                if metric["name"] in names: 
                    names_to_metric_info[metric["name"]] = {"metric": metric["metric"], "data_file": data_file}
        return names_to_metric_info

    def _generate_plot_combination(self, plot_name, plot_info):
        path_plot = self.plots_dir + "/" + plot_name

        plot_title = plot_info["title"] if "title" in plot_info else None
        x_label = plot_info["x_label"] if "x_label" in plot_info else None
        y_label = plot_info["y_label"] if "y_label" in plot_info else None

        names_to_metric_info = self._map_names_to_metric_info(plot_info["data"])

        plt.figure(figsize=(20, 5))

        for plot_line in plot_info["data"]:
            df_metric = self.dataframe.loc[(self.dataframe["file"] == names_to_metric_info[plot_line]["data_file"]) & (self.dataframe["metric"] == names_to_metric_info[plot_line]["metric"])]
            # reset the index, so the plots can be mapped over each other and are not sequential
            df_metric = df_metric.reset_index()
            sns.lineplot(df_metric["value"], linewidth=1, marker=".", label=plot_line)
        
        if plot_title:
            plt.title(plot_title)
        if x_label:
            plt.xlabel(x_label)
        if y_label:
            plt.ylabel(y_label)
        plt.legend(loc="upper left")
        plt.tight_layout()
        plt.savefig(path_plot)

    def generate(self):
        if self.dataframe is None:
            raise Exception("No data(frame) yet to generate plots from.")

        data_files = self.configuration_data.keys()
        for data_file in data_files:
            for metric_parse_configuration in self.configuration_data[data_file]:
                self._generate_plot_metric(data_file, metric_parse_configuration)

    def generate_combinations(self):
        if self.dataframe is None:
            raise Exception("No data(frame) yet to generate plots from.")

        plot_names = self.configuration_plots.keys()
        for plot_name in plot_names:
            plot_info = self.configuration_plots[plot_name]
            self._generate_plot_combination(plot_name, plot_info)
            print(f"Generated combined plot \"{plot_name}\".")

