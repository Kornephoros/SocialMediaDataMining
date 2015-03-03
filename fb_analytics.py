import pandas as pd
import numpy as np


class Analytics():

    def __init__(self):
        pass

    def analyze(self, csvfile):
        ds = pd.read_csv(csvfile)
        ds = pd.DataFrame(csvfile)
        pass