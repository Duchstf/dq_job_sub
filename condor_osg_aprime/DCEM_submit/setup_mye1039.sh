export MY_E1039=/core-inst/this-e1039.sh
export DIR_TOP=$(dirname $(readlink -f $BASH_SOURCE))
echo $MY_E1039
echo $DIR_TOP
source $MY_E1039
export LD_LIBRARY_PATH=/e1039-core/DarkQuest/e1039-analysis/SimHits/install/lib/:$LD_LIBRARY_PATH
export LD_LIBRARY_PATH=/tmp/$CONDOR_JOB_ID/lib64/:$LD_LIBRARY_PATH
export DIR_CMANTILL=/e1039-core/DarkQuest/e1039-analysis/SimHits
