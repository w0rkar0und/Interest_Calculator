'''
Created on 18 Dec 2013

@author: R053016
'''

from SPNs import SPNStatic
import csv

def buildSPNDict(SPN):
    global SPNs
    filename = "smallSPNs.csv"
    b = open(filename, 'rb')
    reader = csv.reader(b, quoting=csv.QUOTE_NONNUMERIC)
    SPNs = []

    if SPN.upper() == "*ALL":
        print "if"
        #SPNs = [SPNStatic(row) for row in reader]
        for row in reader:
            SPNs.append(SPNStatic(row))
        
    else:

        for row in reader:

            if row[0].strip() == SPN:
                SPNs.append(SPNStatic(row))
    

    for row in SPNs:
        print row[0]
    return SPNs
    
        
#buildSPNDict('83775ACM')
buildSPNDict('*ALL')
