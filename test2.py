'''
Created on 16 Dec 2013

@author: R053016
'''

import csv

class Balances(object):
    '''
    classdocs
    '''


    def __init__(self, data):
        '''
        Constructor
        '''
        self.spn = data[0].strip()
        self.ote = data[1]
        self.closing_bal = data[2]
        self.te = data[3]
        self.im = data[4]
        self.med = data[5]
        
filename = open("Balances.csv", 'rb')

reader = csv.reader(filename, quoting=csv.QUOTE_NONNUMERIC)

accts_bal = []

SPN = "99697AC"

for row in reader:

    if row[0].strip() == SPN:
        
        accts_bal.append(Balances(row))

    


#-------------------------------------------------------- print accts_bal[0].spn
#-------------------------------------------------------- print accts_bal[0].ote
#------------------------------------------------ print accts_bal[0].closing_bal
#--------------------------------------------------------- print accts_bal[0].te
#--------------------------------------------------------- print accts_bal[0].im
#-------------------------------------------------------- print accts_bal[0].med

def calcIBB(SPN, formula):
    global ibb
    ibb = 0
    for sublist in accts_bal:
        print sublist.spn

        if sublist.spn == SPN:
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
            
    print ibb

calcIBB(SPN,"B")
