__author__ = 'Brandon Connes'

import csv


class CsvHandler(object):

    def __init__(self):
        pass

    def generate_path(self, obj):
        pass

    def read_file(self):
        obj = ''
        with open(self.generate_path(obj), 'rb') as csvfile:
            reader = csv.reader(csvfile, delimiter=' ', quotechar='|')
