import os, sys
import subprocess
from datetime import datetime
now = datetime.now()

GOODMACHINES = []

def submit_job(config_file, config_dir):
    """
    This file is used to just submit small general sample.
    You can just specify the macro command and the job iwll be submitted.

    Arguments (specify in-file because I'm lazy):
        - The RecoE1039Sim.C macro command with all of its arguments
    
    Example:
    python3 general_submit.py
    """

    #Output files
    tag = "Aprime_Muons_Scan" ####### FIRST PARAMETER
    tag += "_{}".format(now.strftime("%d_%m_%Y"))#Specify date and time

    #Output files
    log_dir = "logs_{}".format(tag)
    #out_dir = "/work/submit/dhoang/DQ/outfiles/{}/".format(tag)
    #os.system('mkdir -p  %s' %out_dir)
    #os.system("gfal-mkdir -p gsiftp://se01.cmsaf.mit.edu:2811//mitgroups/DarkQuest/dhoang/{}".format(tag))

    ####### MACRO command to run
    macro_command = "'RecoE1039Sim.C(10000, 1, 0, -300, true, true, false, {}, {}, {}, {})'"\
                    .format('"{}"'.format(config_file),
                            '"{}"'.format(config_dir),
                            '"{}"'.format(config_file + ".root"),#Aprime configs, can ignore if using guns
                            '"{}"'.format("{}/".format(config_file))) #output file path
    
    current_path =  os.environ['PWD']
    
    #Local logs if it's not there already
    os.system('mkdir -p  %s' %log_dir)

    
    #Produce the slurm file
    slurm_templ_file = open("{}/dq_slurm_temp.slurm".format(current_path)) #Template
    local_slurm = "{}/{}/Mu_gun_{}.slurm".format(current_path, log_dir, config_file)

    print("Creating slurm file ..")
    slurm_file = open(local_slurm,"w")
    for line in slurm_templ_file:
        line=line.replace('LOGDIR', "{}/{}".format(current_path, log_dir))
        line=line.replace('PREFIX', config_file)
        line=line.replace('MACRO', macro_command)
        line=line.replace('OUT_DIR_NAME', tag)
        line=line.replace('OUTFILE', config_file)
        #line=line.replace('OUTDIR', out_dir)
        slurm_file.write(line)
    slurm_file.close()

    #print(local_slurm)
    #os.system('sbatch --output=/dev/null --error=/dev/null {}'.format(local_slurm))
    #os.system('sbatch {}'.format(local_slurm))

    slurm_templ_file.close()
    

def main():
    
    config_dir = "/mnt/T2_US_MIT/hadoop/mitgroups/DarkQuest/APrime_Configs/displaced_Aprime_Muons_z500-600/"

    #test_count = 0
    #Loop through the files
    for filename in os.listdir(config_dir):
        if filename.startswith("Brem"):
            config_file = filename[:-4]
            print("Processing config ... :", config_file)
            submit_job(config_file, config_dir)
            
            #test_count += 1
        
        #Break the loop after a certain file
        # if test_count == 2: 
        #     break
        
if __name__ == "__main__":
    main()