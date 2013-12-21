'''
Created on 16 Dec 2013

@author: R053016
'''

import csv

class Balances(object):
    '''
    classdocs
    '''


    def __init__(self, data):
        '''
        Constructor
        '''
        self.spn = data[0].strip()
        self.date = data[1]
        self.ote = data[2]
        self.closing_bal = data[3]
        self.te = data[4]
        self.im = data[5]
        self.med = data[6]
        
