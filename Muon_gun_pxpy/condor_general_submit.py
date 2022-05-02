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
    python3 general_submit.py
    """

    #Output files
    tag = "Muon_gun_pxy_eflagoff_extraoff" ####### FIRST PARAMETER
    tag += "_{}".format(now.strftime("%d_%m_%Y"))#Specify date and time

    #Output files
    out_dir = "/work/submit/dhoang/DQ/outfiles/{}/".format(tag)
    log_dir = "logs_{}".format(tag)
    os.system('mkdir -p  %s' %out_dir)

    ####### MACRO command to run
    macro_command = "'RecoE1039Sim.C(10000, 3, true, true, false, true, {}, {})'"\
                    .format('"{}"'.format("Brem_1.650000_z500_600_eps_-4"), #Aprime configs, can ignore if using guns
                            '"{}"'.format(out_dir + "Mu_gun_{}.root".format(round(scan_para)))) #output file path
    
    current_path =  os.environ['PWD']
    
    #Local logs if it's not there already
    os.system('mkdir -p  %s' %log_dir)

    
    #Produce the condor file
    condor_templ_file = open("{}/dq_condor_temp_FOR_DUC.sub".format(current_path)) #Template
    local_condor = "{}/{}/Mu_gun_{}.sub".format(current_path, log_dir, round(scan_para))

    print("Creating condor file ..")
    condor_file = open(local_condor,"w")
    for line in condor_templ_file:
        line=line.replace('LOGDIR', "{}/{}".format(current_path, log_dir))
        line=line.replace('PREFIX', "Mu_gun_{}".format(round(scan_para)))
        condor_file.write(line)
    
    #Restrict the jobs to only good machines
    condor_file.write("\n")
    if len(GOODMACHINES) > 0:
        requirements_line = "("
        first = True
        for machine in GOODMACHINES:
            if first:
                first = False
            else:
                requirements_line += " || {}".format("\\")
                requirements_line += "\n"
                requirements_line += "                " #Just for formatting
            requirements_line += "(Machine == \"%s\")" % machine
        requirements_line += ")"
        condor_file.write("requirements = %s\n\n" % requirements_line)
    
    condor_file.write("\n")
    condor_file.write("queue")

    condor_file.close()

    #Produce executable
    sh_templ_file = open("{}/exec_temp.sh".format(current_path))
    local_sh = "{}/{}/Mu_gun_{}.sh".format(current_path, log_dir, round(scan_para))

    print("Creating executable ..")
    sh_file = open(local_sh, "w")
    for line in sh_templ_file:
        line=line.replace('MACRO', macro_command)
        sh_file.write(line)
    sh_file.close()

    os.system('chmod u+x {}'.format(local_sh))
    
    #os.system('condor_submit {}'.format(local_condor))

    condor_templ_file.close()
    sh_templ_file.close()

def main():
    
    #Submit 100 jobs with 1k events each
    for i in range(10):
        #Submit job with this position
        submit_job(i)
        
if __name__ == "__main__":
    main()