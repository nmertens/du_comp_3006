""" This module displays information about cars located in the AutoMPG data set
    AutoMPG data is collected from the UCI Machine Learning Databases
"""
import argparse
import csv
from collections import namedtuple
from collections import defaultdict
import logging
import os
import requests
import numpy as np
import matplotlib.pyplot as plt

def log_config():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # call logging.debug() to append something here
    fh = logging.FileHandler('autompg3.log', 'w')
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
        return f'AutoMPG(make={self.make}, model={self.model}, year={self.year}, mpg={self.mpg})'

    def __str__(self):
        return f'"{self.make}","{self.model}","{self.year}","{self.mpg}"'

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
        logging.debug("DEBUG: Sorting AutoMPG objects by make")
        self.data.sort()
        return self.data

    def sort_by_year(self):
        logging.debug("DEBUG: Sorting AutoMPG objects by year")
        self.data.sort(key = lambda x: (x.year, x.make, x.model, x.mpg))
        return self.data

    def sort_by_mpg(self):
        logging.debug("DEBUG: Sorting AutoMPG objects by mpg")
        self.data.sort(key = lambda x: (x.mpg, x.make, x.model, x.year))
        return self.data

    def mpg_by_year(self, plot = False):
        self.year_dict = defaultdict(list)
        for row in self.data:
            self.year_dict[row.year].append(row.mpg)
        for year in self.year_dict.keys():
            self.year_dict[year] = np.mean(self.year_dict[year])

        if plot:
            plt.figure(figsize = (10, 7))
            plt.plot(self.year_dict.keys(), self.year_dict.values(), 'r--')
            plt.title('Average MPG per year')
            plt.show()

        return self.year_dict


    def mpg_by_make(self, plot = False):
        self.make_dict = defaultdict(list)
        for car in self.data:
            self.make_dict[car.make].append(car.mpg)
        for make in self.make_dict.keys():
            self.make_dict[make] = np.mean(self.make_dict[make])
        
        if plot:
            plt.figure(figsize = (10, 7))
            plt.plot(self.make_dict.keys(), self.make_dict.values(), 'r--')
            plt.xticks(rotation = 75)
            plt.title('Average MPG per make')
            plt.show()

        return dict(sorted(self.make_dict.items()))
    
    def _load_data(self):
        logging.debug("DEBUG: Checking auto-mpg.data.txt")
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

        logging.debug("DEBUG: Parsing auto-mpg.clean.txt into AutoMPG objects")

        self.data = list() # initialize empty list for data

        # mispelled words dictionary
        stupid_words = {'chevroelt':'chevrolet', 'chevy':'chevrolet', 'maxda':'mazda', 'mercedes-benz':'mercedes', \
                        'toyouta':'toyota', 'vokswagen':'volkswagen', 'vw':'volkswagen'}
        with open(AutoMPGData.clean_file, 'rt') as in_file:
            reader = csv.reader(in_file, delimiter = " ", skipinitialspace = True)
            logging.debug("DEBUG: Mispelled car names that were replaced:")
            for row in reader:
                record = Record(*row) # * lets you use all elements of row
                make = record.car_name.split()[0]
                if make in stupid_words.keys(): # is the make mispelled?
                    logging.debug(f'-      Old:{make}')
                    make = stupid_words[make]   # if it is replace it with the correct spelling
                    logging.debug(f'-      New:{make}')
                auto_object = AutoMPG(make,   
                                      record.car_name.split(maxsplit = 1)[-1],
                                      record.model_year,
                                      record.mpg)
                self.data.append(auto_object) 
    
    def _clean_data(self):
        logging.debug("DEBUG: File cleaned by applying .expandtabs() method")
        # read from one and write to the other
        with open(AutoMPGData.original_file,  'rt') as in_file, \
             open(AutoMPGData.clean_file, 'wt') as out_file:
            for row in in_file:
                out_file.write(row.expandtabs()) # makes space delimited instead of tab
        
        logging.debug("DEBUG: Cleaning auto-mpg.data.txt")
    
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
    
    def _to_csv(self, file_name, output, sort_method = None):
        if output == 'print':
            with open(file_name, 'w') as csvfile:
                writer = csv.writer(csvfile, delimiter = ',', quoting = csv.QUOTE_ALL)
                writer.writerow(['Make', 'Model', 'Year', 'MPG'])
                if sort_method == 'default':
                    for car in self.sort_by_default():
                        writer.writerow([car.make, car.model, car.year, car.mpg])
                elif sort_method == 'year':
                    for car in self.sort_by_year():
                        writer.writerow([car.make, car.model, car.year, car.mpg])
                elif sort_method == 'mpg':
                    for car in self.sort_by_mpg():
                        writer.writerow([car.make, car.model, car.year, car.mpg])
                else:
                    for car in self.data:
                        writer.writerow([car.make, car.model, car.year, car.mpg])
        elif output == 'mpg_by_year':
            with open(file_name, 'w') as csvfile:
                writer = csv.writer(csvfile, delimiter = ',', quoting = csv.QUOTE_ALL)
                writer.writerow(['Year', 'MPG'])
                for key, value in self.mpg_by_year().items():
                    writer.writerow([key, value])
        elif output == 'mpg_by_make':
             with open(file_name, 'w') as csvfile:
                writer = csv.writer(csvfile, delimiter = ',', quoting = csv.QUOTE_ALL)
                writer.writerow(['Make', 'MPG'])
                for key, value in self.mpg_by_make().items():
                    writer.writerow([key, value])

        logging.debug(f'DEBUG: Auto-MPG file saved to {file_name}.csv file')



def main():
    log_config()

    parser = argparse.ArgumentParser(description= 'analyze Auto MPG data set')
    
    logging.debug("DEBUG: <output> is a required argument, --sort, --ofile, --plot are optional")
    parser.add_argument('output', metavar = '<output>', choices = ['print', 'mpg_by_year', 'mpg_by_make'], action = 'store')
    parser.add_argument('-s', '--sort', choices = ['default', 'year', 'mpg'], action = 'store', dest = 'sort', default = None)
    parser.add_argument('-o', '--ofile', metavar = '<outfile>', type = str, action = 'store', dest = 'ofile_name')
    parser.add_argument('-p', '--plot', action = 'store_true', dest = 'plot', help = 'if specified plots data')

    args = parser.parse_args()

    if args.ofile_name:
        AutoMPGData()._to_csv(args.ofile_name, args.output, args.sort)
    
    if args.output == 'print':
        print('"Make", "Model", "Year", "MPG"')
        if args.sort == 'default':
            for row in AutoMPGData().sort_by_default():
                print(row)
        elif args.sort == 'year':
            for row in AutoMPGData().sort_by_year():
                print(row)
        elif args.sort == 'mpg':
            for row in AutoMPGData().sort_by_mpg():
                print(row)
        else:
            for row in AutoMPGData():
                print(row)
    elif args.output == 'mpg_by_year':
        print('"Year", "MPG"')
        for key, value in AutoMPGData().mpg_by_year(plot = args.plot).items():
            print(f'"{key}", "{value}"')
    elif args.output == 'mpg_by_make':
        print('"Make", "MPG"')
        for key, value in AutoMPGData().mpg_by_make(plot = args.plot).items():
            print(f'"{key}", "{value}"')

    

if __name__ == "__main__":
    main()