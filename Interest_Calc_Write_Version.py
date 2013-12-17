'''
Created on 17 Dec 2013

@author: R053016
'''

#imports

import csv
import collections as col
import time
import datetime
from Balances import Balances

#Base Interest Rate

int_base_rate = 1.25

#generate the SPN+Formula static dictionary

def buildSPNDict(SPN):
    global SPNs
    filename = "SPNs.csv"

    if SPN.upper() == "*ALL":
        f = open(filename,'rb')
        SPN1 = csv.reader(f,quoting=csv.QUOTE_NONNUMERIC)
        SPNs = col.OrderedDict((row[0], row[1:]) for row in SPN1)
    else:
        f = open(filename, 'rb')
        SPN1 = csv.reader(f,quoting=csv.QUOTE_NONNUMERIC)
        rows = [row for row in SPN1 if row[0] == SPN]
        SPNs = col.OrderedDict((row[0], row[1:]) for row in rows)
    
    return SPNs

def buildBalDict(SPN):
    global accts_bal
    filename = "Balances.csv"
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

def calcIBB(SPN, formula):
    global ibb
    ibb = 0
    for sublist in accts_bal:

        if sublist.spn == SPN:
            print SPN
            print sublist.spn
            if formula == "A":
                print "Underlying Balance: OTE"
                ibb = sublist.ote
            elif formula == "B":
                print "Underlying Balance: TE"
                ibb = sublist.te
            elif formula == "C":
                print "Underlying Balance: Closing Balance"
                ibb = sublist.closing_bal
            elif formula == 'D':
                print "Underlying Balance: IM"
                ibb = sublist.im
            elif formula == 'E':
                print "Underlying Balance: Margin Exc/Def"    
                ibb = sublist.med
            elif formula == 'F':
                print "Underlying Balance: TE + Margin Exc/Def"
                ibb = sublist.ote + sublist.med
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

def buildAccruedInterest(SPN, date, form, int_base_rate, rate, ibb, acc_int, versionID, call_type):

    record = [str(SPN), str(date), form, int_base_rate, round(rate,2), round(ibb,2), round(acc_int,2), t1, str(call_type)]
    table.append(record)
    
def writeAccruedInterest(table):
    filename = open("Accrued Interest.csv", "ab")
    wr = csv.writer(filename, dialect = 'excel')
    for row in table:
        wr.writerow(row)

def calcStdInterest(SPN):
    global t1
    t1 = datetime.datetime.now()
    global call_type
    call_type = str(SPN)
    global table
    table = []
    buildSPNDict(SPN)

    buildBalDict(SPN)

    date = time.strftime("%x")
    
    print date
    error = "Please check earlier messages. Missing Data. Interest Not Calculated."
    version = 0
    
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
            
                buildAccruedInterest(z, date, form, int_base_rate, rate, ibb, accrued_interest, version, call_type)
            
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
            
            buildAccruedInterest(SPN, date, form, int_base_rate, rate, ibb, accrued_interest, version, call_type)
            
    
    writeAccruedInterest(table)
    t2 = datetime.datetime.now()
    print "Execution time: %s" % (t2-t1)

#tests for calcStdInterest

# print calcStdInterest('12345A'),'\n'
# print calcStdInterest('67890A'),'\n'
# print calcStdInterest('89012A'),'\n'
# print calcStdInterest('34567B'),'\n'
# print calcStdInterest('45678F'),'\n'
#print calcStdInterest('78901G'),'\n'
#print calcStdInterest('777397X'),'\n'

print calcStdInterest('*ALL'),'\n'
print calcStdInterest('99991ACM')
