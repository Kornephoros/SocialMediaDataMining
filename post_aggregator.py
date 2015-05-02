"""
This class will aggregate all of the posts of a specified Facebook page.

It will currently store the count, unique post id, and created time into a CSV file.

Note that this will also store posts that were once active but are now deleted.

Created on Feb 2, 2015

@author: Brandon Connes
"""
import urllib
import json
import time
from aggregator import Aggregator
from comment_parser import CommentParser
from like_parser import LikeParser

'''
    The PageAggregator will take input from the user about the page to cycle through, and the date range to collect from, and will 
    aggregate all of the posts from that date range.
'''


class PostAggregator(Aggregator):
    # The following code will aggregate all of the posts from a Facebook Post.

    def __init__(self):
        super(PostAggregator, self).__init__()
        self.page_object = None

    def do_everything(self):
        self.grab_fb_object_num("post")
        self.grab_info_from_page()
        self.grab_data("likes", False)
        self.grab_data("comments", False)

    def multiple_inputs(self, post_id):
        self.page_object = self.graph.get_object(post_id)
        #time.sleep(1.30)
        self.grab_info_from_page()
        self.grab_data("likes", True)
        self.grab_data("comments", True)

    # This function will grab the next URL for the pagination of data records.
    # Parameter is a page object, like the one generated above.
    @staticmethod
    def grab_next_url(page_post):
        url = page_post['paging']['next']
        response = urllib.urlopen(url)
        data = json.loads(response.read())
        return data

    # This will grab information from a post. If the data set is consistent, then these fields would be very useful.
    def grab_info_from_page(self):
        try:
            self.obj_name = self.page_object['from']['name']
        except KeyError:
            self.obj_name = 'Could not determine page name.'

        try:
            self.obj_type = self.page_object['from']['category']
        except KeyError:
            self.obj_type = 'Could not determine page category.'

    def grab_data(self, type_, multiple):
        if type_ == 'likes':
            lp = LikeParser(self.page_object['id'], self.access_token)
            lp.crunch_post_and_write(self.obj_name, multiple)
        elif type_ == 'comments':
            cp = CommentParser(self.page_object['id'], self.access_token)
            cp.crunch_post_and_write(self.obj_name, multiple)