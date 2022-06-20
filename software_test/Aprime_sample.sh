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
#SBATCH --output=/work/submit/dhoang/DQ/dq_job_sub/Aprime_effciency/logs_Aprime_Muons_Scan_20_06_2022/Brem_1.550000_z500_600_eps_-4.4_%j.log     # Standard output and error log
#SBATCH --error=/work/submit/dhoang/DQ/dq_job_sub/Aprime_effciency/logs_Aprime_Muons_Scan_20_06_2022/Brem_1.550000_z500_600_eps_-4.4_err_%j.txt

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
mkdir Brem_1.550000_z500_600_eps_-4.4

sleep $(( $RANDOM % 60 ))

#Run codes
root -b -q 'RecoE1039Sim.C(1000, 1, 0, -300, true, true, false, "Brem_1.550000_z500_600_eps_-4.4", "/mnt/T2_US_MIT/hadoop/mitgroups/DarkQuest/APrime_Configs/displaced_Aprime_Muons_z500-600/", "Brem_1.550000_z500_600_eps_-4.4.root", "Brem_1.550000_z500_600_eps_-4.4/")'

# copy the file over
gfal-copy file://`pwd`/Brem_1.550000_z500_600_eps_-4.4/Brem_1.550000_z500_600_eps_-4.4.root gsiftp://se01.cmsaf.mit.edu:2811//mitgroups/DarkQuest/dhoang/Aprime_Muons_Scan_20_06_2022/Brem_1.550000_z500_600_eps_-4.4.root


# echo "I am here!"
# pwd
# #List all the files in the current directory
# for entry in "${PWD}"/*
# do
#   echo "$entry"
# done

#Remove the output directory
#rm -rf Brem_1.550000_z500_600_eps_-4.4/

#Remove the log file & output file
#rm /tmp/Brem_1.550000_z500_600_eps_-4.4_%A.log
