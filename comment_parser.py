import csv
import json
import urllib
import facebook
import time
from facebook import get_app_access_token
from fb_appinfo import FACEBOOK_APP_ID
from fb_appinfo import FACEBOOK_SECRET_ID
from post_info_parser import FbParser


class CommentParser(FbParser):

    def __init__(self, post_id, access_token):
        super(CommentParser, self).__init__(post_id, access_token)
        self.num_comments = None
        self.next_page = None

    @staticmethod
    def grab_next_url(page_post):
        url = page_post['paging']['next']
        response = urllib.urlopen(url)
        data = json.loads(response.read())
        return data

    def crunch_post_and_write(self, obj_name, multiple):
        self.reset()
        self.obj_name = obj_name
        graph = facebook.GraphAPI(get_app_access_token(FACEBOOK_APP_ID, FACEBOOK_SECRET_ID))
        field_names = ['count', 'time', 'id', 'name', 'comment']
        end_flag = False
        with open(self.generate_path(self.post_id, "comments", multiple), 'wb') as csv_file:
            csv_writer = csv.DictWriter(csv_file, field_names)
            csv_writer.writeheader()
            while not end_flag:
                try:
                    post_object = graph.get_object(self.post_id + '/comments', limit=250, after=self.next_page)
                    time.sleep(1.30)
                except KeyError:
                    print "No comments!"
                    break

                if not post_object['data']:
                    print "End of comments for post " + self.post_id + "!"
                    print "There were {} comments!".format(self.num_comments)

                try:
                    self.next_page = post_object['paging']['cursors']['after']
                except KeyError:
                    end_flag = True
                comments_from_post = post_object['data']

                for commenter in comments_from_post:
                    try:
                        csv_writer.writerow({'count': self.num_comments, 'time': commenter["created_time"], 'id': commenter['from']['id'], 'name': commenter['from']['name'], 'comment': commenter['message']})
                    except UnicodeEncodeError:
                        reformed_comment = ''.join(i for i in commenter['message'] if ord(i) < 128)
                        reformed_name = ''.join(i for i in commenter['from']['name'] if ord(i) < 128)
                        csv_writer.writerow({'count': self.num_comments, 'time': commenter["created_time"], 'id': commenter['from']['id'], 'name': reformed_name, 'comment': reformed_comment})
                    finally:
                        self.num_comments += 1

            print "End of comments for post " + self.post_id + "!"
            print "There were {} comments!".format(self.num_comments)