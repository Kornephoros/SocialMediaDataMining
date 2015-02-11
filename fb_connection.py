# '''
# This is a preliminary attempt at generating an access token with Python, and accumulating some data using Facebook's Graph API.
# 
# Created on Jan 27, 2015
# 
# @author: Brandon Connes
# '''
# import facebook
# from facebook import get_app_access_token
# import csv
# from fb_appinfo import *
# 
# POST_ID = '125172585561_10155099133135562'
# 
# # Generate an access token.
# access_token = get_app_access_token(FACEBOOK_APP_ID, FACEBOOK_SECRET_ID)
# 
# # First call to Facebook's Graph API to access a particular Facebook post.
# # Facebook post can be viewed here: https://www.facebook.com/5550296508_10153303254681509
# graph = facebook.GraphAPI(access_token)
# post = graph.get_object(id = POST_ID)
# 
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
# try:
#     post = post['likes']
# except KeyError:
#     print "No likes!"
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