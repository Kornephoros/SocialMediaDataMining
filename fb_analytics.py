import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class Analytics():

    def __init__(self):
        pass

    def analyze(self, csvfile):
        type_of_file = None
        if 'likes' in csvfile:
            type_of_file = 'likes'
        elif 'comments' in csvfile:
            type_of_file = 'comments'
        elif 'posts' in csvfile:
            type_of_file = 'posts'
        else:
            type_of_file = 'bad'
        ds = pd.read_csv(csvfile)
        assert isinstance(ds, pd.DataFrame)
#       print(ds)
#        print(ds['count'].max())
        #ds = ds['count'].cumsum()

#        plt.plot(ds, 'ro')

        # This block creates a dataset of the counts within the csvfile passed.
        counts_only = ds['count']
        plt.figure(1)
        plt.hist(counts_only, normed=1, histtype='bar', label='Frequency of '+type_of_file)
        plt.title(type_of_file + ' for posts')
        plt.legend()
        plt.show()



        # plt.figure()
        # plt.legend(loc='best')
        # max_value = ds['count'].max()
        # print max_value
        # max_ID = ds['id'][ds['count'] == max_value]
        # text_on_plot = str(max_value) + ' - ' + str(max_ID)
        # assert isinstance(plt, matplotlib)
        #
        # plt.annotate(text_on_plot, xy=(1, max_value), xytext=(8,0), xycoords=('axes fraction', 'data'), textcoords='offset points')
        # print(ds['id'][ds['count'] > 20])
        #
