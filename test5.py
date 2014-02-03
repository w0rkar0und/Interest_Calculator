'''
Created on 26 Dec 2013

@author: R053016
'''

import csv
from collections import namedtuple

filename = 'Bal_Date_Test5.csv'

#===============================================================================
# with open('Bal_Date_Test5.csv', 'r') as infile:
#    reader = csv.reader(infile)
#    Data = namedtuple("Data",next(reader), verbose=True, rename=True)
#    for row in reader:
#        data = Data(row,' ',' ',' ',' ',' ',' ')
#        
# for row in data:
#    print row
#===============================================================================
    
with open(filename, 'rb') as f:
    reader = csv.reader(f)
    CSVLine = namedtuple("Data",reader[0])
    for line in reader:
        print line
        data = CSVLine._make(line)
        
print data.spn
print data.ote
