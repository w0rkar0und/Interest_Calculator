'''
Created on 6 Feb 2014

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
#===============================================================================
# v6 Iteration
# Functionality:
#
# Added currency based processing
# Select static and rates based on currency of balance 
#===============================================================================
#===============================================================================
# v7 Iteration
# Functionality:
#
# Determine formula and calculate IBB only for those accounts with a balance
# Removed *ALL based if/then loop in calcStdInterest as it was redundant (Single
# account processing or *ALL can be handled by same code)
# Changed calcIBB print narrative
# Removed ibb_check variable in calcIBB function
# Changed Balances class to store balance values as float in object
#===============================================================================
#===============================================================================
# v8 Iteration
# Functionality:
#
# Changed Interest_Calc_v8 to a __main__ calling calcStdInterest*
# Split each function off into an individual module. 
# calcStdInterest module imports the following:
# buildAccruedInterest
# buildBalDict
# buildSPNDict
# calcIBB
# fetchBenchmark
# getFormula
# getRate
# selectedBalances
# writeAccruedInterest
#===============================================================================

#imports

from calcStdInterest import calcStdInterest
    
def main():

    SPN = raw_input("Please enter an account: ")
    date = raw_input("Please enter a date (in MM-DD-YYYY format):")
    calcStdInterest(SPN,date)
    
    
if __name__ == '__main__':
    
    main()
