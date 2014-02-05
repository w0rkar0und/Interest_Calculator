'''
Created on 17 Dec 2013

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

import csv
import collections as col
import time
import datetime
from Balances_Date_Currency_v6 import Balances
import hashlib

#Base Interest Rate

int_base_rate = 1.25

#generate the SPN+Formula static dictionary

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

#print buildSPNDict("*ALL")
#print SPNs[("91427ACM","USD")][1]
#print buildSPNDict("91427ACM")
#generate SPN+Balances instances of Balances_Date object

def buildBalDict(SPN):
    global accts_bal
    filename = "Balances_Date_Currency.csv"
    b = open(filename, 'r')
    reader = csv.reader(b, quoting=csv.QUOTE_ALL)
    accts_bal = []

    if SPN.upper() == "*ALL":

        accts_bal = [Balances(row) for row in reader]
    
    else:

        for row in reader:
            if row[0].strip() == SPN:
                accts_bal.append(Balances(row))
    
    return accts_bal



def selectedBals(balances,date):
    global accts
    accts = []
    for acct in accts_bal:
        if acct.date == date:
            accts.append(acct)
    return accts

def calcIBB(SPN, formula):
    global ibb
    ibb = 0
    global ibb_type
    ibb_type = ' '
    for acct in accts:
        if SPN[0] == acct.spn and SPN[1] == acct.currency:
            
            
            if formula == "A":
                print "Underlying Balance: OTE"
                ibb = acct.ote
                ibb_type = "OTE"
                print "IBB:",ibb
                return float(ibb)
            elif formula == "B":
                print "Underlying Balance: TE"
                ibb = acct.te
                ibb_type = "TE"
                print "IBB:",ibb
                return float(ibb)
            elif formula == "C":
                print "Underlying Balance: Closing Balance"
                ibb = acct.closing_bal
                ibb_type = "Closing Bal"
                print "IBB:",ibb
                return float(ibb)
            elif formula == 'D':
                print "Underlying Balance: IM"
                ibb = acct.im
                ibb_type = "IM"
                print "IBB:",ibb
                return float(ibb)
            elif formula == 'E':
                print "Underlying Balance: Margin Exc/Def"    
                ibb = acct.med
                ibb_type = "MED"
                print "IBB:",ibb
                return float(ibb)
            elif formula == 'F':
                print "Underlying Balance: TE + Margin Exc/Def"
                ibb = float(acct.te) + float(acct.med)
                ibb_type = "TE + MED"
                print "IBB:",ibb
                return float(ibb)
            
            else:
                print "Formula Calculation Method Not Found."
                ibb = None
                return ibb
    else:
        print "Balance Not Found"
        ibb = None
        return ibb



def getFormula(SPN,currency):
    
    print "CLIENT SPN:",SPN[0]
    print "Currency:",SPN[1]
    
    if SPN in SPNs.keys():
        
        
        int_formula = SPNs[SPN][0]
        print "Formula:",int_formula
    else:
        print "SPN to Formula Mapping Not Found."
        int_formula = str(None)
    
    
    return int_formula

#print getFormula("91427ACM","USD")


def fetchBenchmark(date, currency):
    
    global BenchmarkDict
    BenchmarkDict = {}
    filename = 'BaseRates.csv'
    f = open(filename,'rb')
    reader = csv.reader(f,quoting=csv.QUOTE_NONNUMERIC)

    rows = [ row for row in reader if row[1] == date and row[0] == currency]
    
    for row in rows:
        k = (row[1],row[0])
        
        v = row[2]
        

        BenchmarkDict[k] = v

    return BenchmarkDict

#print fetchBenchmark("12-20-2013","USD")
    
def getRate(SPN,date,currency):
    
    if SPN in SPNs.keys():

        int_base_rate = BenchmarkDict.get((date,currency))
        print "Base Interest Rate:", int_base_rate
        
        haircut = SPNs[SPN][1]
        print "Haircut:",haircut
        
        final_rate = int_base_rate - haircut
        print "DB/CR Interest Rate:",final_rate
        
    else:
        
        print "SPN to Rate Mapping Not Found."
        
        final_rate = str(None)
        
    return final_rate

def buildAccruedInterest(SPN, date, curr, form, int_base_rate, rate, ibb_type, ibb, acc_int, versionID, call_type):

    hashes = hashlib.sha1()
    hashes.update(str(versionID))
    record = []
    if not ibb_type == " ":
        record = [str(SPN), str(date), str(curr), form, int_base_rate, round(rate,2), ibb_type, round(ibb,2), round(acc_int,2), str(hashes.hexdigest()), str(call_type)]
        table.append(record)
    else:
        pass
    
def writeAccruedInterest(table):
    filename = open("Accrued Interest Date Curr.csv", "ab")
    wr = csv.writer(filename, dialect = 'excel')
    for row in table:
        wr.writerow(row)

def calcStdInterest(SPN,date):
    t1 = datetime.datetime.now()
    global call_type
    call_type = str(SPN)
    global table
    table = []
    rate = 0
    accrued_interest = 0.00
    buildSPNDict(SPN)

    buildBalDict(SPN)

    selectedBals(accts_bal,date)
    print_date = time.strftime("%x")
    
    print "Date:",print_date
    error = "Please check earlier messages. Missing Data. Interest Not Calculated."
    
    if SPN.upper()=='*ALL':
        for z in SPNs.keys():
            curr = z[1]
            fetchBenchmark(date,curr)
            form = getFormula(z,SPNs[z][0])
            ibb = calcIBB(z,form)
            
            if ibb == None:
                pass
            
            else:
                
                rate = getRate(z,date,curr)
                if form == str(None) or ibb == str(None):
                    print error
                    pass
    
                else:
                    
                    print "IBB: %.2f" %ibb
                    accrued_interest = ibb * (float(rate)/100)
                    print "Accrued Interest: %.2f" %accrued_interest, '\n'
                    if accrued_interest < 0 and form <> "D":
                        accrued_interest = 0
                        print "Negative Interest Value. Accrued Interest set to 0",'\n'  
                
            buildAccruedInterest(z[0], date, z[1], form, int_base_rate, rate, ibb_type, ibb, accrued_interest, t1, call_type)
            
    else:
        for z in SPNs.keys():
            if z[0] == SPN:
                curr = z[1]
                fetchBenchmark(date,curr)
                form = getFormula(z,SPNs[z][0])
                ibb = calcIBB(z, form)
                if ibb == None:
                    pass
                else:
                    rate = getRate(z,date,curr)
                    if form == str(None) or ibb == str(None):
                        print error
                        pass
                    else:
                        
                        accrued_interest = ibb * (float(rate)/100)
                        print "Accrued Interest: %.2f" %accrued_interest, '\n'
                        if accrued_interest < 0:
                            accrued_interest = 0
                            print "Negative Interest Value. Accrued Interest set to 0",'\n'  
            
            buildAccruedInterest(z[0], date, z[1], form, int_base_rate, rate, ibb_type, ibb, accrued_interest, t1, call_type)
            
    
    writeAccruedInterest(table)
    t2 = datetime.datetime.now()
    print "Execution time: %s" % (t2-t1)

#tests for calcStdInterest

#print calcStdInterest('91427ACM','12-20-2013'),'\n'
#print calcStdInterest('EE505AC','12-19-2013'),'\n'
#print calcStdInterest('EE505AC','12-21-2013'),'\n'
#print calcStdInterest('91696ACM')
print calcStdInterest('*ALL','12-20-2013'),'\n'
