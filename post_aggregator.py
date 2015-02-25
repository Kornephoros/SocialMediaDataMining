"""
This class will aggregate all of the posts of a specified Facebook page.

It will currently store the count, unique post id, and created time into a CSV file.

Note that this will also store posts that were once active but are now deleted.

Created on Feb 2, 2015

@author: Brandon Connes
"""
import facebook
import os
import traceback
import urllib
import json
import csv
import datetime
import calendar
import time
from facebook import get_app_access_token
from fb_appinfo import *
from post_info_parser import LikeParser, CommentParser


class Aggregator(object):
    def __init__(self):
        self.access_token = get_app_access_token(FACEBOOK_APP_ID, FACEBOOK_SECRET_ID)
        self.graph = facebook.GraphAPI(self.access_token)
        self.obj_name = None
        self.obj_type = None
        
    @staticmethod
    def create_time(time_in):
        try:
            time_ary = time_in.split()
            if not time_ary:  # User entered nothing
                return 0
            elif len(time_ary) != 6:
                print "Invalid format."
                return -1
            time_dict = {'Y': int(time_ary[0]),
                         'm': int(time_ary[1]),
                         'd': int(time_ary[2]),
                         'H': int(time_ary[3]),
                         'M': int(time_ary[4]),
                         'S': int(time_ary[5])}
            formatted_time = datetime.datetime(time_dict['Y'], time_dict['m'], time_dict['d'], time_dict['H'], time_dict['M'], time_dict['S']) + datetime.timedelta(hours=-4)
            time_since_epoch = calendar.timegm(formatted_time.timetuple())
            print time_since_epoch
            return time_since_epoch
        except TypeError:
            print "TypeError: stop doing funky stuff with data structures"
            return -1
        except ValueError:
            print "ValueError: times must not be out of conventional bounds"
            return -1
        except Exception:
            print "you're gonna have a bad time!"
            traceback.print_exc()
            return -1
            
    def input_time(self, input_):
        while True:
            input_ = self.create_time(input_)
            if input_ == -1: # User entered a bad format; try again
                print "Invalid format. The format is: Y m d H M S (ex: 2013 04 20 03 21 43 for 04/20/2013 @ 3:21:43)"
                continue
            else:
                # Successfully parsed, exit
                break
        return input_
    
    def from_unix_to_datettime(self, unix):
        d = datetime.datetime.fromtimestamp(int(unix))
        d = d.strftime("%Y-%m-%dT%H%M%S+0000")
        return d
    
    def from_fbtime_to_datetime(self, fb):
        fb = datetime.datetime.strptime(fb, "%Y-%m-%dT%H:%M:%S+0000")
        print fb
        return fb

    def grab_date_range(self):
        
        while True:
            self.time_from = raw_input('Please enter the time you\'d like to gather from. Leave blank for "from the beginning'
                                       ' of time". \nThe format is: Y m d H M S (ex: 2013 04 20 03 21 43 for 04/20/2013 @ 03:21:43)\n')
            self.time_from = self.input_time(self.time_from)
            if self.time_from == 0:  # If nothing was entered, make the time to gather from the beginning of the epoch
                self.time_from = 1
                break
            elif self.time_from == -1:
                continue
                #self.time_from = calendar.timegm(datetime.datetime.timetuple(datetime.datetime.now()))
            else:
                break
        
        while True:
            self.datetime_from = self.from_unix_to_datettime(self.time_from)
            self.time_until = raw_input('Please enter the time you\'d like to gather until. Leave blank for "until now". \nThe format is: Y m d H M S\n')
            self.time_until = self.input_time(self.time_until)
            if(self.time_until == -1):
                continue
            elif(self.time_until == 0):
                self.time_until = calendar.timegm(datetime.datetime.timetuple(datetime.datetime.now()))
                break
            else:
                break
            
    # This will attempt to create a directory for each page.
    def generate_path(self, type_):
        path = "./data/" + self.obj_name + "/" + str(datetime.datetime.now().date()) + "/" + type_
        if not os.path.exists(path):
            try:
                os.makedirs(path)
            except OSError:
                print "Could not create directory!"
        return path + "/" + self.obj_name + "_@" + str(datetime.datetime.now().time().strftime("%H.%M.%S")) + "_" + type_ + ".csv"

    def grab_fb_object_num(self, type_):
        while True:
            while True:
                self.fb_object_num = raw_input('Please enter the ' + type_ + ' ID: ')
                try:
                    self.page_object = self.graph.get_object(self.fb_object_num)
                    time.sleep(1.30)
                    break
                except facebook.GraphAPIError:
                    print "The " + type_ + " you requested does not exist. Please try again.\n"
                    continue
           
            while True:
                self.date_range = raw_input("Would you like to specify a date range? y/n  ")
                if self.date_range == 'y' or self.date_range == 'n':
                    break
                else:
                    continue

            if self.date_range == 'y':
                self.grab_date_range()


            break


'''
    The PageAggregator will take input from the user about the page to cycle through, and the date range to collect from, and will 
    aggregate all of the posts from that date range.
'''


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

    def grab_info_from_page(self):
        try:
            self.obj_name = self.page_object['name']
        except KeyError:
            self.obj_name = 'Could not determine page name.'

        try:
            self.obj_type = self.page_object['category']
        except KeyError:
            self.obj_type = 'Could not determine page category.'
        
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
            try:
                page_posts = self.graph.get_object(id = self.fb_object_num + '/posts', limit = '250', date_format = "U", until = self.time_until, fields = 'id, created_time')
                time.sleep(1.30)
            except AttributeError: # No 'time from' or 'time until', start at the beginning
                page_posts = self.graph.get_object(id = self.fb_object_num + '/posts', limit = '250', date_format = "U", fields = 'id, created_time')
                time.sleep(1.30)
                self.time_until = calendar.timegm(datetime.datetime.timetuple(datetime.datetime.utcnow()))
                self.time_from = 1
            end_flag = False
            while not end_flag:
                if not page_posts['data']:    # If an empty list is retrieved, we have hit the end of the list
                    break
                data_from_posts = page_posts['data']
                print data_from_posts
                for post in data_from_posts:
                    try:
                        if post['created_time'] < self.time_from:
                            end_flag = True
                            break
                        # if post['created_time'] > self.time_until or post['created_time'] < self.time_from:   # Facebook bug which erases functionality with since / until! :(
                        #     end_flag = True
                        #     break
                        csv_writer.writerow({'count': post_count, 'id': post['id'], 'time': datetime.datetime.fromtimestamp(post['created_time']).strftime('%Y-%m-%d %H:%M:%S')})
#                         lp.crunch_post_and_write(post['id'], obj_name)
#                         cp.crunch_post_and_write(post['id'], obj_name)
                    except UnicodeEncodeError:  # Weird symbols in Facebook name. Decoding possible? Replacing with squares?
                        csv_writer.writerow(["{}".format(post_count), post['id'], post['created_time']])
                    except facebook.GraphAPIError:
                        print "Something weird happened."
                    finally:
                        post_count += 1
                page_posts = self.grab_next_url(page_posts) # Grab the next page of posts to sort through for the next iteration.
            print "End of list!"
            print "There were {} posts!".format(post_count)


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
        time.sleep(1.30)
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