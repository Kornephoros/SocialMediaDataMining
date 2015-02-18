import contextlib
import csv
import subprocess
import os

__author__ = 'Brandon Connes'


class Chdir:
    def __init__(self, new_path):
        self.saved_path = os.getcwd()
        os.chdir(new_path)


class CsvHandler(object):

    initial_path = "./data"

    def __init__(self):
        pass

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
                    subprocess.call("dir /d", shell=True)
                except WindowsError, OSError:
                    print "Directory does not exist. Please try again."
            else:
                newline = True
        while not quit_in:
            try:
                subprocess.call("dir /a:-d", shell=True)
                print "Please input the name of the file you would like to work with:"
                file_name = raw_input()
                if file_name == "quit":
                    quit_in = True
                elif os.path.isfile(file_name):
                    self.read_file(file_name)
                else:
                    print "That is not a file, please try again."
            except IOError:
                print "FOF"



    def generate_path(self, obj):
        pass

    def read_file(self):
        obj = ''
        with open(self.generate_path(obj), 'rb') as csvfile:
            reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
