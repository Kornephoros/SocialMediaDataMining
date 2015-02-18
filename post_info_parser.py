"""
This class will take a post generated from the post_aggregator class and parse all of the likes
that are associated with the post.

Created on Feb 2, 2015

@author: Brandon Connes
"""

import facebook
from facebook import get_app_access_token
import csv, os, urllib, json
import datetime
from fb_appinfo import *


class FbParser(object):

    # Initialize the parser with a unique post ID.
    def __init__(self, post_id, access_token):
        self.post_id = post_id
        self.access_token = access_token
        self.obj_name = None

    def set_post_id(self, post_id):
        self.post_id = post_id

    def generate_path(self, post_id, type_):
        path = "./data/" + self.obj_name + "/" + str(datetime.datetime.now().date()) + "/" + type_
        if not os.path.exists(path):
            try:
                os.makedirs(path)
            except OSError:
                print "Could not create directory!"
        return path + "/" + str(post_id) + "_@" + str(datetime.datetime.now().time().strftime("%H.%M.%S")) + "_" + str(type_) + ".csv"


class LikeParser(FbParser):

    def __init__(self, post_id, access_token):
        super(LikeParser, self).__init__(post_id, access_token)
        self.next_page = 0
        self.num_likes = 0

    def reset(self):
        self.next_page = 0
        self.num_likes = 0

    def crunch_post_and_write(self, obj_name):
        self.reset()
        self.obj_name = obj_name
        graph = facebook.GraphAPI(get_app_access_token(FACEBOOK_APP_ID, FACEBOOK_SECRET_ID))
        field_names = ['num_likes', 'liker_id', 'liker_name']
        with open(self.generate_path(self.post_id, "likes"), 'wb') as csvfile:
            csv_writer = csv.DictWriter(csvfile, field_names)
            while(True):
                try:
                    post_object = graph.get_object(self.post_id + '/likes', limit = 500, after = self.next_page)
                except KeyError:
                    print "No likes!"
                    break
                if not post_object['data']:
                    print "End of list for post " + self.post_id + "!"
                    print "There were {} likes!".format(self.num_likes)
                    return self.num_likes
                try:
                    self.next_page = post_object['paging']['cursors']['after']
                except KeyError:
                    print "No 'after' paging detected. End of list?"
                likes_from_post = post_object['data']

                for liker in likes_from_post:
                    try:
                        csv_writer.writerow({'num_likes': self.num_likes, 'liker_id': liker['id'], 'liker_name': liker['name']})
                    except UnicodeEncodeError:  # Weird symbols in Facebook name. Decoding possible? Replacing with squares?
                        csv_writer.writerow({'num_likes': self.num_likes, 'liker_id': liker['id'], 'liker_name': "User has a strange character in their name!"})
                    finally:
                        self.num_likes += 1


class CommentParser(FbParser):

    def __init__(self, post_id, access_token):
        super(CommentParser, self).__init__(post_id, access_token)
        self.num_comments = None
        self.next_page = None

    def reset(self):
        self.num_comments = 0
        self.next_page = ''

    @staticmethod
    def grab_next_url(page_post):
        url = page_post['paging']['next']
        response = urllib.urlopen(url)
        data = json.loads(response.read())
        return data

    def crunch_post_and_write(self, obj_name):
        self.reset()
        self.obj_name = obj_name
        graph = facebook.GraphAPI(get_app_access_token(FACEBOOK_APP_ID, FACEBOOK_SECRET_ID))
        field_names = ['num_comments', 'comment_time', 'commenter_id', 'commenter_name', 'comment']
        end_flag = False
        with open(self.generate_path(self.post_id, "comments"), 'wb') as csv_file:
            csv_writer = csv.DictWriter(csv_file, field_names)
            while not end_flag:
                try:
                    post_object = graph.get_object(self.post_id + '/comments', limit=250, after=self.next_page)
                except KeyError:
                    print "No comments!"
                    break
                if not post_object['data']:
                    print "End of comments for post " + self.post_id + "!"
                    print "There were {} comments!".format(self.num_comments)
                try:
                    self.next_page = post_object['paging']['cursors']['after']
                except KeyError:
                    print "No 'after' paging detected. End of list?"
                    end_flag = True
                comments_from_post = post_object['data']

                for commenter in comments_from_post:
                    try:
                        csv_writer.writerow({'num_comments': self.num_comments, 'comment_time': commenter["created_time"], 'commenter_id': commenter['from']['id'], 'commenter_name': commenter['from']['name'], 'comment': commenter['message']})
                        print commenter['from']['name'] + ": " + commenter['message']
                    except UnicodeEncodeError:
                        print "Funky character in post"
                        pass
                    finally:
                        self.num_comments += 1
            print "End of comments for post " + self.post_id + "!"
            print "There were {} comments!".format(self.num_comments)