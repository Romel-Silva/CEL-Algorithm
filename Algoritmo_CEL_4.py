#This code is an integral part of the article "LIMA, J. D. de; SILVA, R. da R. da; DRANKA,G. G.; RIBEIRO, M. H. D. M.; SOUTHIER, L. F. Introducing Conditional Expected Loss: A Novel Metric for Risk Investment Analysis. The Engineering Economist, 2024".

#####################################################################
# MCS (Monte Carlo Simulation)
# NPV  (Net Present Value)
# P(NPV < 0) (probability of financial failure in general)
# VaR  (Value at Risk)
# CVaR  (Conditional Value at Risk)
# VaR_alpha (Value at Risk at specific level)
# CEL (expected value in case of financial insufficiency)
#####################################################################

import numpy as np
import sys

######################################################################
#Input data (you can adjust for your situation)
#The lines below enable interactive data input by the user. You can comment out this section and uncomment the section below to allow direct data entry into the script, if desired. 
print("Please enter the following data:")

Planning_Horizon = int(input("Planning Horizon (number of periods): "))
Number_of_simulations = int(input("Number of simulations for Monte Carlo simulation: "))

print("\nPlease enter the parameters for the triangular distribution of WACC (Weighted Average Cost of Capital):")
print("Note: Please enter the WACC value as a decimal number. For example, if the WACC is 5%, enter 0.05.")
WACC_m = float(input("Minimum WACC value: "))
WACC_ml = float(input("Most likely WACC value: "))
WACC_M = float(input("Maximum WACC value: "))

print("\nPlease enter the parameters for the uniform distribution of initial investment (CF_0 - Initial Cash Flow):")
CF_0_m = float(input("Minimum CF_0 value: "))
CF_0_M = float(input("Maximum CF_0 value: "))

print("\nPlease enter if the cash flow will follow a fixed distribution over the project or will be adjusted annually:")
distribution_choice = input("Enter 'fixed' for a fixed distribution or 'adjusted' for annually adjusted distribution: ")

if distribution_choice.lower() == 'fixed':
    print("\nPlease enter the parameters for the triangular distribution of cash flow per period:")
    CF_m = float(input("Minimum cash flow per period value: "))
    CF_ml = float(input("Most likely cash flow per period value: "))
    CF_M = float(input("Maximum cash flow per period value: "))
    CF_distributions_m = [CF_m] * Planning_Horizon
    CF_distributions_ml = [CF_ml] * Planning_Horizon
    CF_distributions_M = [CF_M] * Planning_Horizon
else:
    CF_distributions_m = []
    CF_distributions_ml = []
    CF_distributions_M = []
    for period in range(Planning_Horizon):
        print(f"\nPlease enter the parameters for the triangular distribution of cash flow for period {period + 1}:")
        CF_m = float(input(f"Minimum cash flow value for period {period + 1}: "))
        CF_ml = float(input(f"Most likely cash flow value for period {period + 1}: "))
        CF_M = float(input(f"Maximum cash flow value for period {period + 1}: "))
        CF_distributions_m.append(CF_m)
        CF_distributions_ml.append(CF_ml)
        CF_distributions_M.append(CF_M)

print("\nPlease enter if residual value:")
RV = float(input("Residual value: "))

# Data for Numerical Integration Modeling
k = int(input("\nPlease enter the number of partitions used in numerical integration (suggested value: 100000): "))


########################################################################################################

###Input data (you can adjust for your situation)
###Uncomment the lines below to enable direct data entry into the script, if desired.
##Planning_Horizon = 10
##Number_of_simulations = 10000
###Weighted Average Cost of Capital (WACC) with a triangular probability distribution with the following parameters/values:
##WACC_m = 0.08
##WACC_ml = 0.1
##WACC_M = 0.14
### Initial investment (CF_0 – initial Cash Flow) follows a uniform distribution with the following parameters/values:
##CF_0_m = 2000000
##CF_0_M = 3000000
###Cash Flow per period follows a triangular distribution with the following parameters/values:
###If the bounds of the triangular distribution associated with the cash flow remain constant throughout the project horizon, please fill in the following data
###CF_m = 
###CF_ml = 
###CF_M = 
###CF_distributions_m = [CF_m] * Planning_Horizon
###CF_distributions_ml = [CF_ml] * Planning_Horizon
###CF_distributions_M = [CF_M] * Planning_Horizon
##
###If the bounds of the triangular distribution associated with the cash flow vary throughout the project horizon, please fill in the following data.
###Provide three lists of values associated with the triangular distribution of the cash flow.
###In the first list, include the lower bounds of the distribution.
###In the second list, include the most likely values.
###In the third list, include the upper bounds of the distribution.
##CF_distributions_m = [80000, 160000, 240000, 320000, 400000, 480000, 560000, 640000, 720000, 800000]    #Include the lower bounds of the distribution.
##CF_distributions_ml = [100000, 200000, 300000, 400000, 500000, 600000, 700000, 800000, 900000, 1000000] #Include the most likely values.
##CF_distributions_M = [120000, 240000, 360000, 480000, 600000, 720000, 840000, 960000, 1080000, 1200000] #Include the upper bounds of the distribution.
##    
###Residual value
##RV = 250000#float(input("Residual value: "))
##
### Data for Numerical Integration Modeling
##k = 100000 # Number of partitions used in numerical integration

###############################################################################


# Generating data, NPV, Monte Carlo Simulation 
NPV = [] # vector to store NPV generated information

for i in range (Number_of_simulations):
    year = 0
    CF_0 = np.random.uniform(CF_0_m, CF_0_M) 
    NPV_year = - CF_0
    #print(-CF_0)
    WACC_year = np.random.triangular(WACC_m, WACC_ml, WACC_M)
    for j in range (Planning_Horizon):
        year += 1 
        CF_year = np.random.triangular(CF_distributions_m[j], CF_distributions_ml[j], CF_distributions_M[j]) # draw the cash flow for each year
        #print("CF",j+1,":",CF_year)
        NPV_year += CF_year / ((1 + WACC_year) ** year)
        #print(NPV_year)
    NPV_year +=     RV / ((1 + WACC_year) ** Planning_Horizon)
    NPV.append(NPV_year)
    #print(NPV)

#####################################################################

# Statistics Descriptive

# Calculating the statistical measures
NPV_minimum = np.min(NPV)  # NPV minimum
NPV_maximum = np.max(NPV)  # NPV maximum
NPV_range = NPV_maximum - NPV_minimum  # Range of NPV values
NPV_mean = np.mean(NPV)  # Mean of NPV values
NPV_standard_deviation = np.std(NPV)  # Standard deviation of NPV values (S_NPV in paper)
NPV_median = np.median(NPV)  # Median of NPV values
NPV_Coefficient_of_variation = (NPV_standard_deviation/NPV_mean)*100



print("\nSTATISTICS DESCRIPTIVE")
print("Minimum:", NPV_minimum)
print("Maximum:", NPV_maximum)
print("Range:", NPV_range)
print("Mean:", NPV_mean)
print("Standard Deviation:", NPV_standard_deviation)
print("Coefficient of Variation:", NPV_Coefficient_of_variation)
print("Median:", NPV_median)


if NPV_mean - 6 * NPV_standard_deviation > 0:
    print("The probability of NPV being negative is low (zero). The rest of the program does not apply in this case.")
    sys.exit()

########################################################################

# Numerical Modeling of the Probability of Financial Deficit – P(NPV < 0)

Delta = (6 * NPV_standard_deviation - NPV_mean) / k  # Size of each subinterval

    # List to store the midpoints of the subintervals
Midpoints = []

    # Determine the midpoints of each subinterval
for i in range(k):
    Midpoint = (NPV_mean - 6 * NPV_standard_deviation) +((2*(i+1)-1)/2)*Delta 
    Midpoints.append(Midpoint)

    # function PDF
    
def calculate_pdf(x): 
    """
    Calculates the probability density function (PDF) at a given point x
    for a normal distribution with mean NPV_mean and standard deviation NPV_standard_deviation.
    """
    pdf_value = (1 / (NPV_standard_deviation * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - NPV_mean) / NPV_standard_deviation) ** 2)
    return pdf_value

    # Probability_of_Financial_Deficit

Probability_of_Financial_Deficit = 0 

for i in range(k): 
    Probability_of_Financial_Deficit += calculate_pdf(Midpoints[i])

Probability_of_Financial_Deficit = Delta*Probability_of_Financial_Deficit

##########################################################################

# Numerical Modeling of the Conditional Expected Loss – CEL

CEL_uper = 0  #

for i in range(k): 
    CEL_uper += Midpoints[i]*calculate_pdf(Midpoints[i])

CEL_uper = Delta*CEL_uper    

CEL = CEL_uper/Probability_of_Financial_Deficit    

#########################################################################

#Numerical Modeling of the P(NPV < CEL) and P(NPV < CEL | NPV < 0)


    # Calculate the size of each subinterval
Delta = (CEL - (NPV_mean - 6 * NPV_standard_deviation)) / k

    # List to store the midpoints of the subintervals
Midpoints = []

    # Determine the midpoints of each subinterval
for i in range(k):
    Midpoint = (NPV_mean - 6 * NPV_standard_deviation) + ((2*(i+1)-1)/2) * Delta 
    Midpoints.append(Midpoint)
    
Probability_NPV_less_CEL = 0 

for i in range(k): 
    Probability_NPV_less_CEL += calculate_pdf(Midpoints[i])

Probability_NPV_less_CEL = Delta*Probability_NPV_less_CEL



#########################################################################

#Numerical Modeling of the P(NPV < CEL | NPV < 0)

Probability_NPV_less_CEL_given_that_NPV_less_0 = Probability_NPV_less_CEL/Probability_of_Financial_Deficit

#########################################################################

#Numerical Modeling of the Conditional Value at Risk – CVaR

VaR_5 = NPV_mean - 1.645 * NPV_standard_deviation # precisaria alguma explicação para o 1.645

    # Calculate the size of each subinterval
Delta = (VaR_5 - (NPV_mean - 6 * NPV_standard_deviation)) / k

    # List to store the midpoints of the subintervals
Midpoints = []

    # Determine the midpoints of each subinterval
for i in range(k):
    Midpoint = (NPV_mean - 6 * NPV_standard_deviation) + ((2*(i+1)-1)/2) * Delta 
    Midpoints.append(Midpoint)

CVaR_below = 0

for i in range(k): 
    CVaR_below += calculate_pdf(Midpoints[i])

CVaR_below = Delta * CVaR_below

CVaR_uper = 0  

for i in range(k): 
    CVaR_uper += Midpoints[i]*calculate_pdf(Midpoints[i])

CVaR_uper = Delta*CVaR_uper    

CVaR_5 = CVaR_uper/CVaR_below     

# Other statistics inferential

VaR_deviation = NPV_mean - VaR_5

CVaR_deviation = NPV_mean - CVaR_5

CEL_deviation = NPV_mean - CEL

################################################################


# Inferential Statistics
print("\nSTATISTICS INFERENTIAL")
print("P(NPV < 0):", Probability_of_Financial_Deficit)
print("VaR5%:", VaR_5)
print("CVaR5%:", CVaR_5)
print("CEL:", CEL)
print("P(NPV < CEL):", Probability_NPV_less_CEL)
print("P(NPV < CEL | NPV < 0):", Probability_NPV_less_CEL_given_that_NPV_less_0)
print("VaR deviation:", VaR_deviation)
print("CVaR deviation:", CVaR_deviation)
print("CEL deviation:", CEL_deviation)

