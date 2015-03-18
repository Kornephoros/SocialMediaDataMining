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
        plt.interactive(False)
        # This block creates a dataset of the counts within the csvfile passed.
        counts_only = ds['count']
        with plt.xkcd():
            plt.figure(1)
            plt_ret = plt.hist(counts_only, label='Frequency of '+type_of_file, range=(1, 22), bins=21)
            print plt_ret[0]
            print plt_ret[1]
            plt.clf()
            plt.bar(plt_ret[1][1:-1] - 0.4, plt_ret[0][1:])
            plt.xticks(np.arange(22))
            plt.title(type_of_file + ' for posts')
            plt.legend()
            plt.show()


        print ds
        # greater_than_one = ds[ds['count'] > 1]
        # plt.figure(2)
        # plt.hist(counts_only[counts_only > 1], histtype='bar', label='Frequency of '+type_of_file)
        # plt.title(type_of_file + ' for posts > 1')
        # plt.legend()
        # plt.show()


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
