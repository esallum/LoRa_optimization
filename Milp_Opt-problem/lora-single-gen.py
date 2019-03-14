# generates LP algebraic representation for CPLEX
import sys
from ntw_defs import * # defines some network-related parameters such as available CFs, SF, average tx rate,...

DFT_N = 10

# number of nodes can be passed as argument
if len(sys.argv) > 1:
	try:
		N=int(sys.argv[1])
	except ValueError:
		N=DFT_N
else:
	N=DFT_N

print("Number of Nodes: {0}".format(N), file=sys.stderr)

# nodes in the network {1..N}
NODES=range(1, N+1);

# initialize a dictionary that will contain all Z variables created (Z_i,cf,sf = CF_i,cf * SF_i,sf)
# Z is a substitution performed to linearize the multiplication of two binary variables: CF_i,cf * SF_i,sf
Z = dict()

# initialize a set for all CF and SF variables 
# (some might not be used; this is an easy way to have a list of all used for the integrality constraints)
CF_SF = set();

# create list of Z_{i,cf,sf}
# \sum_{cf=CF1,CF2,...}
for cf in CF:
	# \sum_{sf=SF1,SF2,...}	
	for sf in SF:
		# Z_{i,cf,sf} 
		for n in NODES: 
			Z_icfsf = "Z_{0}#{1}#{2}".format(n, cf, sf)
			Z[Z_icfsf] = {'i': n, 'cf': "CF_{0}#{1}".format(n, cf), 'sf':"SF_{0}#{1}".format(n, sf)}

# objective function
print("min\nobj: MU")

# constraints
print("\nst")

# print("\nU ")
# for Z_icfsf, i_cf_sf in Z.items():
# 	q= -1  T_SF[sf]  L
# 	if (q>0): 
# 		print("+ ", end='')	
# 	print("{0:.8f} {1} ".format(q, Z_icfsf), end='')
# print("= 0\n")

# \sum_{n \in \{1..N\}}  \sum_{cf=\{G\}} \sum_{sf=\{SF1,SF2,...\}} ( CF_{i,cf} . SF_{i,sf} . T_{SF} * \Lambda ) \leq 0.01		
for cf in CF:
	for sf in SF:
		print("\nMU - ")
		for n in NODES:
			if (n > 1):
				print(" - ", end='') 
			# CF_{i,cf} . SF_{i,sf} . T_{SF} * \Lambda
			print("{0:.8f} {1}".format(T_SF[sf]*L, "Z_{0}#{1}#{2}".format(n, cf, sf)), end='')
		print(" >= 0\n")

# all nodes are assigned exactly one CF
# \forall n \in \{1..N\} \sum_{cf=CF1,CF2,...} CF_{n,cf} = 1
for n in NODES:
	for cf in CF:
		if (cf != CF[0]):
			print("+", end='')		
		print("CF_{0}#{1}".format(n, cf), end='')
		CF_SF.add("CF_{0}#{1}".format(n, cf));
	print(" = 1\n")

# all nodes are assigned exactly one SF
# \forall n \in \{1..N\} \sum_{sf=SF1,SF2,...} SF_{n,sf} = 1
for n in NODES:
	for sf in SF:
		if (sf != SF[0]):
			print("+", end=''),		
		print("SF_{0}#{1}".format(n, sf), end='')
		CF_SF.add("SF_{0}#{1}".format(n, cf));
	print(" = 1\n")

# # g <= 0.01
# # \sum_{n \in \{1..N\}}  \sum_{cf=\{G\}} \sum_{sf=\{SF1,SF2,...\}} ( CF_{i,cf} . SF_{i,sf} . T_{SF} * \Lambda ) \leq 0.01
# for n in NODES:
# 	if (n > 1):
# 		print(" + ", end='')
# 	for cf in G:
# 		if (cf != G[0]):
# 			print(" + ", end='')
# 		for sf in SF:
# 			if (sf != SF[0]):
# 				print(" + ", end='')
# 			# CF_{i,cf} . SF_{i,sf} . T_{SF} * \Lambda
# 			print("{0:.8f} {1}".format(T_SF[sf]*L, "Z_{0}#{1}#{2}".format(n, cf, sf)), end='')
# print(" <= 0.01\n")

# # g1 <= 0.01
# # \sum_{n \in \{1..N\}}  \sum_{cf=\{G1\}} \sum_{sf=\{SF1,SF2,...\}} ( CF_{i,cf} . SF_{i,sf} . T_{SF} * \Lambda ) \leq 0.01
# for n in NODES:
# 	if (n > 1):
# 		print(" + ", end='')
# 	for cf in G1:
# 		if (cf != G1[0]):
# 			print(" + ", end='')
# 		for sf in SF:
# 			if (sf != SF[0]):
# 				print(" + ", end='')
# 			# CF_{i,cf} . SF_{i,sf} . T_{SF} * \Lambda
# 			print("{0:.8f} {1}".format(T_SF[sf]*L, "Z_{0}#{1}#{2}".format(n, cf, sf)), end='')
# print(" <= 0.01\n")

# # g2 <= 0.1
# # \sum_{n \in \{1..N\}}  \sum_{cf=\{G2\}} \sum_{sf=\{SF1,SF2,...\}} ( CF_{i,cf} . SF_{i,sf} . T_{SF} * \Lambda ) \leq 0.01
# for n in NODES:
# 	if (n > 1):
# 		print(" + ", end='')
# 	for cf in G2:
# 		if (cf != G2[0]):
# 			print(" + ", end='')
# 		for sf in SF:
# 			if (sf != SF[0]):
# 				print(" + ", end='')
# 			# CF_{i,cf} . SF_{i,sf} . T_{SF} * \Lambda
# 			print("{0:.8f} {1}".format(T_SF[sf]*L, "Z_{0}#{1}#{2}".format(n, cf, sf)), end='')
# print(" <= 0.1\n")

# Each Z_i,cf,sf requires the following contraints:
# Z_i,cf,sf <= CF_i,cf 
# Z_i,cf,sf <= SF_i,sf 
# Z_i,cf,sf >= CF_i,cf  + SF_i,sf + 1
for Z_icfsf, value in Z.items():
	print("{0} - {1} <= 0  \n{0} - {2} <= 0 \n{0} - {1} - {2} >= -1".format(Z_icfsf, Z[Z_icfsf]['cf'], Z[Z_icfsf]['sf'] ) )

# bounds and integrality constraints
#print("\nbounds")

print("\nbinaries")
# CF_i,cf and SF_i,sf are binary
for n in NODES:
	for cf in CF:	
		print("CF_{0}#{1}".format(n, cf))
	for sf in SF:	
		print("SF_{0}#{1}".format(n, sf))

# Z_i,cf,sf are binary
for var_Z, value in Z.items():
	print("{0}".format(var_Z))

print("\nend")