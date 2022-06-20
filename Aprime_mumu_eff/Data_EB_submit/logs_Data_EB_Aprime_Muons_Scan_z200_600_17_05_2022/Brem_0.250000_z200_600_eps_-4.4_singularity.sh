#!/bin/bash 

cd /e1039-core/DarkQuest/e1039-analysis/SimHits/
source /tmp/$CONDOR_JOB_ID/setup_mye1039.sh
cd macro/

which root
ls -lth /tmp/$CONDOR_JOB_ID/

root -b -q '/tmp/$CONDOR_JOB_ID/RunEmbedding.C("/tmp/$CONDOR_JOB_ID/Brem_0.250000_z200_600_eps_-4.4_DST.root","output.root","/tmp/$CONDOR_JOB_ID/","/tmp/$CONDOR_JOB_ID/embedding_data.root",10)'