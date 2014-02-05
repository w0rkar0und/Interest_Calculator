'''
Created on 07 Jan 14

@author: R053016
'''

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
        self.currency = data[2]
        self.ote = float(data[3])
        self.closing_bal = float(data[4])
        self.te = float(data[5])
        self.im = float(data[6]) * -1
        self.med = float(data[7])
        
