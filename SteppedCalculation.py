'''
Created on 13 Jan 2014

@author: R053016
'''

base_rate = 1.50

ibb = 550

x1 = 100
x2 = 200
x3 = 300
x4 = 400
x5 = 500
x6 = 600
x7 = 700
x8 = 800
x9 = 900

hc1 = 0.05
hc2 = 0.075
hc3 = 0.1
hc4 = 0.125
hc5 = 0.15
hc6 = 0.175
hc7 = 0.2
hc8 = 0.225
hc9 = 0.25
hc10 = 0.275

def CalcSteppedInterest(balance):
    remaining = balance
    interest = 0
    baserate = base_rate/100
    while remaining > 0:
        print "Remaining Original",remaining
        
        interest = x1 * (baserate - (hc1/100))
        print interest,"x1"
        
        remaining = balance - x1
        print "Remaining X1",remaining
        
        interest = interest + (x2-(x1+1) * (baserate - (hc2/100)))
        print interest,"x2"
        
        remaining -= (x2-x1)
        print "Remaining X2",remaining
        
        interest = interest + (x3-(x2+1) * (baserate - (hc3/100)))
        print interest,"x3"
        
        remaining -= (x3-x2)
        print "Remaining X3",remaining
        
        interest = interest + (x4-(x3+1) * (baserate - (hc4/100)))
        print interest,"x4"
        
        remaining -= (x4-x3)
        print "Remaining X4",remaining
        
        interest = interest + (x5-(x4+1) * (baserate - (hc5/100)))
        print interest,"x5"
        
        remaining -= (x5-x4)
        print "Remaining X5",remaining
        
        interest = interest + (x6-(x5+1) * (baserate - (hc6/100)))
        print interest,"x6"
        
        remaining -= (x6-x5)
        print "Remaining X6",remaining
        
        interest = interest + (x7-(x6+1) * (baserate - (hc7/100)))
        print interest,"x7"
        
        remaining -= (x7-x6)
        print "Remaining X7",remaining
        
        
    print interest
    return interest

CalcSteppedInterest(550)
