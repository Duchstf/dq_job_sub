#!/bin/bash
hostname

echo "proxy id"
voms-proxy-info - all 
pwd
ls -lt

echo "Condor Job ClassAds"
cat $PWD/.job.ad

#Set up gfal-copy
source /cvmfs/grid.cern.ch/centos7-ui-4.0.3-1_umd4v4/etc/profile.d/setup-c7-ui-example.sh

echo "Copying singularity image"
gfal-copy gsiftp://se01.cmsaf.mit.edu:2811//mitgroups/DarkQuest/wmccorma/new-sif.sif .

echo "Copying Signal DST file"
gfal-copy gsiftp://se01.cmsaf.mit.edu:2811//mitgroups/DarkQuest/dhoang/Aprime_Muons_Scan_z200_600_18_04_2022/Brem_0.250000_z200_600_eps_-4.4_DST.root .

echo "Copying Data DST file"
gfal-copy gsiftp://se01.cmsaf.mit.edu:2811//mitgroups/DarkQuest/0053/embedding_data.root .


#Might want to make a /tmp/job_jobid
mkdir /tmp/$CONDOR_JOB_ID

cp setup_mye1039.sh  /tmp/$CONDOR_JOB_ID
cp RunEmbedding_AprimeMumu_Template.C  /tmp/$CONDOR_JOB_ID/RunEmbedding.C
cp Brem_0.250000_z200_600_eps_-4.4_DST.root /tmp/$CONDOR_JOB_ID
cp Brem_0.250000_z200_600_eps_-4.4_singularity.sh /tmp/$CONDOR_JOB_ID
cp embedding_data.root /tmp/$CONDOR_JOB_ID

mkdir /tmp/$CONDOR_JOB_ID/lib64
cp libgsl.so.0 /tmp/$CONDOR_JOB_ID/lib64/
cp libsatlas.so.3 /tmp/$CONDOR_JOB_ID/lib64/
cp libicuuc.so.50 /tmp/$CONDOR_JOB_ID/lib64/

# Don’t have to do this if use job id
# rm /tmp/output.root
# rm /tmp/output_DST.root
# rm /tmp/eval.root

echo "Check before singularity"
ls -lt

singularity exec -B /cvmfs -B /usr -B /etc new-sif.sif bash /tmp/$CONDOR_JOB_ID/Brem_0.250000_z200_600_eps_-4.4_singularity.sh

echo 'I ran, now ls tmp'
ls -lth /tmp/$CONDOR_JOB_ID/
gfal-copy -f file:///tmp/$CONDOR_JOB_ID/output.root gsiftp://se01.cmsaf.mit.edu:2811//mitgroups/DarkQuest/dhoang/Data_EB_Aprime_Muons_Scan_z200_600_17_05_2022/Brem_0.250000_z200_600_eps_-4.4.root

rm Brem_0.250000_z200_600_eps_-4.4_DST.root
rm new-sif.sif
rm -rf  /tmp/$CONDOR_JOB_ID