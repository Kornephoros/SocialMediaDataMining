import csv
import facebook
from facebook import get_app_access_token
import time
from fb_appinfo import FACEBOOK_APP_ID
from fb_appinfo import FACEBOOK_SECRET_ID
from post_info_parser import FbParser


class LikeParser(FbParser):

    def __init__(self, post_id, access_token):
        super(LikeParser, self).__init__(post_id, access_token)

    def crunch_post_and_write(self, obj_name, multiple_flag):
        self.reset()
        self.obj_name = obj_name
        graph = facebook.GraphAPI(get_app_access_token(FACEBOOK_APP_ID, FACEBOOK_SECRET_ID))
        #time.sleep(1.30)

        field_names = ['count', 'id', 'name']
        with open(self.generate_path(self.post_id, "likes", multiple_flag), 'wb') as csvfile:
            csv_writer = csv.DictWriter(csvfile, field_names)
            csv_writer.writeheader()
            while True:
                while True:
                    try:
                        if self.next_page is not None:
                            post_object = graph.get_object(self.post_id + '/likes', limit = 2500, after = self.next_page, fields="id, name")
                            #time.sleep(1.30)
                            break
                        else:
                            post_object = graph.get_object(self.post_id + '/likes', limit = 2500, fields="id, name")
                            #time.sleep(1.30)
                            break
                    except KeyError:
                            print "No likes!"
                            break
                    except facebook.GraphAPIError:
                            print "Facebook Timed Out, retrying after 10 seconds."
                            time.sleep(10.0)
                            continue
                if not post_object['data']:
                    print "End of list for post " + self.post_id + "!"
                    print "There were {} likes!".format(self.object_count)
                    return self.object_count
                try:
                    self.next_page = post_object['paging']['cursors']['after']
                except KeyError:
                    print "No 'after' paging detected. End of list?"
                likes_from_post = post_object['data']
                # likes_p = pd.DataFrame(data = post_object['data'])
                # try:
                #     likes_p.to_csv('panda_output' + self.post_id +'.csv', encoding='utf-8')
                # except UnicodeEncodeError:  # Weird symbols in FB Name.
                #     likes_p = ''.join(i for i in likes_p if ord(i) < 128)
                #     likes_p.to_csv('panda_output_e' + self.post_id+'.csv', encoding='utf-8')
                # finally:
                #     self.object_count += 1
                for liker in likes_from_post:
                    try:
                        csv_writer.writerow({'count': self.object_count, 'id': liker['id'], 'name': liker['name']})
                    except UnicodeEncodeError:  # Weird symbols in FB Name.
                        reformed_name = ''.join(i for i in liker['name'] if ord(i) < 128)
                        csv_writer.writerow({'count': self.object_count, 'id': liker['id'], 'name': reformed_name})
                    finally:
                        self.object_count += 1