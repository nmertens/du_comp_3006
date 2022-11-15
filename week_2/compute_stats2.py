# import packages
import sys
import csv
import statistics as stats

def main():
    # inputs

    col_num = int(sys.argv[1])

    # this code will run if a .txt file is specified
    if len(sys.argv) == 3:
        file = sys.argv[2]

        array = []

        with open(file, "r") as f:
            reader = csv.reader(f, delimiter = " ", skipinitialspace = True)
            for row in reader:
                array.append(float(row[col_num]))

    # this code will run if a .txt file is NOT specified; looks for stdin
    else:
        file = sys.stdin

        array = []

        reader = csv.reader(file, delimiter = " ", skipinitialspace = True)
        for row in reader:
            array.append(float(row[col_num]))

    # only keeping reasonable values (-273.15 is absolute zero)
    array = [i for i in array if i >= -273.15]

    # sort the array
    array.sort()

    # compute statisitics
    results = compute_stats(array)

    # printing out statistics
    print("min:", results[0], "max:", results[1], "average:", results[2], "median:", results[3])

def compute_stats(array):
    """ Takes in a sorted array and returns minimum, maximum, average,
        and median values """
    # calculate statistics
    if len(array):
        o_min    = min(array)
        o_max    = max(array)
        o_avg    = stats.mean(array)
        o_median = stats.median(array)

        return(o_min, o_max, o_avg, o_median)

    else:
        return None

if __name__ == '__main__':
    main()
