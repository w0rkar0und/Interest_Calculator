'''
Created on 5 Feb 2014

@author: R053016
'''

def getRate(BenchmarkDict,SPNs,SPN,date,currency):
    global int_base_rate
    
    if (SPN,currency) in SPNs.keys():

        int_base_rate = BenchmarkDict.get((date,currency))
        print "Base Interest Rate:", int_base_rate
        lookup_key = (SPN,currency)
        haircut = SPNs[lookup_key][1]
        print "Haircut:",haircut
        final_rate = int_base_rate - haircut
        print "DB/CR Interest Rate:",final_rate
        
    else:
        
        print "SPN to Rate Mapping Not Found."
        final_rate = str(None)
        
    return (final_rate,int_base_rate)
