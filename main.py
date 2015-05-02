from post_aggregator import PostAggregator
from page_aggregator import PageAggregator
from csv_handler import CsvHandler


def switch_choice(choice):
    if choice == 1:
        collect_page_data()
    elif choice == 2:
        collect_post_data()
    elif choice == 3:
        analyze_post_data()
    else:
        "You have not entered anything from the menu."


def collect_page_data():
    agg = PageAggregator()
    agg.do_everything()


def collect_post_data():
    agg = PostAggregator()
    agg.do_everything()

def analyze_post_data():
    read = CsvHandler()
    read.do_everything()


menu_length = 3
while True:
    print "Welcome! Please select what you would like to do:"
    print "1. Collect posts from a Facebook Page of your choice"
    print "2. Collect data from a Facebook Post of your choice"
    print "3. Analyze data that you have collected from a Facebook Post"
    try:
        choice = input()
        if choice > menu_length or choice == '' or choice < 1:
            continue
        else:
            switch_choice(choice)
            break
    except ValueError:
        continue
    except SyntaxError:
        continue