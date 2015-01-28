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
    
post = post['likes']
after = ''
with open('out.csv', 'wb') as csvfile:
    csv_writer = csv.writer(csvfile, delimiter= ',', quotechar='|', quoting = csv.QUOTE_MINIMAL)
    while True:
        print ""
        post = graph.get_object( POST_ID + "/likes", after = after, limit='500')
        
        # When the final list has been retrived, 'data' is empty, thus we can safely assume the end of a list.
        if not post['data']:
            print "End of list!"
            print "There were {} likes!".format(num_likes)
            break
        after = post['paging']['cursors']['after'] # Set up 'after' for next time
        print after
        likes_from_post = post['data']
        
        for liker in likes_from_post:
            try:
                csv_writer.writerow(["{}".format(num_likes), liker['id'], liker['name']])
            except UnicodeEncodeError:  # Weird symbols in Facebook name. Decoding possible? Replacing with squares?
                print liker['id'] + ", " + "User has strange character in their name!"
            finally:
                num_likes += 1