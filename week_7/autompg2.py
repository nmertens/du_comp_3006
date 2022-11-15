""" This module displays information about cars located in the AutoMPG data set
    AutoMPG data is collected from the UCI Machine Learning Databases
"""
import argparse
import csv
from collections import namedtuple
import logging
import os
import requests

def log_config():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # call logging.debug() to append something here
    fh = logging.FileHandler('autompg2.log', 'w')
    fh.setLevel(logging.DEBUG)
    logger.addHandler(fh)

    # call logging.info() to append something here
    sh = logging.StreamHandler()
    sh.setLevel(logging.INFO)
    logger.addHandler(sh)

class AutoMPG:
    def __init__(self, make, model, year, mpg):
        # make sure the values are the right type
        self.make = str(make)
        self.model = str(model)
        self.year = 1900 + int(year)
        self.mpg = float(mpg)
    
    def __repr__(self):
        return f"AutoMPG(make={self.make}, model={self.model}, year={self.year}, mpg={self.mpg})"

    def __str__(self):
        return f"AutoMPG('{self.make}','{self.model}',{self.year},{self.mpg})"

    def __eq__(self, other):
        # make sure types are the same
        if type(self) == type(other):
            return self.make == other.make and \
                   self.model == other.model and \
                   self.year == other.year and \
                   self.mpg == other.mpg
        else:
            return NotImplemented

    def __lt__(self, other):
        # make sure types are the same
        if type(self) == type(other):
            return (self.make, self.model, self.year, self.mpg) < \
                   (other.make, other.model, other.year, other.mpg)
        else:
            return NotImplemented
    
    def __hash__(self):
        # return the hash of the tuple
        return hash((self.make, self.model, self.year, self.mpg))

class AutoMPGData:

    original_file = 'auto-mpg.data.txt'
    clean_file    = 'auto-mpg.clean.txt'

    def __init__(self):
        self._load_data()

    def __iter__(self):
        return iter(self.data)
    
    def __repr__(self):
        return "AutoMPGData()"
    
    def __str__(self):
        return str(self.data)

    def sort_by_default(self):
        logging.info("INFO: Sorting AutoMPG objects by make")
        self.data.sort()
        return self.data

    def sort_by_year(self):
        logging.info("INFO: Sorting AutoMPG objects by year")
        self.data.sort(key = lambda x: x.year)
        return self.data

    def sort_by_mpg(self):
        logging.info("INFO: Sorting AutoMPG objects by mpg")
        self.data.sort(key = lambda x: x.mpg)
        return self.data
    
    def _load_data(self):
        logging.info("INFO: Checking auto-mpg.data.txt")
        # if original file doesn't exist, pull from website
        if not os.path.exists(AutoMPGData.original_file):
            self._get_data()

        # if the clean file doesn't exist, clean it
        if not os.path.exists(AutoMPGData.clean_file):
            self._clean_data()
        
        # initialize a namedtuple object
        logging.debug("DEBUG: Record objects are of type <namedtuple>")
        Record = namedtuple('Record', ['mpg', 'cylinders', 'displacement', 'horsepower', 'weight', \
                                       'acceleration', 'model_year', 'origin', 'car_name'])

        logging.info("INFO: Parsing auto-mpg.clean.txt into AutoMPG objects")

        self.data = list() # initialize empty list for data
        with open(AutoMPGData.clean_file, 'rt') as in_file:
            reader = csv.reader(in_file, delimiter = " ", skipinitialspace = True)
            for row in reader:
                record = Record(*row) # * lets you use all elements of row
                logging.debug("DEBUG: Record objects filtered into AutoMPG objects")
                auto_object = AutoMPG(record.car_name.split()[0], \
                                      record.car_name.split(maxsplit = 1)[-1], \
                                      record.model_year, \
                                      record.mpg)
                self.data.append(auto_object) 
    
    def _clean_data(self):
        logging.debug("DEBUG: File cleaned by applying .expandtabs() method")
        # read from one and write to the other
        with open(AutoMPGData.original_file,  'rt') as in_file, \
             open(AutoMPGData.clean_file, 'wt') as out_file:
            for row in in_file:
                out_file.write(row.expandtabs()) # makes space delimited instead of tab
        
        logging.info("INFO: Cleaning auto-mpg.data.txt")
    
    def _get_data(self):
        logging.debug("DEBUG: auto-mpg.data.txt accessed from UCI Machine Learning Database")
        logging.info("INFO: Getting auto-mpg.data.txt")
        # access original dataset from url
        url = "https://archive.ics.uci.edu/ml/machine-learning-databases/auto-mpg/auto-mpg.data"
        response = requests.get(url)

        # write the content to .txt file
        with open('auto-mpg.data.txt', 'wb') as outfile:
            outfile.write(response.content)

        logging.debug(f"DEBUG: Response code from url request: {response.status_code}")

def main():
    log_config()

    parser = argparse.ArgumentParser(description= 'analyze Auto MPG data set')
    
    logging.debug("DEBUG: <print> is a required argument, --sort is optional")
    parser.add_argument('print', metavar = '<print>', type = lambda x: bool(x), help = 'print sorted Auto MPG data')
    parser.add_argument('-s', '--sort', choices = ['default', 'year', 'mpg'], action = 'store', dest = 'sort')

    args = parser.parse_args()

    if args.print == True:
        if args.sort == 'default':
            for car in AutoMPGData().sort_by_default():
                print(car)
        elif args.sort == 'year':
            for car in AutoMPGData().sort_by_year():
                print(car)
        elif args.sort == 'mpg':
            for car in AutoMPGData().sort_by_mpg():
                print(car)
        else:
            for car in AutoMPGData():
                print(car)
    

if __name__ == "__main__":
    main()