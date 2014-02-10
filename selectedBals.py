'''
Created on 5 Feb 2014

@author: R053016
'''

def selectedBals(accts_bal,balances,date):
    global accts
    accts = []
    
    for acct in accts_bal:
    
        if acct.date == date:
        
            accts.append(acct)
    
    return accts
