import json
import os
import sys
import pandas as pd
import matplotlib.pyplot
from datetime import datetime


PATH_SAVE = 'plots/'


class PlotInfo:
    '''
        Class that contains all the information about the plot
    '''

    def __init__(self, title: str, sub_directory: str, xlabel: str, ylabel: str, description: str) -> None:

        # all input parameters must be strings and not empty
        if not self.__check_input(title, sub_directory, xlabel, ylabel, description):
            raise Exception(
                'All input parameters must be strings and not empty')

        self.title: str = title
        # if PATH_SAVE + sub_directory + '/' not in sys.path:
        if not os.path.exists(PATH_SAVE + sub_directory + '/'):
            os.makedirs(PATH_SAVE + sub_directory + '/')
        self.sub_directory: str = sub_directory
        self.xlabel: str = xlabel
        self.ylabel: str = ylabel
        self.description: str = description
        self.date_generated: str = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
        self.filename: str = self.__create_filename()

    def __check_input(self, *args):
        '''
            Check if all input parameters are strings and not empty
        '''
        for arg in args:
            if type(arg) != str or arg == '':
                return False
        return True

    def __create_filename(self):
        return f'{PATH_SAVE}{self.sub_directory}/{self.title}.png'


class Plot:
    '''
        Class that contains all the functions to plot the data and perform various visualizations
    '''
    plt = None  # this is the matplotlib.pyplot object, it is initialized in the setup function

    def __init__(self):
        pass

    def show(self):
        self.plt.show()

    def save(self):
        # if path doesn't exist, create it
        if not os.path.exists(PATH_SAVE + self.plot_info.sub_directory + '/'):
            os.makedirs(PATH_SAVE + self.plot_info.sub_directory + '/')
        self.plt.savefig(self.plot_info.filename)
        self.__log_info()

    def __log_info(self):
        # create json file with all the info
        # dict to json
        print(self.plot_info.__dict__)

        json.dump(self.plot_info.__dict__, open(
            PATH_SAVE + self.plot_info.sub_directory + '/' + self.plot_info.title + '.json', 'w'))

    def setup(self, plot_info: PlotInfo):
        '''
            Setup the plot, call this before creating the plot
        '''
        self.plot_info = plot_info
        if self.plt is not None:
            self.plt.clf()
            self.plt.close()
            del self.plt
        # reinitialize
        self.plt: matplotlib.pyplot = sys.modules['matplotlib.pyplot']
        # create new plot, add grid
        self.plt.figure(figsize=(10, 5))
        self.plt.grid(axis='y', alpha=0.75, linestyle='--',
                      linewidth=0.5, color='grey')
        self.plt.grid(axis='x', alpha=0.75, linestyle='--',
                      linewidth=0.5, color='grey')
        self.plt.title(self.plot_info.title)
        self.plt.xlabel(self.plot_info.xlabel)
        self.plt.ylabel(self.plot_info.ylabel)

    def example_histogram(self, some_df: pd.DataFrame, some_df_name: str, some_feature_name: str) -> None:
        ''' Create a plot that should the distribution of values for one feature (input)
        @param some_df: DataFrame
        @param some_df_name: str
        @param some_feature_name: str
        '''
        self.setup()
        self.plt.title(
            f'Distribution of {some_feature_name} in {some_df_name}')
        self.plt.hist(some_df[some_feature_name], bins=100)
        self.plt.xlabel(some_feature_name)
        self.plt.ylabel('Frequency')

    def run(self):
        '''
        Implement this function when inheriting from this class.  Use method example_histogram as a template.
        '''
        return NotImplementedError
