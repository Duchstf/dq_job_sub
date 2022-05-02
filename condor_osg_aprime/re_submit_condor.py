import os, sys
import subprocess


def submit_job(config_file, config_dir):
    """
    This file is used to just submit small general sample.
    You can just specify the macro command and the job will be submitted.

    Arguments (specify in-file because I'm lazy):
        - The RecoE1039Sim.C macro command with all of its arguments
    
    Example:
    python3 general_submit.py
    """

    #Ignore /mnt/T2_US_MIT/hadoop/mitgroups/DarkQuest/ in config_dir
    config_dir = config_dir[42:-1]

    #Output files
    tag = "Aprime_Electrons_Scan" ####### FIRST PARAMETER
    tag += "_{}".format(now.strftime("%d_%m_%Y"))#Specify date and time

    macro_path = "/work/submit/dhoang/DQ/e1039-core/DarkQuest/e1039-analysis/SimHits/macro/RecoE1039Sim.C"

    #Output files
    log_dir = "logs_{}".format(tag)

    #Copy setup file into log dir
    os.system('cp setup_mye1039.sh %s/' %log_dir)

    ####### MACRO command to run
    macro_command = "'/tmp/$CONDOR_JOB_ID/RecoE1039Sim.C(10000, 2, 0, -300, true, true, false, {}, {}, {}, {})'"\
                    .format('"{}"'.format(config_file),
                            '"{}"'.format("/tmp/$CONDOR_JOB_ID/"),
                            '"{}"'.format("output.root"),#Aprime configs, can ignore if using guns
                            '"{}"'.format("/tmp/$CONDOR_JOB_ID/")) #output file path
    
    current_path =  os.environ['PWD']
    
    #Local logs if it's not there already
    os.system('mkdir -p  %s' %log_dir)

    #1. Produce command to run wihtin the singularity image
    singularity_templ_file = open("{}/dq_run_singularity_temp.sh".format(current_path)) #Template
    local_singularity_run = "{}/{}/{}_singularity.sh".format(current_path, log_dir, config_file)

    print("Creating singularity file ..")
    singularity_file = open(local_singularity_run,"w")
    for line in singularity_templ_file:
        line=line.replace('MACRO', macro_command)
        singularity_file.write(line)
    singularity_file.close()
    
    #2. Produce the condor file
    condor_templ_file = open("{}/dq_condor_temp.sub".format(current_path)) #Template
    local_condor = "{}/{}/{}.sub".format(current_path, log_dir, config_file)

    print("Creating condor file ..")
    condor_file = open(local_condor,"w")
    for line in condor_templ_file:
        line=line.replace('LOGDIR', "{}/{}".format(current_path, log_dir))
        line=line.replace('PREFIX', config_file)
        line=line.replace('MACRO_PATH', macro_path)
        line=line.replace('RUNSCRIPT', config_file)
        condor_file.write(line)
    
    condor_file.close()

    #3. Produce executable
    sh_templ_file = open("{}/dq_exec_condor_temp.sh".format(current_path))
    local_sh = "{}/{}/{}.sh".format(current_path, log_dir, config_file)

    print("Creating executable ..")
    sh_file = open(local_sh, "w")
    for line in sh_templ_file:
        line=line.replace('CONFIG_DIR', config_dir)
        line=line.replace('CONFIG_FILE', config_file)
        line=line.replace('RUNSCRIPT', config_file)
        line=line.replace('OUT_DIR_NAME', tag)
        line=line.replace('OUTFILE', config_file)
        sh_file.write(line)
    sh_file.close()

    os.system('chmod u+x {}'.format(local_sh))
    
    os.system('condor_submit {}'.format(local_condor))

    condor_templ_file.close()
    sh_templ_file.close()
    singularity_templ_file.close()

def re_submit(log_dir):

    current_path =  os.environ['PWD']

    for filename in os.listdir("{}/{}".format(current_path, log_dir)):
        if filename.endswith(".error"):
            config_file = filename[:-6]
            
            #Open file
            local_err = "{}/{}/{}".format(current_path, log_dir, filename)
            with open(local_err, "r") as f:
                first_line = f.readline()
                err_message = "could not open image"

                if err_message in f.read():
                    print("Re-submitting {}...".format(config_file))
                    local_condor = "{}/{}/{}.sub".format(current_path, log_dir, config_file)
                    os.system('condor_submit {}'.format(local_condor))

                    #Remove the error file
                    os.remove(local_err)


def main():

    log_dir = "logs_Aprime_Electrons_Scan_z200_600_20_04_2022"
    re_submit(log_dir)
            
        
if __name__ == "__main__":
    main()