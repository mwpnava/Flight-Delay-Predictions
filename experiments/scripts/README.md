# Plots

The `plot.py` file contains an class that wraps the module `matplotlib.pyplot`.  The goal of the wrapper class is to provide a simple interface for creating plots and a consistent style for the plots.

The `plot.py` provide an example function that creates a histogram, and that plot has now been implemented in `feature_distribution.py`.  Notice that `self.setup()` should always be called first.  

```python
class FeatureDistribution (Plot):
    def run(self, 
            plot_info: PlotInfo, # this is the plot info object, its required
            df: pd.DataFrame,  # up to you what you want to pass in, but you have to pass something
            feature: str # up to you what you want to pass in, but you have to pass something
            ) -> None: # this is the return type, it is optional but recommended

        # you have to include this and call it before you can use the plot
        self.setup(plot_info)

        # histogram, this is just an example.  You can do whatever you want here
        self.plt.hist(df[feature], bins=100)


if __name__ == '__main__':

    # example usage, called from the command line in the parent directory (./flight-delay-prediction/)
    df = pd.read_csv('datasets/wunderground/ABI_weather_data.csv')
    plot_info = PlotInfo(title='feature distribution of ABI Temperature',
                         sub_directory='feature_distribution',
                         description='This is a histogram of the temperature feature in the ABI weather dataset',
                         xlabel='Temperature (F)',
                         ylabel='Frequency')

    my_plot = FeatureDistribution()
    my_plot.run(plot_info, df, 'temp')

    # unfortunately, you can only show one plot at a time
    # also, you can only .show() or .save(), you can't do both to the current plot
    # my_plot.show()
    my_plot.save()
```

Do not edit plot.py.  If there is a need to add a new plot, create a new function script in the src/plot/ folder and create a class that inherits the Plot class.  The only method that should be overwritten is the run method.  See feature_distribution.py for an example.
