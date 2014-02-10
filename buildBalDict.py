'''
Created on 5 Feb 2014

@author: R053016
'''
import csv
from Balances_Date_Currency_v7 import Balances

def buildBalDict(SPN):
    global accts_bal
    filename = "Balances_Date_Currency.csv"
    b = open(filename, 'r')
    reader = csv.reader(b, quoting=csv.QUOTE_ALL)
    accts_bal = []

    if SPN.upper() == "*ALL":

        accts_bal = [Balances(row) for row in reader]
    
    else:

        for row in reader:
        
            if row[0].strip() == SPN:
            
                accts_bal.append(Balances(row))
    
    return accts_bal
