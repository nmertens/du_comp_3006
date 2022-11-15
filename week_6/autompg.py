""" This module displays information about cars located in the AutoMPG data set
"""

import os
import csv
from collections import namedtuple

class AutoMPG:
    def __init__(self, make, model, year, mpg):
        # make sure the values are the right type
        self.make = str(make)
        self.model = str(model)
        self.year = 1900 + int(year)
        self.mpg = float(mpg)
    
    def __repr__(self):
        return f'AutoMPG(make={self.make}, model={self.model}, year={self.year}, year={self.mpg})'

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

    def __init__(self):
        self._load_data()

    def __iter__(self):
        return iter(self.data)
    
    def __repr__(self):
        return "AutoMPGData()"
    
    def __str__(self):
        return str(self.data)
    
    def _load_data(self):
        clean_file = 'auto-mpg.clean.txt'

        # if the clean file doesn't exist, clean it
        if not os.path.exists(clean_file):
            self._clean_data()
        
        # initialize a namedtuple object
        Record = namedtuple('Record', ['mpg', 'cylinders', 'displacement', 'horsepower', 'weight', \
                                       'acceleration', 'model_year', 'origin', 'car_name'])

        self.data = list() # initialize empty list for data
        with open(clean_file, 'rt') as file:
            reader = csv.reader(file, delimiter = " ", skipinitialspace = True)
            for row in reader:
                record = Record(*row) # * lets you use all elements of row
                auto_object = AutoMPG(record.car_name.split()[0], \
                                      record.car_name.split(maxsplit = 1)[-1], \
                                      record.model_year, \
                                      record.mpg)
                self.data.append(auto_object) 
    
    def _clean_data(self):
        # read from one and write to the other
        with open('auto-mpg.data.txt',  'rt') as in_file, \
             open('auto-mpg.clean.txt', 'wt') as out_file:
            for row in in_file:
                out_file.write(row.expandtabs()) # makes space delimited instead of tab

def main():
    for car in AutoMPGData():
        print(car)

if __name__ == "__main__":
    main()