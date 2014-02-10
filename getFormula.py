'''
Created on 5 Feb 2014

@author: R053016
'''

def getFormula(SPNs,SPN,currency):
    print "CLIENT SPN:",SPN
    print "Currency:",currency
    lookup_key = (SPN,currency)

    if lookup_key in SPNs.keys():
        
        int_formula = SPNs[lookup_key][0]
        print "Formula:",int_formula
        
    else:
        
        print "SPN to Formula Mapping Not Found."
        int_formula = str(None)
    
    return int_formula

