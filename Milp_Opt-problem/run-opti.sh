#!/bin/sh
#executes the optimization problem; first argument of the script is the number of nodes (if not passed default value in lora-single-gen.py will be used)
LP_FILENAME="problem.lp"
SOL_FILENAME="solution.log"
echo "Running..."
python3 lora-single-gen.py $1 > $LP_FILENAME 
#cplex -c "read $LP_FILENAME" "set mip limits solutions 1" "optimize" "display solution variables -" > $SOL_FILENAME
cplex -c "read $LP_FILENAME" "set workmem 45000" "optimize" "display solution variables -" > $SOL_FILENAME
rm clone*log
python3 parse-solution-log.py $SOL_FILENAME 
cp $SOL_FILENAME solution$1.log
