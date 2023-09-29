import os

class Reporter:
    def __init__(self, configuration_data, dataframe, path_output_dir, reports_dir):
        print("Initializing Reporter.")

        self.path_output_dir = path_output_dir
        self.reports_dir = self.path_output_dir + "/" + reports_dir
        if not os.path.exists(self.reports_dir):
            os.mkdir(self.reports_dir)
        self.report_summary_suffix = "summary"
        self.report_data_suffix = "data"

        # initialize configuration and dataframe
        self.configuration_data = configuration_data
        self.dataframe = dataframe
   
    def _need_report(self, metric_parse_configuration):
        return ("report" in metric_parse_configuration and (metric_parse_configuration["report"] == 1 or isinstance(metric_parse_configuration["report"], str)))

    def _get_report_name(self, metric_parse_configuration):
        report_name = metric_parse_configuration["name"]
        if isinstance(metric_parse_configuration["report"], str):
            report_name = metric_parse_configuration["report"]
        return report_name

    def _generate_report(self, report_name, data_file, metric):
        path_report_summary = self.reports_dir + "/" + report_name + "-" + self.report_summary_suffix + ".csv"
        path_report_data = self.reports_dir + "/" + report_name + "-" + self.report_data_suffix + ".csv"

        # save all data
        df_metric = self.dataframe.loc[(self.dataframe["file"] == data_file) & (self.dataframe["metric"] == metric)]
        df_metric.to_csv(path_report_data)

        # save the summary
        description = df_metric["value"].describe()
        description.to_csv(path_report_summary)

    def _generate_report_metric(self, data_file, metric_parse_configuration):
        if not self._need_report(metric_parse_configuration):
            return
        
        report_name = self._get_report_name(metric_parse_configuration)
        metric = metric_parse_configuration["metric"]
        # parse the data frame for the metric and data file you want to be reported
        self._generate_report(report_name, data_file, metric)
        print(f"Generated report for metric \"{metric}\" in data file \"{data_file}\".")

    def generate(self):
        if self.dataframe is None:
            raise Exception("No data(frame) yet to generate reports from.")

        data_files = self.configuration_data.keys()
        for data_file in data_files:
            for metric_parse_configuration in self.configuration_data[data_file]:
                self._generate_report_metric(data_file, metric_parse_configuration)
