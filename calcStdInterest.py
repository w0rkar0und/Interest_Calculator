'''
Created on 5 Feb 2014

@author: R053016
'''

#===============================================================================
# v1 Iteration
# Functionality:
#
# Build Dictionary containing SPN + Balances from CSV
# Build Dictionary containing SPN + Formula + Haircut from CSV
# Lookup SPN match in both dictionaries
# Generate IBB from the Balances Dictionary based on Formula
# Calculate Applied Interest Rate using haircut
# Ability to run for one SPN or *ALL SPNs
# Generate Print output
#===============================================================================
#===============================================================================
# v2 Iteration
# Functionality:
#
# Write output to CSV file (Accrued Interest.csv):
# SPN, Processing Date, Formula, Base Rate, Applied Rate, IBB, Accrued Interest
# , version ID = 0)
# Added Execution Time "calculation"
#
#===============================================================================
#===============================================================================
# v3 Iteration
# Functionality:
#
# Build Balances object using the Balances Class to replace the SPN + Balances
# Dictionary (function buildBalDict)
# Change calcIBB function to retrieve balance from list of Balances objects
#
#===============================================================================
#===============================================================================
# v4 Iteration
# Functionality:
#
# Changed Version ID value and added Call Type on record written to the output 
# CSV (Accrued Interest.csv): 
# Version ID is now datetime.datetime.now() value generated at start of call to 
# calcStdInt() function
# Call Type is SPN argument passed on calcStdInt() function - will be either 
# single SPN or *ALL
#===============================================================================
#===============================================================================
# v4.1 Iteration
# Functionality:
#
# Fixed calcIBB function - calculation of Formula F IBB was pointing to OTE 
# rather than TE.
# Fixed buildSPNDict to strip the white space around SPN values so that look up
# of SPN works if value is shorter than stored value
# Fixed buildBalDict to strip the white space around SPN values so that look up
# of SPN works if value is shorter than stored value
# Added IBB Type value to the output
# Version ID changed to hash value of datetime.datetime.now()
#===============================================================================
#===============================================================================
# v5 Iteration
# Functionality:
#
# Added value date processing
# Select balances based on date provided on the calcStdInt() function
#===============================================================================


#imports

import datetime
from buildSPNDict import buildSPNDict
from buildBalDict import buildBalDict
from getFormula import getFormula
from selectedBals import selectedBals
from calcIBB import calcIBB
from fetchBenchmark import fetchBenchmark
from getRate import getRate
from buildAccruedInterest import buildAccruedInterest
from writeAccruedInterest import writeAccruedInterest
    


def calcStdInterest(SPN,date):
    t1 = datetime.datetime.now()
    global call_type
    call_type = str(SPN)
    global table
    table = []
    global SPNs
    global accts_bal
    global accts
    global ibb_type
    global BenchmarkDict
    global int_base_rate
    rate = 0
    accrued_interest = 0.00
    
    SPNs = buildSPNDict(SPN)
    
    accts_bal = buildBalDict(SPN)
    
    accts = selectedBals(accts_bal,accts_bal,date)
    
    #print_date = time.strftime("%x")
    
    error = "Please check earlier messages. Missing Data.""\n""Interest Not Calculated."
    
    for acct in accts:
        
        curr = acct.currency
            
        BenchmarkDict = fetchBenchmark(date,curr)
        
        form = getFormula(SPNs,acct.spn,curr)
        
        ibb, ibb_type = calcIBB(accts,acct.spn,form,curr)

        if ibb == None or form == None:

            print error
            pass
        
        else:
            
            rate,int_base_rate = getRate(BenchmarkDict,SPNs,acct.spn,date,curr)
            
            print "IBB: %.2f" %ibb
            accrued_interest = ibb * (float(rate)/100)
            print "Accrued Interest: %.2f" %accrued_interest, '\n'
            
            if accrued_interest < 0 and form <> "D":
                
                accrued_interest = 0
                print "Negative Interest Value for Non-IM IBB. Accrued Interest set to 0",'\n'  
            
        buildAccruedInterest(table,acct.spn, date, acct.currency, form, int_base_rate, rate, ibb_type, ibb, accrued_interest, t1, call_type)
            
    writeAccruedInterest(table)
    
    t2 = datetime.datetime.now()
    
    print "Execution time: %s" % (t2-t1)


#print calcStdInterest('EE505AC','12-20-2013'),'\n'
#print calcStdInterest('91427ACM','12-20-2013'), '\n'
#print calcStdInterest('*ALL','12-20-2013')
