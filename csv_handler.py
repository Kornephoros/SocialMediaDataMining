import csv
import subprocess
import os
import datetime
from facebook import get_app_access_token
from fb_appinfo import FACEBOOK_SECRET_ID, FACEBOOK_APP_ID
from post_aggregator import PostAggregator
from time_handler import TimeHandler

__author__ = 'Brandon Connes'


class Chdir:
    def __init__(self, new_path):
        self.saved_path = os.getcwd()
        os.chdir(new_path)


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
            subprocess.call("dir /d", shell=True)
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
        while not quit_in:
            #try:
                subprocess.call("dir /a:-d", shell=True)
                print "\nPlease input the name of the file you would like to work with:"
                print "Enter 'all' to use all of the files in the current directory."
                file_name = raw_input()
                if file_name == "quit":
                    quit_in = True
                elif file_name == "all":
                    basepath = "./"
                    for fname in os.listdir(basepath):
                        path = os.path.join(basepath, fname)
                        if os.path.isdir(path):
                            continue  # Skip directories
                        else:
                            self.read_file(fname)
                elif os.path.isfile(file_name) and ("likes" in file_name or "comments" in file_name):
                    self.read_file(file_name)
                elif os.path.isfile(file_name) and "posts" in file_name:
                    self.parse_posts(file_name)
                else:
                    print "That is not a file, please try again."

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

    def parse_posts(self, file_name):
        time_handler = TimeHandler()
        time_handler.grab_date_range()
        with open(file_name, 'rb') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                self.posts.append(row['id'])
            pa = PostAggregator()
            for post in self.posts:
                pa.multiple_inputs(post)

    def read_file(self, file_name):
        with open(file_name, 'rb') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                user_id = row['id']
                if user_id in self.users:
                    self.users[user_id] += 1
                else:
                    self.users[user_id] = 1

        with open(self.generate_path(self, file_name), 'wb') as csvfile:
            field_names = ['id', 'count']
            writer = csv.DictWriter(csvfile, field_names)
            writer.writeheader()
            for id_, count in self.users.iteritems():
                writer.writerow({'id': id_, 'count': count})