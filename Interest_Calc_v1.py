'''
Created on 13 Dec 2013

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


import csv
import collections as col

int_base_rate = 1.25

#print calcStdInterest(100,-7.75)

# SPNs = col.OrderedDict()
#
# filename = "SPNs.csv"
#
# f = open(filename, 'rb')
# SPN1 = csv.reader(f,quoting=csv.QUOTE_NONNUMERIC)
# print SPN1
# if ['12345A'] in SPN1:
#     SPNs = col.OrderedDict((row[0], row[1:]) for row in SPN1)

# SPN Key = SPN. Value 1 = Formula Code. Value 2 = Haircut
#===============================================================================
# 
# SPNs['12345A'] = ('A',0.5)
# SPNs['67890A'] = ('B',0.5)
# SPNs['89012A'] = ('C',0.25)
# SPNs['34567B'] = ('D',0.1)
# SPNs['78901G'] = ('E',0.2)
# SPNs['45678F'] = ('F',0.3)
#===============================================================================

#print the dictionary of SPNs with Formula and Haircut

#print SPNs

# filename1 = "Balances.csv"
#
# acctsbal = col.OrderedDict()
#
# b = open(filename1,'rb')
# acctsbal1 = csv.reader(b, quoting=csv.QUOTE_NONNUMERIC)
# accts_bal = col.OrderedDict((row[0], row[1:]) for row in acctsbal1)

# the ability to extract one haircut rate for one SPN

#print SPNs.items()[0][1][1]

#Imagine this is the retrieval of base client and balance data from the DW

#===============================================================================
# acct_balances = col.OrderedDict()
# 
# acct_balances['SPN'] = '12345A'
# acct_balances['OTE'] = 150
# acct_balances['Closing_Bal'] = 50
# acct_balances['TE'] = acct_balances['OTE'] + acct_balances['Closing_Bal']
# acct_balances['IM'] = -30
# acct_balances['MED'] = acct_balances['TE']+acct_balances['IM']
#===============================================================================

#print the dictionary of Balances. Key = Balance Name

#print accts_bal
        
#acct_bal = ('ABCDE',50.0, 150.0, 200.0, -30.0, 170.0)

#===============================================================================
# acct_bal = []
# for val in acct_balances.keys():
#    #acct_bal.append(acct_balances[val])
#    print val
#    acct_bal.append(acct_balances[val])
#    
# 
# print acct_bal
#===============================================================================

#generate the interest bearing balance that will be used in calc_interest function

def buildSPNDicts(SPN):
    filename = "SPNs.csv"
    global SPNs
    SPNs = col.OrderedDict()

    if SPN.upper() == '*ALL':

        f = open(filename, 'rb')
        SPN1 = csv.reader(f,quoting=csv.QUOTE_NONNUMERIC)
        SPNs = col.OrderedDict((row[0], row[1:]) for row in SPN1)

    else:

        f = open(filename,'rb')
        SPN1 = csv.reader(f,quoting=csv.QUOTE_NONNUMERIC)
        rows = [row for row in SPN1 if row[0] == SPN]
        SPNs = col.OrderedDict((row[0], row[1:]) for row in rows)

    return SPNs

def buildBalDict(SPN):
    filename1 = "Balances.csv"
    global accts_bal
    accts_bal = col.OrderedDict()
    if SPN.upper() == "*ALL":
        b = open(filename1,'rb')
        acctsbal1 = csv.reader(b, quoting=csv.QUOTE_NONNUMERIC)
        accts_bal = col.OrderedDict((row[0], row[1:]) for row in acctsbal1)

    else:
        b = open(filename1,'rb')
        acctsbal1 = csv.reader(b, quoting=csv.QUOTE_NONNUMERIC)
        row2 = [row for row in acctsbal1 if row[0] == SPN]
        accts_bal = col.OrderedDict((row[0], row[1:]) for row in row2)

    return accts_bal

def calcIBB(SPN,formula):
    global ibb
    ibb = 0
    if SPN in accts_bal.keys():
        if formula == 'A':
            print "Underlying Balance: OTE"
            ibb = accts_bal[SPN][0]
        elif formula == 'B':
            print "Underlying Balance: TE"
            ibb = accts_bal[SPN][1]
        elif formula == 'C':
            print "Underlying Balance: Closing Balance"
            ibb = accts_bal[SPN][2]
        elif formula == 'D':
            print "Underlying Balance: IM"
            ibb = accts_bal[SPN][3]
        elif formula == 'E':
            print "Underlying Balance: Margin Exc/Def"
            ibb = accts_bal[SPN][4]
        elif formula == 'F':
            print "Underlying Balance: TE + Margin Exc/Def"
            ibb = accts_bal[SPN][1] + accts_bal[SPN][4]
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
        print "HairCut:",SPNs[SPN][1]
        haircut = SPNs[SPN][1]
        final_rate = int_base_rate - haircut
        print "Db/Cr Interest Rate:",final_rate
    else:
        print "SPN to Rate Mapping Not Found."
        final_rate = str(None)
    return final_rate


def calcStdInterest(SPN):

    buildSPNDicts(SPN)
    buildBalDict(SPN)

    if SPN.upper() == '*ALL':
        for z in SPNs.keys():
            form = getFormula(z)
            ibb = calcIBB(z,form)
            rate = getRate(z)
            if form == None or ibb == None:
                print "Please check earlier messages. Missing Data. Interest Not Calculated."
            else:
                print "IBB: %.2f" %ibb
                accrued_interest = ibb * (float(rate)/100)
                if accrued_interest > 0:
                    print 'Accrued Interest: %.2f' %accrued_interest,'\n'
                else:
                    print 'Accrued Interest: %.2f' %accrued_interest
                    accrued_interest = 0
                    print "Negative Interest Value. Accrued Interest set to 0",'\n'
    else:
        form = getFormula(SPN)
        ibb = calcIBB(SPN,form)
        rate = getRate(SPN)
        if form == None or ibb == None:
            print "Please check earlier messages. Missing Data. Interest Not Calculated."
        else:
            print "IBB: %.2f" %ibb
            accrued_interest = ibb * (float(rate)/100)
            if accrued_interest > 0:
                print 'Accrued Interest: %.2f' %accrued_interest,'\n'
            else:
                print 'Accrued Interest: %.2f' %accrued_interest
                accrued_interest = 0
                print "Negative Interest Value. Accrued Interest set to 0",'\n'


def test(got, expected):
    if got == expected:
        prefix = ' OK '
    else:
        prefix = '  X '
    print '%s got: %s expected: %s' % (prefix, repr(got), repr(expected))
  
#===============================================================================
# def main():
#  print 'verbing'
#  test(calcIBB('hail'), 'hailing')
#  test(verbing('swiming'), 'swimingly')
#  test(verbing('do'), 'do')
#===============================================================================
#===============================================================================
#  
# #tests for calc_ibb function
# 
#print "IBB: " + str(calcIBB('12345A','A')),'\n'
#print "IBB: " + str(calcIBB('12345A','B')),'\n'
#print "IBB: " + str(calcIBB('12345A','C')),'\n'
#print "IBB: " + str(calcIBB('12345A','D')),'\n'
#print "IBB: " + str(calcIBB('12345A','E')),'\n'
#print "IBB: " + str(calcIBB('12345A','F')),'\n'
#print "IBB: " + str(calcIBB('12345A','G')),'\n'
# 
# #tests for getFormula function
#    
# print getFormula('12345A'),'\n'
# print getFormula('67890A'),'\n'
# print getFormula('89012A'),'\n'
# print getFormula('34567B'),'\n'
# print getFormula('45678F'),'\n'
# print getFormula('78901G'),'\n'
# print getFormula('777397X'),'\n'
# 
# #tests for getRate function 
# 
# print getRate('12345A'),'\n'
# print getRate('67890A'),'\n'
# print getRate('89012A'),'\n'
# print getRate('34567B'),'\n'
# print getRate('45678F'),'\n'
# print getRate('78901G'),'\n'
# print getRate('777397X'),'\n'
#===============================================================================

#tests for calcStdInterest

# print calcStdInterest('12345A'),'\n'
# print calcStdInterest('67890A'),'\n'
print calcStdInterest('89012A'),'\n'
# print calcStdInterest('34567B'),'\n'
# print calcStdInterest('45678F'),'\n'
# print calcStdInterest('78901G'),'\n'
print calcStdInterest('777397X'),'\n'

print calcStdInterest('*ALL'),'\n'
