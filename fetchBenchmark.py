'''
Created on 5 Feb 2014

@author: R053016
'''

import csv

def fetchBenchmark(date, currency):
    global BenchmarkDict
    BenchmarkDict = {}
    filename = 'BaseRates.csv'
    f = open(filename,'rb')
    reader = csv.reader(f,quoting=csv.QUOTE_NONNUMERIC)

    rows = [ row for row in reader if row[1] == date and row[0] == currency]
    
    for row in rows:
        
        k = (row[1],row[0])
        v = row[2]
        BenchmarkDict[k] = v

    return BenchmarkDict
