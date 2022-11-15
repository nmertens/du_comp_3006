# Updates:
#   9/23/21 - NM - changed filter method to remove unwanted values.
#                - added in example from class. 

# import packages
import sys
import statistics as stats

# grab input
file = sys.stdin

# initialize list
array = []

# input values into list as float object
for i in file:
    array.append(float(i))

# remove missing values
#array.remove(-9999.0)

# only keeping reasonable values
array = array[array >= -273.15]

# calculate statistics
min = min(array)
max = max(array)
average = stats.mean(array)
median = stats.median(array)

# print output
print("min:", min, "max:", max, "average:", average, "median:", median)

# input method used for class (-273.15 is absolute zero)
#array = [float(line) for line in sys.stdin if float(line) >= -273.15]
