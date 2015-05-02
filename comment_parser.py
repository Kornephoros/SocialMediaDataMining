import csv
import json
import urllib
import facebook
import time
from facebook import get_app_access_token
from fb_appinfo import FACEBOOK_APP_ID
from fb_appinfo import FACEBOOK_SECRET_ID
from post_info_parser import FbParser

'''
    CommentParser is a class of type FbParser. Its role is to be fed the IDs of Facebook Posts, query the
    Facebook Graph API for information about the comments of that post ID, and store the results in a .csv file.
'''
class CommentParser(FbParser):

    # Call on the FbParser's init, initializing vars relative to the comment parser.
    def __init__(self, post_id, access_token):
        super(CommentParser, self).__init__(post_id, access_token)
        self.object_count = None
        self.next_page = None

    # Comments objects can grab the next page by opening a url object by the [paging][next] object in a post.
    # This is a bit of a complicated way to parse through posts but the only way I have found so far.
    @staticmethod
    def grab_next_url(page_post):
        url = page_post['paging']['next']
        response = urllib.urlopen(url)
        data = json.loads(response.read())
        return data

    # This method will do all of the heavy lifting by writing information about Post comments to a .csv file.
    # It iterates through the json object, grabbing appropriate data chunks and storing them in the csv.
    def crunch_post_and_write(self, obj_name, multiple):
        self.reset()
        self.obj_name = obj_name
        graph = facebook.GraphAPI(get_app_access_token(FACEBOOK_APP_ID, FACEBOOK_SECRET_ID))
        #time.sleep(1.30)
        field_names = ['count', 'time', 'id', 'name', 'comment']
        end_flag = False
        with open(self.generate_path(self.post_id, "comments", multiple), 'wb') as csv_file:
            csv_writer = csv.DictWriter(csv_file, field_names)
            csv_writer.writeheader()
            while not end_flag:
                try:
                    # The post object will be different based on whether there is a next page or not.
                    if self.next_page is not None:
                        post_object = graph.get_object(self.post_id + '/comments', limit=250, after=self.next_page)
                    else:
                        post_object = graph.get_object(self.post_id + '/comments', limit=250)
                except KeyError:
                    print "No comments!"
                    break

                if not post_object['data']:
                    print "End of comments for post " + self.post_id + "!"
                    print "There were {} comments!".format(self.object_count)

                try:
                    self.next_page = post_object['paging']['cursors']['after']
                except KeyError:
                    end_flag = True
                except facebook.GraphAPIError:
                    print "Facebook Timed Out, retrying after 10 seconds."
                    time.sleep(10.0)
                    continue
                comments_from_post = post_object['data']

                # This chunk writes the collected data to the CSV file.
                for commenter in comments_from_post:
                    try:
                        csv_writer.writerow({'count': self.object_count, 'time': commenter["created_time"], 'id': commenter['from']['id'], 'name': commenter['from']['name'], 'comment': commenter['message']})
                    except UnicodeEncodeError or KeyError:
                        # Key Error detected. Some funky character. Instead of printing the name / comment, just print IDs instead.
                        # If comment analytics are to be done in the future, this should be changed.
                        csv_writer.writerow({'count': self.object_count, 'time': commenter["created_time"], 'id': commenter['from']['id'], 'name': '', 'comment': ''})
                    finally:
                        self.object_count += 1