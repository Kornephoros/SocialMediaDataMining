import calendar
import csv
import json
import urllib
import time
import datetime
import facebook
from aggregator import Aggregator


class PageAggregator(Aggregator):
    # The following code will aggregate all of the posts from a Facebook Page.

    def __init__(self):
        super(PageAggregator, self).__init__()

    def do_everything(self):
        self.grab_fb_object_num("page")
        self.grab_info_from_page()
        self.grab_data()

    # This function will grab the next URL for the pagination of data records.
    # Parameter is a page object, like the one generated above.
    @staticmethod
    def grab_next_url(page_post):
        url = page_post['paging']['next']
        response = urllib.urlopen(url)
        data = json.loads(response.read())
        return data

    # This function will grab information from the page object. Could be used for further analysis if desired.
    def grab_info_from_page(self):
        try:
            self.obj_name = self.page_object['name']
        except KeyError:
            self.obj_name = 'Could not determine page name.'

        try:
            self.obj_type = self.page_object['category']
        except KeyError:
            self.obj_type = 'Could not determine page category.'

    # Grab information from a page.
    def grab_data(self):
        with open(self.generate_path("posts"), 'wb') as csv_file:
            field_names = ['count', 'id', 'time']
            csv_writer = csv.DictWriter(csv_file, field_names)
            csv_writer.writeheader()

            post_count = 0
            '''
                Due to the weird way that Facebook Open Graph API pagination works, getting just the 'posts' doesn't have an 'after'.
                To combat this, we can grab a URL from the request that we can funnel into our next request. 
            '''
            if self.time_handler.time_until is not None:
                    page_posts = self.graph.get_object(id = self.fb_object_num + '/posts', limit = '250', date_format = "U", until = self.time_handler.time_until, fields = 'id, created_time')
                    #time.sleep(1.30)
            else: # No 'time from' or 'time until', start at the beginning
                page_posts = self.graph.get_object(id = self.fb_object_num + '/posts', limit = '250', date_format = "U", fields = 'id, created_time')
                #time.sleep(1.30)
                self.time_handler.time_until = calendar.timegm(datetime.datetime.timetuple(datetime.datetime.utcnow()))
                self.time_handler.time_from = 1
            end_flag = False
            while not end_flag:
                if not page_posts['data']:    # If an empty list is retrieved, we have hit the end of the list
                    break
                data_from_posts = page_posts['data']
                print data_from_posts
                for post in data_from_posts:
                    try:
                        if post['created_time'] < self.time_handler.time_from:
                            end_flag = True
                            break

                        csv_writer.writerow({'count': post_count, 'id': post['id'], 'time': datetime.datetime.fromtimestamp(post['created_time']).strftime('%Y-%m-%d %H:%M:%S')})
                    except UnicodeEncodeError:  # Weird symbols in Facebook name. Decoding possible? Replacing with squares?
                        csv_writer.writerow(["{}".format(post_count), post['id'], post['created_time']])
                    except facebook.GraphAPIError:
                        print "Something weird happened."
                    finally:
                        post_count += 1
                page_posts = self.grab_next_url(page_posts) # Grab the next page of posts to sort through for the next iteration.
            print "End of list!"
            print "There were {} posts!".format(post_count)