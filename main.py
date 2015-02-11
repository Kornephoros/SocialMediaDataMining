from post_aggregator import PageAggregator
def switch_choice(choice):
    if(choice == 1):
        collect_page_data()
    elif(choice == 2):
        collect_post_data()
    elif(choice == 31):
        analyze_page_data()
    elif(choice == 4):
        analyze_post_data()
    else:
        "You have not entered anything from the menu."
#     return {
#             1 : "You have decided to collect data from a Facebook Page.",
#             2 : "You have decided to collect data from a Facebook Post",
#             3 : "You have decided to analyze data from a Page source",
#             4 : "You have decided to analyze data from a Post source"
#     }.get(choice, "You have not selected something from the menu.")

def collect_page_data():
    agg = PageAggregator()
    agg.doEverything()
def collect_post_data():
    pass
def analyze_page_data():
    pass
def analyze_post_data():
    pass    

print "Welcome! Please select what you would like to do:"
print "1. Collect posts from a Facebook Page of your choice"
print "2. Collect data from a Facebook Post of your choice"
print "3. Analyze data that you have collected from a Facebook Page"
print "4. Analyze data that you have collected from a Facebook Post"

choice = input()
print switch_choice(choice)