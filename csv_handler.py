import csv
import subprocess
import os
import datetime
from facebook import get_app_access_token
from fb_analytics import Analytics
from fb_appinfo import FACEBOOK_SECRET_ID, FACEBOOK_APP_ID
from post_aggregator import PostAggregator
from time_handler import TimeHandler
import pandas as pd


# Simple Chdir class for navigating directories.
class Chdir:
    def __init__(self, new_path):
        self.saved_path = os.getcwd()
        os.chdir(new_path)

'''
    The CSV Handler will prompt the user about navigating through directories until they are at the
    place they would like to be for data analytics.

    It can analyze _posts.csv, _likes.csv, _comments.csv, or all of the above.
'''
class CsvHandler(object):
    initial_path = "./data"

    def __init__(self):
        self.posts = list()
        self.users = dict()
        self.access_token = get_app_access_token(FACEBOOK_APP_ID, FACEBOOK_SECRET_ID)

    def do_everything(self):
        self.grab_file_from_input()

    # We want to grab navigate through directories until we find the file we want.
    def grab_file_from_input(self):
        Chdir(self.initial_path)
        newline = False
        quit_in = False
        while not newline and not quit_in:
            subprocess.call("dir /d", shell=True)  # List the directory
            print "\nPlease enter the directory you would like to navigate to."
            print "If you have arrived at the directory you would like to read from, just press Enter."
            new_dir = raw_input()
            if new_dir == "quit":
                quit_in = True
            elif new_dir:
                try:
                    Chdir(new_dir)
                except WindowsError or OSError:
                    print "Directory does not exist. Please try again."
            else:
                newline = True
        while not quit_in: # While the user has not entered 'quit'
            #try:
                subprocess.call("dir /a:-d", shell=True)  # List the current directory.
                print "\nPlease input the name of the file you would like to work with:"
                print "Enter 'all' to use all of the files in the current directory,"
                print "or enter 'analyze' to start data analytics."
                print "'analyze a' will analyze all of the posts within a directory."
                print "'analyze p' will analyze the posts and print out ratio information."
                file_name = raw_input()
                if file_name == "quit":
                    quit_in = True
                elif file_name == "all": # If user enters 'all', attempt to use all of the files in the directory.
                    basepath = "./"      # This is intended to be used with comment & like CSVs.
                    for fname in os.listdir(basepath):
                        path = os.path.join(basepath, fname)
                        if os.path.isdir(path):
                            continue  # Skip directories
                        else:
                            self.read_file(fname)
                elif file_name == "analyze":  # 'analyze' will analyze the file entered. This should be used for plotting a single file's contents.
                    print "Enter the name of the file you would like to analyze: "
                    file_name = raw_input()
                    ana = Analytics()
                    ana.analyze(file_name)
                elif file_name == "analyze a": # 'analyze a' will analyze all of the posts within a directory. It will
                    ana = Analytics()          # generate and plot weights based on likes / comments
                    ana.initialize_weights()
                    basepath = "./"
                    for fname in os.listdir(basepath):
                        path = os.path.join(basepath, fname)
                        if os.path.isdir(path):
                            continue   # Skip directories
                        else:
                            ana.determine_posts(fname)
                            ana.determine_users(fname)
                    print ana.initialize_weights()

                    for fname in os.listdir(basepath):
                        path = os.path.join(basepath, fname)
                        if os.path.isdir(path):
                            continue   # Skip directories
                        else:
                            ana.determine_weight(fname)
                    ana.write_to_matrix()
                elif file_name == "analyze p":  # Analyze p will analyze post data in this directory. It will print out
                    ana = Analytics()           # ratios of likes and comments.
                    basepath = "./"
                    for fname in os.listdir(basepath):
                        path = os.path.join(basepath, fname)
                        if os.path.isdir(path):
                            continue   # Skip directories
                        else:
                            ana.determine_posts(fname)
                    ana.initialize_ratios()
                    for fname in os.listdir(basepath):
                        path = os.path.join(basepath, fname)
                        if os.path.isdir(path):
                            continue   # Skip directories
                        else:
                            ana.find_post_counts(fname)
                    print ana.post_ratios
                    ana.calculate_ratios()
                    print ana.post_ratios



                elif os.path.isfile(file_name) and ("likes" in file_name or "comments" in file_name): # If it is a file with likes/comments, read & parse those likes/comments
                    self.read_file(file_name)
                elif os.path.isfile(file_name) and "posts" in file_name: # Read/parse posts
                    self.parse_posts(file_name)
                else:
                    print "That is not a file, please try again."

    # Generating a path for storing CSV files as called by read_file.
    def generate_path(self, file_name):
        obj_type = None
        if 'likes' in str(file_name):
            obj_type = 'likes'
        elif 'comments' in str(file_name):
            obj_type = 'comments'
        elif 'posts' in str(file_name):
            obj_type = 'posts'
        else:
            obj_type = "bad"
        path = "../parsed/{0}/".format(str(datetime.datetime.now().date()))
        if not os.path.exists(path):
            try:
                os.makedirs(path)
            except OSError:
                print "Could not create directory!"
        return path + "{0}_{1}.csv".format(str(
            datetime.datetime.now().time().strftime("%H")), str(obj_type))

    # Parse through a _posts file by prompting for time input and reading every row. It will then aggregate
    # information about those posts.
    def parse_posts(self, file_name):
        time_handler = TimeHandler()
        time_handler.prompt_for_input()

        with open(file_name, 'rb') as csvfile:
            reader = csv.DictReader(csvfile)
            time_from_ = time_handler.from_unixtime_to_csvtime(time_handler.time_from)
            time_until_ = time_handler.from_unixtime_to_csvtime(time_handler.time_until)
            for row in reader:
                row_time_created = row['time']
                if time_from_ <= row_time_created <= time_until_:
                    self.posts.append(row['id'])
            pa = PostAggregator()
            df = pd.DataFrame(data = self.posts, columns = ["IDs"])
            print(df)
            for post in self.posts:
                pa.multiple_inputs(post)

    # This function will gather information from a single file and then write the information to a CSV file.
    # It gathers user IDs and the amount of impressions they have made.
    def read_file(self, file_name):
        with open(file_name, 'rb') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                user_id = row['id']
                if user_id in self.users:
                    self.users[user_id] += 1
                else:
                    self.users[user_id] = 1

        with open(self.generate_path(file_name), 'wb') as csvfile:
            field_names = ['id', 'count']
            writer = csv.DictWriter(csvfile, field_names)
            writer.writeheader()
            for id_, count in self.users.iteritems():
                writer.writerow({'id': id_, 'count': count})

    # merge files will write to a file by merging the files passed to it together.
    # I'm not sure if this is used anywhere?
    def merge_files(self, *args):
        with open("MERGED.csv", 'wb') as csvfile:
            writer = csv.DictWriter(csvfile)
            users_and_impressions = dict()
            for file_name in args:
                with open(file_name, 'rb') as csv_read:
                    reader = csv.DictReader()
                    for row in reader:
                        user_id = row['id']
                        if user_id in users_and_impressions:
                            users_and_impressions['userid']
                        else:
                            self.users[user_id] = 1
                        print file_name