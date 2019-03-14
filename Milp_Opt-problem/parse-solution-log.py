# parse solution
import sys
import math
from ntw_defs import * # defines some network-related parameters such as available CFs, SF, average tx rate,...

# number of nodes can be passed as argument
if len(sys.argv[1]) > 0: 
	SOLUTION_FN=sys.argv[1]
else:
	print("Please povide the solution log file as argument.")
	exit()

# dictionary to store the cf and sf for each node 
nodes = dict()

# compute n_cfsf (number of nodes in a given {cf,sf}) 
def n_cfsf( cf, sf ):
	n = 0
	for node, cf_sf in nodes.items():
		if (cf_sf['cf'] == cf and cf_sf['sf'] == sf):
			n = n + 1
	return n;

# compute u_cf (utilization of a given cf) 
def u_cf(cf):
	u = 0
	for node, cf_sf in nodes.items():
		if (cf_sf['cf'] == cf):
			u = u + T_SF[cf_sf['sf']] * L
	return u;

sol_lines=False
for line in open(SOLUTION_FN, 'r'):
	if line.startswith('CPLEX> Incumbent solution'): 
		sol_lines = True # found where the solution starts
	if sol_lines:
		if line.startswith( 'CF_' ):
			# line in the form CF_<node>#CF<cf num>
			n_and_cf = line[3:30].split('#') # get an array where the first element is the node and the second is the CF<cf num> string
			cf = "CF{0}".format(int(n_and_cf[1][2:])) # this removes extra spaces in the string
			if (nodes.get(n_and_cf[0]) == None):
				nodes[n_and_cf[0]] = {'cf' : cf}
			else:
				nodes[n_and_cf[0]].update({'cf' : cf})
		if line.startswith( 'SF_' ):
			# line in the form SF_<node>#<SF>
			n_and_sf = line[3:30].split('#') # get an array where the first element is the node and the second is the SF<cf num> string
			sf = "SF{0}".format(int(n_and_sf[1][2:])) # this removes extra spaces in the string
			if (nodes.get(n_and_sf[0]) == None):
				nodes[n_and_sf[0]] = {'sf' : sf}
			else:
				nodes[n_and_sf[0]].update({'sf' : sf})

# assign fixed value for debug
#nodes = {'3': {'cf': 'CF2', 'sf': 'SF7'}, '2': {'cf': 'CF1', 'sf': 'SF7'}, '1': {'cf': 'CF3', 'sf': 'SF7'}}
#nodes={'9': {'cf': 'CF1', 'sf': 'SF7'}, '6': {'cf': 'CF2', 'sf': 'SF7'}, '5': {'cf': 'CF3', 'sf': 'SF7'}, '1': {'cf': 'CF4', 'sf': 'SF7'}, '2': {'cf': 'CF5', 'sf': 'SF7'}, '8': {'cf': 'CF6', 'sf': 'SF7'}, '7': {'cf': 'CF7', 'sf': 'SF7'}, '3': {'cf': 'CF8', 'sf': 'SF7'}, '10': {'cf': 'CF9', 'sf': 'SF7'}, '4': {'cf': 'CF1', 'sf': 'SF7'}}

# print node settings
print("\n**Nodes")
print("\t{0}".format(nodes))
for n, cf_sf in nodes.items():
	print("\t N{0:4d}: {1}, {2}".format(int(n), cf_sf['cf'], cf_sf['sf']))

# compute success probability function
print("\n**Success Probability", end='')
p=0
u=0
for cf in CF:
	# \sum_{sf=SF1,SF2,...}	
	for sf in SF:
		# -2 . N_{cf,sf} * T_{SF} * \Lambda 
		u_node =  n_cfsf( cf, sf ) * T_SF[sf] * L
		p = p + -2 * u_node
		u = u + u_node

print(": {0:.6f} % (e^{1:.6f})".format(math.exp(p)*100, p))

# total utilization 
print("\n**Utilization: {0:.6f} %".format(u*100)) 

# utilization per cf
print("\n**Utilization per CF (only u > 0)")
for cf in CF:
	u = u_cf(cf)
	if u > 0:
		print("\t{0}: {1:.6f} %".format(cf, u_cf(cf)*100))

# utilization per {cf, sf}
print("\n**Utilization per {CF, SF} (only u > 0)")
for cf in CF:
	for sf in SF:
		u = n_cfsf( cf, sf ) * T_SF[sf] * L * 100
		if u > 0:
			print("\t{0}, {1}\t: {2:.6f} %".format(cf, sf, u))

print()
