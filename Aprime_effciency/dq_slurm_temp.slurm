#!/bin/bash
#SBATCH --job-name=dq_job      # Job name
##SBATCH --mail-type=END,FAIL         # Mail events (NONE, BEGIN, END, FAIL, ALL)
##SBATCH --mail-user=email@ufl.edu    # Where to send mail 
#SBATCH --nodes=1                    # Run all processes on a single node	
#SBATCH --ntasks=1                   # Run a single task    
##SBATCH --cpus-per-task=4            # Number of CPU cores per task
##SBATCH --mem=1gb                    # Job memory request
##SBATCH --time=30:00:00              # Time limit hrs:min:sec
##SBATCH --array=0-1
#SBATCH --output=LOGDIR/PREFIX_%j.log     # Standard output and error log
#SBATCH --error=LOGDIR/PREFIX_err_%j.txt

##SBATCH --nodelist=cvmfs-test-compute-0-7,cvmfs-test-compute-0-8,cvmfs-test-compute-0-9,cvmfs-test-compute-0-10
##SBATCH --exclusive

hostname
pwd

#Set up the certificate
# if you need cvmfs or a given architecture
export X509_USER_PROXY=~/x509up_u207327

#gfal setup
source /cvmfs/grid.cern.ch/centos7-ui-test/etc/profile.d/setup-c7-ui-example.sh

#DarkQuest software setup
source /work/submit/dhoang/DQ/e1039-core/DarkQuest/e1039-analysis/SimHits/setup_mye1039.sh

#Move to the directory
cd /work/submit/dhoang/DQ/e1039-core/DarkQuest/e1039-analysis/SimHits/macro/

#Make output directory
mkdir OUTFILE

sleep $(( $RANDOM % 60 ))

#Run codes
root -b -q MACRO

# copy the file over
gfal-copy file://`pwd`/OUTFILE/OUTFILE.root gsiftp://se01.cmsaf.mit.edu:2811//mitgroups/DarkQuest/dhoang/OUT_DIR_NAME/OUTFILE.root


# echo "I am here!"
# pwd
# #List all the files in the current directory
# for entry in "${PWD}"/*
# do
#   echo "$entry"
# done

#Remove the output directory
rm -rf OUTFILE/

#Remove the log file & output file
#rm /tmp/PREFIX_%A.log
