#!/bin/bash
hostname
pwd
ls -lt

echo "Condor Job ClassAds"
cat $PWD/.job.ad

#Set up gfal-copy
source /cvmfs/grid.cern.ch/centos7-ui-4.0.3-1_umd4v4/etc/profile.d/setup-c7-ui-example.sh

gfal-copy gsiftp://se01.cmsaf.mit.edu:2811//mitgroups/DarkQuest/wmccorma/new-sif.sif .
echo "Using singularity image"

echo "Copying DST file"
gfal-copy gsiftp://se01.cmsaf.mit.edu:2811//mitgroups/DarkQuest/dhoang/CONFIG_DIR/CONFIG_FILE_DST.root .


#Might want to make a /tmp/job_jobid
mkdir /tmp/$CONDOR_JOB_ID

cp setup_mye1039.sh  /tmp/$CONDOR_JOB_ID
cp MACRO_NAME  /tmp/$CONDOR_JOB_ID/RunEmbeddingNOEMBED.C
cp CONFIG_FILE_DST.root /tmp/$CONDOR_JOB_ID
cp RUNSCRIPT_singularity.sh /tmp/$CONDOR_JOB_ID

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

singularity exec -B /cvmfs -B /usr -B /etc new-sif.sif bash /tmp/$CONDOR_JOB_ID/RUNSCRIPT_singularity.sh

echo 'I ran, now ls tmp'
ls -lth /tmp/$CONDOR_JOB_ID/
gfal-copy -f file:///tmp/$CONDOR_JOB_ID/output.root gsiftp://se01.cmsaf.mit.edu:2811//mitgroups/DarkQuest/dhoang/OUT_DIR_NAME/OUTFILE.root

rm CONFIG_FILE_DST.root
rm new-sif.sif
rm -rf  /tmp/$CONDOR_JOB_ID