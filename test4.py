__author__ = 'Miten'

import csv
from Balances_Date import Balances

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

#    print accts[0].spn
#    print accts[0].date
#    print accts[0].ote
#    print accts[0].te
#    print accts[0].im
#    print accts[0].closing_bal
#    print accts[0].med

    for row in accts:
        print row

    return accts

buildBalDict('EE505AC')
selectedBals(accts_bal,'12-21-2013')