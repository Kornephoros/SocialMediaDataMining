import calendar
import datetime
import os
import time
import traceback
from facebook import get_app_access_token
import facebook
from fb_appinfo import FACEBOOK_APP_ID
from fb_appinfo import FACEBOOK_SECRET_ID
from time_handler import TimeHandler
import time_handler

'''
    The Aggregator is a parent object (children: page_aggregator, post_aggregator) that provides some common
    functionalities between the Facebook aggregation tools used in this program.
'''
class Aggregator(object):

    # Each aggregator needs an Access Token (its 'gateway' into the Facebook Graph),
    # a Graph object which is how it will make calls to the graph,
    # a Time Handler (defined in time_handler.py) which will do all of the time functions.
    # The obj_name and obj_type represent a single object (post, like, or comment) from the Graph API.
    # Todo: Replace all (defunct?) time methods in this class and delegate them to the time_handler
    def __init__(self):
        self.access_token = get_app_access_token(FACEBOOK_APP_ID, FACEBOOK_SECRET_ID)
        self.graph = facebook.GraphAPI(self.access_token)
        self.obj_name = None
        self.obj_type = None
        self.time_handler = TimeHandler()

    # Todo: Delegate this to time_handler
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

    # Todo: Delegate this to time_handler
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

    # def grab_date_range(self):
    #
    #     while True:
    #         self.time_from = raw_input('Please enter the time you\'d like to gather from. Leave blank for "from the beginning'
    #                                    ' of time". \nThe format is: Y m d H M S (ex: 2013 04 20 03 21 43 for 04/20/2013 @ 03:21:43)\n')
    #         self.time_from = self.input_time(self.time_from)
    #         if self.time_from == 0:  # If nothing was entered, make the time to gather from the beginning of the epoch
    #             self.time_from = 1
    #             break
    #         elif self.time_from == -1:
    #             continue
    #         else:
    #             break
    #
    #     while True:
    #         self.datetime_from = from_unix_to_datettime(self.time_from)
    #         self.time_until = raw_input('Please enter the time you\'d like to gather until. Leave blank for "until now". \nThe format is: Y m d H M S\n')
    #         self.time_until = self.input_time(self.time_until)
    #         if self.time_until == -1:
    #             continue
    #         elif self.time_until == 0:
    #             self.time_until = calendar.timegm(datetime.datetime.timetuple(datetime.datetime.now()))
    #             break
    #         else:
    #             break

    # This function will create a directory for each page that the csv_writer can write to.
    # Example: ./data/CNN/2015-04-15/posts/CNN_@21.12.48_posts.csv
    # is a collection of posts gathered on 4-15-2015 at 9:12 PM
    def generate_path(self, type_):
        path = "./data/" + self.obj_name + "/" + str(datetime.datetime.now().date()) + "/" + type_
        if not os.path.exists(path):
            try:
                os.makedirs(path)
            except OSError:
                print "Could not create directory!"
        return path + "/" + self.obj_name + "_@" + str(datetime.datetime.now().time().strftime("%H.%M.%S")) + "_" + type_ + ".csv"

    # This function will grab the ID from the user, check to see if it actually exists, and then prompt
    # the user if they would like to specify a date range.
    def grab_fb_object_num(self, type_):
        while True:
            while True:
                self.fb_object_num = raw_input('Please enter the ' + type_ + ' ID: ')
                try:
                    self.page_object = self.graph.get_object(self.fb_object_num)
                    break
                except facebook.GraphAPIError:
                    print "The " + type_ + " you requested does not exist. Please try again.\n"
                    continue

            self.time_handler.prompt_for_input()

            break