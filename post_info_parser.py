"""
This class will take a post generated from the post_aggregator class and parse all of the likes
that are associated with the post.

Created on Feb 2, 2015

@author: Brandon Connes
"""

import os
import datetime


class FbParser(object):

    # Initialize the parser with a unique post ID.
    def __init__(self, post_id, access_token):
        self.post_id = post_id
        self.access_token = access_token
        self.obj_name = None
        self.url = None
        self.next_page = None
        self.object_count = 0

    def set_post_id(self, post_id):
        self.post_id = post_id

    # Reset common fields to 0
    def reset(self):
        self.next_page = None
        self.object_count = 0

    # Generate the path to write to
    def generate_path(self, post_id, type_, multiple):
        if multiple:
            path = "../parsed/"
            if not os.path.exists(path):
                try:
                    os.makedirs(path)
                except OSError:
                    print "Could not create directory! [m]"
            return path + "{0}_{1}.csv".format(post_id, type_)
        else:
            path = "./data/" + self.obj_name + "/" + str(datetime.datetime.now().date()) + "/" + type_
            if not os.path.exists(path):
                try:
                    os.makedirs(path)
                except OSError:
                    print "Could not create directory! [s]"
            return path + "/" + str(post_id) + "_@" + str(datetime.datetime.now().time().strftime("%H.%M.%S")) + "_" + str(type_) + ".csv"