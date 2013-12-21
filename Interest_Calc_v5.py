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
#===============================================================================

#imports

import csv
import collections as col
import time
import datetime
from Balances_Date import Balances
import hashlib

#Base Interest Rate

int_base_rate = 1.25

#generate the SPN+Formula static dictionary

def buildSPNDict(SPN):
    global SPNs
    filename = "SPNs.csv"

    if SPN.upper() == "*ALL":
        f = open(filename,'rb')
        SPN1 = csv.reader(f,quoting=csv.QUOTE_NONNUMERIC)
        SPNs = col.OrderedDict((row[0].strip(), row[1:]) for row in SPN1)
    else:
        f = open(filename, 'rb')
        SPN1 = csv.reader(f,quoting=csv.QUOTE_NONNUMERIC)
        rows = [row for row in SPN1 if row[0].strip() == SPN]
        SPNs = col.OrderedDict((row[0].strip(), row[1:]) for row in rows)
    
    return SPNs

def buildBalDict(SPN):
    global accts_bal
    filename = "Balances_Date.csv"
    b = open(filename, 'rb')
    reader = csv.reader(b, quoting=csv.QUOTE_NONNUMERIC)
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

def calcIBB(SPN, formula):
    global ibb
    ibb = 0
    global ibb_type
    ibb_type = ' '

    for acct in accts:
        if acct.spn == SPN:
            if formula == "A":
                print "Underlying Balance: OTE"
                ibb = acct.ote
                ibb_type = "OTE"
            elif formula == "B":
                print "Underlying Balance: TE"
                ibb = acct.te
                ibb_type = "TE"
            elif formula == "C":
                print "Underlying Balance: Closing Balance"
                ibb = acct.closing_bal
                ibb_type = "Closing Bal"
            elif formula == 'D':
                print "Underlying Balance: IM"
                ibb = acct.im
                ibb_type = "IM"
            elif formula == 'E':
                print "Underlying Balance: Margin Exc/Def"    
                ibb = acct.med
                ibb_type = "MED"
            elif formula == 'F':
                print "Underlying Balance: TE + Margin Exc/Def"
                ibb = acct.te + acct.med
                ibb_type = "TE + MED"
            else:
                print "Formula Calculation Method Not Found."
                ibb = None
            
    return ibb

def getFormula(SPN):
    
    print "CLIENT SPN:",SPN
    
    if SPN in SPNs.keys():
        print "Formula:",SPNs[SPN][0]
        int_formula = SPNs[SPN][0]
    else:
        print "SPN to Formula Mapping Not Found."
        int_formula = str(None)
    
    return int_formula

def getRate(SPN):
    
    if SPN in SPNs.keys():
        
        print "Base Interest Rate:",int_base_rate
        
        haircut = SPNs[SPN][1]
        print "Haircut:",haircut
        
        final_rate = int_base_rate - haircut
        print "DB/CR Interest Rate:",final_rate
        
    else:
        
        print "SPN to Rate Mapping Not Found."
        
        final_rate = str(None)
        
    return final_rate

def buildAccruedInterest(SPN, date, form, int_base_rate, rate, ibb_type, ibb, acc_int, versionID, call_type):
    hash = hashlib.sha1()
    hash.update(str(versionID))
    record = [str(SPN), str(date), form, int_base_rate, round(rate,2), ibb_type, round(ibb,2), round(acc_int,2), str(hash.hexdigest()), str(call_type)]
    table.append(record)
    
def writeAccruedInterest(table):
    filename = open("Accrued Interest Date.csv", "ab")
    wr = csv.writer(filename, dialect = 'excel')
    for row in table:
        wr.writerow(row)

def calcStdInterest(SPN,date):
    t1 = datetime.datetime.now()
    global call_type
    call_type = str(SPN)
    global table
    table = []
    buildSPNDict(SPN)

    buildBalDict(SPN)
    selectedBals(accts_bal,date)
    print_date = time.strftime("%x")
    
    print print_date
    error = "Please check earlier messages. Missing Data. Interest Not Calculated."
    
    if SPN.upper()=='*ALL':
        for z in SPNs.keys():
            form = getFormula(z)
            ibb = calcIBB(z,form)
            rate = getRate(z)
            if form == str(None) or ibb == str(None):
                print error
                pass
            else:
                print "IBB: %.2f" %ibb
                accrued_interest = ibb * (float(rate)/100)
                print "Accrued Interest: %.2f" %accrued_interest, '\n'
                if accrued_interest < 0:
                    accrued_interest = 0
                    print "Negative Interest Value. Accrued Interest set to 0",'\n'  
            
                buildAccruedInterest(z, date, form, int_base_rate, rate, ibb_type, ibb, accrued_interest, t1, call_type)
            
    else:
            
        form = getFormula(SPN)
        ibb = calcIBB(SPN, form)
        rate = getRate(SPN)
        if form == str(None) or ibb == str(None):
            print error
            pass
        else:
            print "IBB: %.2f" %ibb
            accrued_interest = ibb * (float(rate)/100)
            print "Accrued Interest: %.2f" %accrued_interest, '\n'
            if accrued_interest < 0:
                accrued_interest = 0
                print "Negative Interest Value. Accrued Interest set to 0",'\n'  
            
            buildAccruedInterest(SPN, date, form, int_base_rate, rate, ibb_type, ibb, accrued_interest, t1, call_type)
            
    
    writeAccruedInterest(table)
    t2 = datetime.datetime.now()
    print "Execution time: %s" % (t2-t1)

#tests for calcStdInterest

print calcStdInterest('*ALL','12-21-2013'),'\n'
print calcStdInterest('EE505AC','12-20-2013'),'\n'
#print calcStdInterest('91696ACM')
