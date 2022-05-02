import os, sys
import subprocess
from datetime import datetime
now = datetime.now()

GOODMACHINES = []

def submit_job(scan_para):
    """
    This file is used to just submit small general sample.
    You can just specify the macro command and the job iwll be submitted.

    Arguments (specify in-file because I'm lazy):
        - The RecoE1039Sim.C macro command with all of its arguments
    
    Example:
    python3 slurm_general_submit.py
    """

    #Output files
    tag = "Muon_gun_pxy_eflagoff_extraoff_OLD" ####### FIRST PARAMETER
    tag += "_{}".format(now.strftime("%d_%m_%Y"))#Specify date and time

    #Output files
    out_dir = "/work/submit/dhoang/DQ/outfiles/{}/".format(tag)
    log_dir = "logs_{}".format(tag)
    os.system('mkdir -p  %s' %out_dir)

    ####### MACRO command to run
    macro_command = "'RecoE1039Sim.C(10000, 3, true, true, false, true, {}, {})'"\
                    .format('"{}"'.format("Brem_1.650000_z500_600_eps_-4"), #Aprime configs, can ignore if using guns
                            '"{}"'.format(out_dir + "Mu_gun_{}_${{SLURM_JOB_ID}}_${{SLURM_PROCID}}.root".format(round(scan_para)))) #output file path
    
    current_path =  os.environ['PWD']
    
    #Local logs if it's not there already
    os.system('mkdir -p  %s' %log_dir)

    
    #Produce the slurm file
    slurm_templ_file = open("{}/dq_slurm_temp.slurm".format(current_path)) #Template
    local_slurm = "{}/{}/Mu_gun_{}.slurm".format(current_path, log_dir, round(scan_para))

    print("Creating slurm file ..")
    slurm_file = open(local_slurm,"w")
    for line in slurm_templ_file:
        line=line.replace('LOGDIR', "{}/{}".format(current_path, log_dir))
        line=line.replace('PREFIX', "Mu_gun_{}".format(round(scan_para)))
        line=line.replace('MACRO', macro_command)
        slurm_file.write(line)
    slurm_file.close()

    print(local_slurm)
    os.system('sbatch {}'.format(local_slurm))

    slurm_templ_file.close()
    

def main():
    
    #Submit 100 jobs with 1k events each
    for i in range(1):
        #Submit job with this position
        submit_job(i)
        
if __name__ == "__main__":
    main()