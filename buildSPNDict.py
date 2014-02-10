'''
Created on 5 Feb 2014

@author: R053016
'''

import csv
import collections as col

def buildSPNDict(SPN):
    global SPNs
    filename = "SPNsv6.csv"
    SPNs = col.OrderedDict()
    if SPN.upper() == "*ALL":
        f = open(filename,'rb')
        SPN1 = csv.reader(f,quoting=csv.QUOTE_NONNUMERIC)
        
        for row in SPN1:
            #print row
            k = (row[0].strip(),row[2])
            v = (row[1],row[3])
            
            SPNs.update({(k,v)})

    else:
        f = open(filename, 'rb')
        SPN1 = csv.reader(f,quoting=csv.QUOTE_NONNUMERIC)
        rows = [row for row in SPN1 if row[0].strip() == SPN]
        
        for row in rows:
            
            #print row
            k = (row[0].strip(),row[2])
            v = (row[1],row[3])
            
            SPNs.update({(k,v)})
    
    return SPNs
