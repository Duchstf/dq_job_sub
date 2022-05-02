#
echo $HOSTNAME

#Setup
source /work/submit/dhoang/DQ/e1039-core/DarkQuest/e1039-analysis/SimHits/setup_mye1039.sh

#Move to the directory
cd /work/submit/dhoang/DQ/e1039-core/DarkQuest/e1039-analysis/SimHits/macro/

#Run codes
root -b -q MACRO
