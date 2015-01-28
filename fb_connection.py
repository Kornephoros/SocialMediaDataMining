'''
This is a preliminary attempt at generating an access token with Python, and accumulating some data using Facebook's Graph API.

Created on Jan 27, 2015

@author: Brandon Connes
'''
import facebook
from facebook import get_app_access_token
import csv
# Facebook App ID's necessary for generating an access token.
FACEBOOK_APP_ID = '331939727010193'
FACEBOOK_SECRET_ID = '1fe6042123ad75a4496ec58b51b27784'
POST_ID = '5550296508_10153303254681509'

# Generate an access token.
access_token = get_app_access_token(FACEBOOK_APP_ID, FACEBOOK_SECRET_ID)

# First call to Facebook's Graph API to access a particular Facebook post.
# Facebook post can be viewed here: https://www.facebook.com/5550296508_10153303254681509
graph = facebook.GraphAPI(access_token)
post = graph.get_object(id = '5550296508_10153303254681509')

num_likes = 0

# This call gathers all of the likes from a post. Every like is an array of User ID, and Name.
likes_from_post = graph.get_object(id = "5550296508_10153303254681509/likes", limit = '500')['data']

# This prints the type of Facebook post the post is, i.e. video, picture, link, text, etc..
print "This post is a " + post['type']

# And this prints information about the post. This post is a video, so it prints "Length 0:14"
for information in post['properties']:
    print " ".join(information.values())
# This for loop will iterate through the post buffer received from Facebook.
for liker in likes_from_post:
    try:
        print liker['id'] + ", " + liker['name']
    except UnicodeEncodeError:  # Weird symbols in Facebook name. Decoding possible? Replacing with squares?
        print liker['id'] + ", " + "User has strange character in their name!"
    finally:
        num_likes += 1


post = post['likes']
while True:
    print ""
    print post
    after = post['paging']['cursors']['after']
    print after
    post = graph.get_object( POST_ID + "/likes", after = after, limit='500')
    print post
    likes_from_post = post['data']
    if not likes_from_post:
        print "End of list!"
        print "There were {} likes!".format(num_likes)
        break
#     post = graph.get_object(post['likes']['paging']['next'])
#     print post
    for liker in likes_from_post:    
        try:
            print liker['id'] + ", " + liker['name']
        except UnicodeEncodeError:
            print liker['id'] + ", " + "User has strange character in their name!"
        finally:
            num_likes += 1

# This prints the next 'paging' URL to follow.
# NOTE: This can be used to make more API calls! 
# print post['likes']['paging']['next']
# 
# newLikesFromPost = 