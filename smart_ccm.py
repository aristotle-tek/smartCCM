# smart_CCM.py
# Andrew Peterson
# Exploratory analysis to understand concretely contract dynamics.
# (For an algebraic approach, see instead the accompanying paper.)

import pandas as pd
import numpy as np
import argparse

parser = argparse.ArgumentParser(description="smart CCM explorer")
parser.add_argument('-dur', dest='contract_years', type=float, default=5, required=False, help="Enter the duration of the contract in years")
parser.add_argument('-costy0', dest='cost_mit_y0', type=float, default=20, required=False, help="Enter the cost of mititgation at year=0")
parser.add_argument('-scc1', dest='scc_theta1', type=float, default=171.0, required=False, help="Enter the social cost of carbon for theta1 (high), believed by P1")
parser.add_argument('-scc0', dest='scc_theta0', type=float, default=56.0, required=False, help="Enter the social cost of carbon for theta0 (low), believed by P2")
parser.add_argument('-initcost', dest='initial_cost', type=float, default=1000.0, required=False, help="The initial investment cost e.g. 1000")
parser.add_argument('-return', dest='return_req', type=float, default=0.08, required=False, help="Enter return on investment required as .08 for 8 percent")
args = parser.parse_args()



contract_duration = args.contract_years

cost_of_mitigation_year0 = args.cost_mit_y0 #20.0 #  $ per ton of carbon emissions reductions - randomly chosen from between $1 and $50.
social_cost_carbon_theta1 = args.scc_theta1 #171.0 # from Brookings
social_cost_carbon_theta0 = args.scc_theta0 #56.0 # from Brookings
initial_cost_mitigation = args.initial_cost #1000.0
yearly_return_expected = args.return_req


assert contract_duration >0
assert cost_of_mitigation_year0 >0
assert social_cost_carbon_theta1 >0
assert social_cost_carbon_theta0 >0
assert initial_cost_mitigation >0
assert 0 <= yearly_return_expected <= 1


print("\nInput assumptions: (enter arguments to change these):\n(1) Participants expect a yearly return of %d percent." % (yearly_return_expected*100))  

print("(2) The cost of mitigation in year 0 of $%d/ton and a contract duration of %d years.\n" % ( cost_of_mitigation_year0, contract_duration ))  

tons_mitigated = initial_cost_mitigation/cost_of_mitigation_year0

print("P1 makes an investment of $%d to offset %.1f tons of carbon.\n" % ( initial_cost_mitigation, tons_mitigated ))  


#x_star = # amount p1 pays to engage contract.

expected_val_if_theta1 = tons_mitigated * social_cost_carbon_theta1 # aka 'v_final'
expected_val_if_theta0 = tons_mitigated * social_cost_carbon_theta0


print("If P1 is right, (theta=1) the social cost of carbon at expiration is $%.2f,\nand the final value of the contract is $%.2f\n" % (social_cost_carbon_theta1, expected_val_if_theta1 ))  
print("If P0 is right, (theta=0), the social cost of carbon at expiration is $%.2f,\nand the final value of the contract is $%.2f\n" % (social_cost_carbon_theta0, expected_val_if_theta0 ))  



# kappa - insurance cost, assume for now this is payed by p1, though could equally have it paid by p2 or split.

# Condition: p1 participates if expected_val_if_theta1 > initial_cost_mitigation + x_star * (1 + yearly_return)^contract_duration + kappa

investment_return_factor = (1 + yearly_return_expected)**contract_duration 


p1_max_xstar = (expected_val_if_theta1 - (initial_cost_mitigation *investment_return_factor) ) / investment_return_factor
p2_min_xstar = expected_val_if_theta0 / investment_return_factor


#--- When will p2 participate in contract? --- 
# want their income from their initial payment of x_star to be
# greater than the final contract payment under their assumption that theta=0:
# i.e. xstar * investment_return_factor > expected_val_if_theta0



if p1_max_xstar<0:
	print("\n **** Sorry! Contract not possible!  ****** ")
	print("P1 would only enter a contract if they were paid $%.2f to do so (by some unknown 3rd party).\n" % ( -p1_max_xstar )) 
else:
	print("\nIgnoring the cost of insurance ('kappa'), P1 will accept the the contract if the value of x* (to enter the contract) is no more than $%.2f\n" % ( p1_max_xstar ))  

	if p2_min_xstar > p1_max_xstar:
		print("\n **** Sorry! Contract not possible!  ****** ")
		print("P2 would have to be paid $%.2f to enter into a contract,\nbut P1 is only willing to pay $%.2f \n" % ( p2_min_xstar, p1_max_xstar )) 
	else:
		print("P2 will accept the the contract if the value of x_star\n (to enter the contract) is at least $%.2f\n" % ( p2_min_xstar ))  

		print("So they can agree on a contract with xstar betweeen $%.2f and $%.2f" % ( p2_min_xstar, p1_max_xstar ))  
		print("(or, assuming there is some cost to pay for insurance against P2 defaulting,\nthis insurance has to cost less than $%.2f.\n\n" % (p1_max_xstar- p2_min_xstar ))






