'''
This class will take a post generated from the post_aggregator class and parse all of the likes that are associated with the post.

Created on Feb 2, 2015

@author: Brandon Connes
'''

import facebook
from facebook import get_app_access_token
import csv
import urllib, json
from fb_appinfo import *

class FB_Parser(object):
    
    # Initialize the parser with a unique post ID.
    def __init__(self, post_id, access_token):
        self.post_id = post_id
        self.access_token = access_token
        
    def set_post_id(self, post_id):
        self.post_id = post_id

class Like_Parser(FB_Parser):
    
    next_page = ''
    num_likes = 0
    
    def reset(self):
        self.num_likes = 0;
        self.next_page = 0;
        
    def crunch_post_and_write(self, post_id, page_name):
        self.reset()
        self.post_id = post_id
        graph = facebook.GraphAPI(get_app_access_token(FACEBOOK_APP_ID, FACEBOOK_SECRET_ID))
        field_names = ['num_likes', 'liker_id', 'liker_name']
        with open(page_name + '/' + post_id + '_likes.csv', 'wb') as csvfile:
            csv_writer = csv.DictWriter(csvfile, field_names)
            while(True):
                try:
                    post_object = graph.get_object(post_id + '/likes', limit = 1000, after = self.next_page)
                except KeyError:
                    print "No likes!"
                    break
                if not post_object['data']:
                    print "End of list for post " + post_id + "!"
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

class Comment_Parser(FB_Parser):
    num_comments = 0
    next_page = ''
    
    def reset(self):
        self.num_comments = 0
        self.next_page = ''
    
    def grab_next_url(self, page_post):
        url = page_post['paging']['next']
        response = urllib.urlopen(url)
        data = json.loads(response.read())
        return data
    
    def crunch_post_and_write(self, post_id, page_name):
        self.reset()
        self.post_id = post_id
        graph = facebook.GraphAPI(get_app_access_token(FACEBOOK_APP_ID, FACEBOOK_SECRET_ID))
        field_names = ['num_comments', 'commenter_id', 'commenter_name', 'comment']
        with open(page_name + '/' + post_id + '_comments.csv', 'wb') as csvfile:
            csv_writer = csv.DictWriter(csvfile, field_names)
            while(True):
                try:
                    post_object = graph.get_object(post_id + '/comments', limit = 500, after = self.next_page)
                except KeyError:
                    print "No comments!"
                    break
                if not post_object['data']:
                    print "End of comments for post " + post_id + "!"
                    print "There were {} comments!".format(self.num_comments)
                try:
                    self.next_page = self.grab_next_url(post_object)
                except KeyError:
                    print "No 'after' paging detected. End of list?"
                comments_from_post = post_object['data']
                
                for commenter in comments_from_post:
                    try:
                        csv_writer.writerow({'num_comments': self.num_comments, 'commenter_id': commenter['from']['id'], 'commenter_name': commenter['from']['name'], 'comment': commenter['message']})
                        print commenter['from']['name'] + ": " + commenter['message']
                    except UnicodeEncodeError:
                        pass # Ignore funky characters
# Generate an access token. -- Consider deleting??
#access_token = get_app_access_token(FACEBOOK_APP_ID, FACEBOOK_SECRET_ID)

# First call to Facebook's Graph API to access a particular Facebook post.
# Facebook post can be viewed here: https://www.facebook.com/5550296508_10153303254681509

# num_likes = 0
# 
# # This call gathers all of the likes from a post. Every like is an array of User ID, and Name.
# likes_from_post = graph.get_object(id = POST_ID + "/likes", limit = '500')['data']
# 
# # This prints the type of Facebook post the post is, i.e. video, picture, link, text, etc..
# print "This post is a " + post['type']
# print "This was posted " + post['created_time']
# 
# # And this prints information about the post. This post is a video, so it prints "Length 0:14"
# #for information in post['properties']:
# #    print " ".join(information.values())
#     
# post = post['likes']
# after = ''
# with open(POST_ID + '_likes.csv', 'wb') as csvfile:
#     csv_writer = csv.writer(csvfile, delimiter= ',', quotechar='|', quoting = csv.QUOTE_MINIMAL)
#     while True:
#         print ""
#         post = graph.get_object( POST_ID + "/likes", after = after, limit='500')
#         
#         # When the final list has been retrived, 'data' is empty, thus we can safely assume the end of a list.
#         if not post['data']:
#             print "End of list!"
#             print "There were {} likes!".format(num_likes)
#             break
#         after = post['paging']['cursors']['after'] # Set up 'after' for next time
#         print after
#         likes_from_post = post['data']
#         
#         for liker in likes_from_post:
#             try:
#                 csv_writer.writerow(["{}".format(num_likes), liker['id'], liker['name']])
#             except UnicodeEncodeError:  # Weird symbols in Facebook name. Decoding possible? Replacing with squares?
#                 csv_writer.writerow(["{}".format(num_likes), liker['id'], "User has a strange character in their name!"])
#             finally:
#                 num_likes += 1