from ..plot.plot import Plot, PlotInfo


class BarChart(Plot):
    def run(self,
            plot_info: PlotInfo,  # this is the plot info object, its required
            json_data: dict,  # up to you what you want to pass in, but you have to pass something
            ) -> None:  # this is the return type, it is optional but recommended

        # you have to include this and call it before you can use the plot
        self.setup(plot_info)

        # bar chart, this is just an example.  You can do whatever you want here
        self.plt.bar(json_data.keys(), json_data.values())
