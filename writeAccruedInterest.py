'''
Created on 6 Feb 2014

@author: R053016
'''

import csv

def writeAccruedInterest(table):
    filename = open("Accrued Interest Date Curr.csv", "ab")
    wr = csv.writer(filename, dialect = 'excel')
    
    for row in table:
        
        wr.writerow(row)
