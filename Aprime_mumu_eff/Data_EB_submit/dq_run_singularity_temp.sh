#!/bin/bash 

cd /e1039-core/DarkQuest/e1039-analysis/SimHits/
source /tmp/$CONDOR_JOB_ID/setup_mye1039.sh
cd macro/

which root
ls -lth /tmp/$CONDOR_JOB_ID/

root -b -q MACRO