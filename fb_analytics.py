import csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re


class Analytics():

    def __init__(self):
        self.posts_to_analyze = list()
        self.users = list()
        self.weight = list(tuple())
        self.count = 0

        self.post_ratios = list()
        pass

    def determine_type(self, file_name):
        if "likes" in file_name:
            return "likes"
        elif "comments" in file_name:
            return "comments"
        elif "posts" in file_name:
            return "posts"
        else:
            return "bad"

    def analyze(self, csvfile):
        type_of_file = self.determine_type(csvfile)
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
            #print plt_ret[0]
            #print plt_ret[1]
            plt.clf()
            plt.bar(plt_ret[1][1:-1] - 0.4, plt_ret[0][1:]) # Bar graph, from 1 : the end. -0.4 to center the chart.
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

    def determine_posts(self, csvfile):
        try:
            regex = re.compile("([0-9])+_+([0-9])+")   # Gathers the post ID from a string Ex: 5556667231_32144112
            post_id = regex.match(csvfile).group()
            if post_id in self.posts_to_analyze:
                pass
            else:
                self.posts_to_analyze.append(post_id)
        except AttributeError:
            pass # An input did not match the Regex arg.

    def determine_users(self, file_name):
        with open(file_name, 'rb') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                user_id = row['id']
                if user_id in self.users:
                    pass
                else:
                    self.users.append(user_id)
        self.count += 1
        print self.count

    def initialize_weights(self):
        size_of_matr = (self.users.__len__(), self.posts_to_analyze.__len__())
        self.weight = pd.DataFrame(0, index = self.users, columns = self.posts_to_analyze) # Creates a DataFrame of size [users X posts] and fills with 0s

    def determine_weight(self, file_name):
        regex = re.compile("([0-9])+_+([0-9])+")   # Gathers the post ID from a string Ex: 5556667231_32144112
        post_id = regex.match(file_name).group()

        type = self.determine_type(file_name)
        with open(file_name, 'rb') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                user_id = row['id']
#                ana.weight.ix['10153162120909267', '5550296508_10152442461411509'] = 1
#                print ana.weight.at['10153162120909267', '5550296508_10152442461411509']
                if type == "likes":
                    self.weight.ix[user_id, post_id] += 1
                    print "Successful like parsing of post " + post_id + " with user " + user_id
                elif type == "comments":
                    self.weight.ix[user_id, post_id] += 0.5
                    print "Successful comment parsing of post " + post_id + " with user " + user_id
                else:
                    print "something went wrong during weight analysis"

    def plot_weights(self):
        self.weight.to_csv("./results/DataFrameProto.csv")
        #ana.weight.ix['10153162120909267', '5550296508_10152442461411509'] = 1
        #print ana.weight.at['10153162120909267', '5550296508_10152442461411509']
        plt.figure(1)
        plt.plot(self.weight, label='Weights')
        plt.show()
#        plt_ = self.weight.plot()

    def initialize_ratios(self):
        self.post_ratios = pd.DataFrame(0, index = self.posts_to_analyze, columns = ["likes", "comments", "ratio", "total_impressions"])

    def find_post_counts(self, file_name):
        type = self.determine_type(file_name)
        regex = re.compile("([0-9])+_+([0-9])+")   # Gathers the post ID from a string Ex: 5556667231_32144112
        post_id = regex.match(file_name).group()
        count = 0
        with open(file_name, 'rb') as csvfile:
            for i, l in enumerate(csvfile):
                pass
            count = i + 1
        self.post_ratios.ix[post_id, type] = count

    def calculate_ratios(self):
        for index, row in self.post_ratios.iterrows():
            num_likes = self.post_ratios[index, "likes"]
            num_comments = self.post_ratios[index, "comments"]