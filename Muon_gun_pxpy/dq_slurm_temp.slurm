#!/bin/bash
#SBATCH --job-name=run_test      # Job name
##SBATCH --mail-type=END,FAIL         # Mail events (NONE, BEGIN, END, FAIL, ALL)
##SBATCH --mail-user=email@ufl.edu    # Where to send mail 
#SBATCH --nodes=1                    # Run all processes on a single node	
#SBATCH --ntasks=1                   # Run a single task    
##SBATCH --cpus-per-task=4            # Number of CPU cores per task
##SBATCH --mem=1gb                    # Job memory request
#SBATCH --time=05:00:00              # Time limit hrs:min:sec
#SBATCH --array=0-10
#SBATCH --output=LOGDIR/PREFIX_%A_%a.log     # Standard output and error log
##SBATCH --nodelist=cvmfs-test-compute-0-7,cvmfs-test-compute-0-8,cvmfs-test-compute-0-9,cvmfs-test-compute-0-10
##SBATCH --exclusive

hostname

pwd

#Setup
source /work/submit/dhoang/DQ/e1039-core/DarkQuest/e1039-analysis/SimHits/setup_mye1039.sh

#Move to the directory
cd /work/submit/dhoang/DQ/e1039-core/DarkQuest/e1039-analysis/SimHits/macro/

sleep $(( $RANDOM % 60 ))

#Run codes
root -b -q MACRO
