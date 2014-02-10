'''
Created on 5 Feb 2014

@author: R053016
'''

import hashlib

def buildAccruedInterest(table,SPN, date, curr, form, int_base_rate, rate, ibb_type, ibb, acc_int, versionID, call_type):
       
    hashes = hashlib.sha1()
    hashes.update(str(versionID))
    record = []
    
    if not ibb_type == " ":
        
        record = [str(SPN), str(date), str(curr), form, int_base_rate, round(rate,2), ibb_type, round(ibb,2), round(acc_int,2), str(hashes.hexdigest()), str(call_type)]
        table.append(record)
        
    else:
        
        pass
