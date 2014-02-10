'''
Created on 5 Feb 2014

@author: R053016
'''

def calcIBB(accts,SPN, formula, currency):
    global ibb
    ibb = 0
    global ibb_type
    ibb_type = ' '
    
    for acct in accts:
        
        if acct.spn == SPN and acct.currency == currency:
            
            
            if formula == "A":
    
                print "IBB Balance Type: OTE"
                ibb = acct.ote
                ibb_type = "OTE"
                print "IBB:",ibb
                return (float(ibb),ibb_type)
            
            elif formula == "B":
            
                print "IBB Balance Type: TE"
                ibb = acct.te
                ibb_type = "TE"
                print "IBB:",ibb
                return (float(ibb),ibb_type)
            
            elif formula == "C":
            
                print "IBB Balance Type: Closing Balance"
                ibb = acct.closing_bal
                ibb_type = "Closing Bal"
                print "IBB:",ibb
                return (float(ibb),ibb_type)
            
            elif formula == 'D':
            
                print "IBB Balance Type: IM"
                ibb = acct.im
                ibb_type = "IM"
                print "IBB:",ibb
                return (float(ibb),ibb_type)
            
            elif formula == 'E':
            
                print "IBB Balance Type: Margin Exc/Def"    
                ibb = acct.med
                ibb_type = "MED"
                print "IBB:",ibb
                return (float(ibb),ibb_type)
            
            elif formula == 'F':
            
                print "IBB Balance Type: TE + Margin Exc/Def"
                ibb = float(acct.te) + float(acct.med)
                ibb_type = "TE + MED"
                print "IBB:",ibb
                return (float(ibb),ibb_type)
            
            else:
                
                print "Formula Calculation Method Not Found."
                ibb = None
                return (ibb,ibb_type)
    else:
        
        print "Balance Not Found"
        ibb = None
        return (ibb,ibb_type)
