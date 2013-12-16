'''
Created on 13 Dec 2013

@author: R053016
'''

import csv
import collections as col

filename = "SPNs.csv"
filename1 = "Balances.csv"

SPN = '12345A'

def buildDicts(SPN):
    filename = "SPNs.csv"
    filename1 = "Balances.csv"
    SPNs = col.OrderedDict()
    accts_bal = col.OrderedDict()

    if SPN.upper == "*ALL":

        f = open(filename, 'rb')
        SPN1 = csv.reader(f,quoting=csv.QUOTE_NONNUMERIC)
        SPNs = col.OrderedDict((row[0], row[1:]) for row in SPN1)
        b = open(filename1,'rb')
        acctsbal1 = csv.reader(b, quoting=csv.QUOTE_NONNUMERIC)
        accts_bal = col.OrderedDict((row[0], row[1:]) for row in acctsbal1)
        print SPNs
        print accts_bal

    else:

        f = open(filename,'rb')
        SPN1 = csv.reader(f,quoting=csv.QUOTE_NONNUMERIC)
        rows = [row for row in SPN1 if row[0] == SPN]
        SPNs = col.OrderedDict((row[0], row[1:]) for row in rows)


        b = open(filename1,'rb')
        acctsbal1 = csv.reader(b, quoting=csv.QUOTE_NONNUMERIC)
        row2 = [row for row in acctsbal1 if row[0] == SPN]
        accts_bal = col.OrderedDict((row[0], row[1:]) for row in row2)
        print SPNs
        print accts_bal

buildDicts('12345A')