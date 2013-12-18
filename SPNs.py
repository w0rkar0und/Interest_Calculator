'''
Created on 18 Dec 2013

@author: R053016
'''

class SPNStatic(object):
    '''
    classdocs
    '''


    def __init__(self, data):
        '''
        Constructor
        '''
        self.spn = data[0].strip()
        self.formula = data[1]
        self.haircut = data[2]
