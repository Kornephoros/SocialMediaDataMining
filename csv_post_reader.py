from facebook import get_app_access_token
from fb_appinfo import FACEBOOK_APP_ID, FACEBOOK_SECRET_ID
from csv_handler import Chdir

class CsvPostReader():
    initial_path = "./data"

    def __init__(self):
        self.posts = list()
        self.users = dict()
        self.access_token = get_app_access_token(FACEBOOK_APP_ID, FACEBOOK_SECRET_ID)
        self.chdir = Chdir()

    def do_everything(self):
        pass