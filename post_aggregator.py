'''
This class will aggregate all of the posts of a specified Facebook page.

It will currently store the count, unique post id, and created time into a CSV file.

Note that this will also store posts that were once active but are now deleted. 

Created on Feb 2, 2015

@author: Brandon Connes
'''
import facebook
import os, traceback
import urllib, json, csv
import datetime, calendar
from facebook import get_app_access_token
from fb_appinfo import *

class Aggregator(object):
    def __init__(self):
        self.access_token = get_app_access_token(FACEBOOK_APP_ID, FACEBOOK_SECRET_ID)
        self.graph = facebook.GraphAPI(self.access_token)
        
    def create_time(self, time_in):
        try:
            time_ary = time_in.split()
            if not time_ary: # User entered nothing
                return 0
            elif len(time_ary) != 6:
                print "Invalid format."
                return -1
            time_dict = {
                         'Y': int(time_ary[0]),
                         'm': int(time_ary[1]),
                         'd': int(time_ary[2]),
                         'H': int(time_ary[3]),
                         'M': int(time_ary[4]),
                         'S': int(time_ary[5])
                         }
            formatted_time = datetime.datetime(time_dict['Y'], time_dict['m'], time_dict['d'], time_dict['H'], time_dict['M'], time_dict['S']) + datetime.timedelta(hours = 4)
            time_since_epoch = calendar.timegm(formatted_time.timetuple())
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
            if(input_ == -1): # User entered a bad format; try again
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
        
class PageAggregator(Aggregator):
    # The following code will aggregate all of the posts from a Facebook Page.
    
    def doEverything(self):
        self.grab_page_num()
        self.grab_info_from_page()
        self.grab_data()
    
    # Prompt user for a page number to aggregate data from.
    #print "Welcome! This program will aggregate the posts and likes of the Facebook Page you enter."
    def grab_page_num(self):
        # Sample page nums: WSJ 125172585561, CNN 5550296508 FOX 15704546335
        while True:
            self.PAGE_NUM = raw_input('Please enter the page number / id: ')
           
            self.time_from = raw_input('Please enter the time you\'d like to gather from. Leave blank for "from now". \nThe format is: Y m d H M S (ex: 2013 04 20 03 21 43 for 04/20/2013 @ 03:21:43)\n')
            self.time_from = self.input_time(self.time_from)
            if(self.time_from == 0): # If nothing was entered, make the time to gather from right now
                self.time_from = calendar.timegm(datetime.datetime.timetuple(datetime.datetime.now()))
            self.datetime_from = self.from_unix_to_datettime(self.time_from)
            self.time_until = raw_input('Please enter the time you\'d like to gather until. Leave blank for "until the end". \nThe format is: Y m d H M S\n')
            self.time_until = self.input_time(self.time_until)
            
            break
        try:
            self.page_object = self.graph.get_object(self.PAGE_NUM)
        except self.facebook.GraphAPIError:
            print "The page you requested does not exist. Please try again.\n"

    # This function will grab the next URL for the pagination of data records.
    # Parameter is a page object, like the one generated above.
    def grab_next_url(self, page_post):
        url = page_post['paging']['next']
        response = urllib.urlopen(url)
        data = json.loads(response.read())
        return data

    def grab_info_from_page(self):
        try:
            self.page_name = self.page_object['name']
        except KeyError:
            self.page_name = 'Could not determine page name.'
        
        try:
            self.page_type = self.page_object['category']
        except KeyError:
            self.page_type = 'Could not determine page category.'

    # This will attempt to create a directory for each page.
    def generate_path(self):    
        if not os.path.exists("./" + self.page_name):
            try:
                os.makedirs("./" + self.page_name)
            except OSError:
                print "Could not create directory!"
        return self.page_name + "/" + self.PAGE_NUM + "_posts.csv"
        
    def grab_data(self):
        with open(self.generate_path(), 'wb') as csv_file:
            field_names = ['post_count', 'post_id', 'created_time']
            csv_writer = csv.DictWriter(csv_file, field_names)
            post_count = 0
            '''
                Due to the weird way that Facebook Open Graph API pagination works, getting just the 'posts' doesn't have an 'after'.
                To combat this, we can grab a URL from the request that we can funnel into our next request. 
            '''
            page_posts = self.graph.get_object(id = self.PAGE_NUM + '/posts', limit = '250', date_format = "U", until = self.time_until, since = self.time_from, fields = 'id, created_time')
            end_flag = False
            while(not end_flag):
                if not page_posts['data']:    # If an empty list is retrieved, we have hit the end of the list
                    break
                data_from_posts = page_posts['data']
                print data_from_posts
                for post in data_from_posts:
                    try:
                        if(post['created_time'] < self.time_from):   # Facebook bug which erases functionality with since / until! :(
                            end_flag = True
                            break 
                        csv_writer.writerow({'post_count': post_count, 'post_id': post['id'], 'created_time': datetime.datetime.fromtimestamp(post['created_time']).strftime('%Y-%m-%d %H:%M:%S')})
#                         lp.crunch_post_and_write(post['id'], page_name)
#                         cp.crunch_post_and_write(post['id'], page_name)
                    except UnicodeEncodeError:  # Weird symbols in Facebook name. Decoding possible? Replacing with squares?
                        csv_writer.writerow(["{}".format(post_count), post['id'], post['created_time']])
                    except facebook.GraphAPIError:
                        print "Something weird happened."
                    finally:
                        post_count += 1
                page_posts = self.grab_next_url(page_posts) # Grab the next page of posts to sort through for the next iteration.
            print "End of list!"
            print "There were {} posts!".format(post_count)
