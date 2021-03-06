import calendar
import datetime
import time



'''
    The time handler takes care of all of the messy time format swaps that had to occur. Should be cleaned up
    in the future, but works as expected.
'''
class TimeHandler:
    def __init__(self):
        self.time_from = None
        self.time_until = None

    # Prompts the user for input about time.
    def prompt_for_input(self):
        while True:
                date_range = raw_input("Would you like to specify a date range? y/n  ")
                if date_range == 'y' or date_range == 'n':
                    break
                else:
                    continue

        if date_range == 'y':
            self.grab_date_range()
        if date_range == 'n':
            self.time_until = datetime.datetime.now().strftime('%s')
            self.time_from = 0

    # grabs input from the user.
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

    # Will create time based on user input in epoch time.
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

    # Will grab date range from user
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
            else:
                break

        while True:
            self.datetime_from = self.from_unix_to_datettime(self.time_from)
            self.time_until = raw_input('Please enter the time you\'d like to gather until. Leave blank for "until now". \nThe format is: Y m d H M S\n')
            self.time_until = self.input_time(self.time_until)
            if self.time_until == -1:
                continue
            elif self.time_until == 0:
                self.time_until = calendar.timegm(datetime.datetime.timetuple(datetime.datetime.now()))
                break
            else:
                break

    # converts from unixtime to datettime.
    @staticmethod
    def from_unix_to_datettime(unix):
        d = datetime.datetime.fromtimestamp(int(unix))
        d = d.strftime("%Y-%m-%dT%H%M%S+0000")
        return d

    # converts from fbtime (bad) to datetime (good)
    @staticmethod
    def from_fbtime_to_datetime(fb):
        fb = datetime.datetime.strptime(fb, "%Y-%m-%dT%H:%M:%S+0000")
        print fb
        return fb

    # converts from unixttime to pretty csvtime.
    def from_unixtime_to_csvtime(self, unixtime):
        converted = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(unixtime))
        return converted
