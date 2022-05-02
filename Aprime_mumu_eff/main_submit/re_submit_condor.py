import os, sys
from os.path import exists
import subprocess

def re_submit_error(log_dir):

    current_path =  os.environ['PWD']

    for filename in os.listdir("{}/{}".format(current_path, log_dir)):
        if filename.endswith(".error"):
            config_file = filename[:-6]
            
            #Open file
            local_err = "{}/{}/{}".format(current_path, log_dir, filename)

            with open(local_err, "r") as f:
                first_line = f.readline()
                err_message = "No such file or directory"

                if err_message in f.read():
                    print("Re-submitting {}...".format(config_file))
                    local_condor = "{}/{}/{}.sub".format(current_path, log_dir, config_file)
                    os.system('condor_submit {}'.format(local_condor))

                    #Remove the error file
                    os.remove(local_err)


def re_submit_missing(log_dir):

    current_path =  os.environ['PWD']

    for filename in os.listdir("{}/{}".format(current_path, log_dir)):
        if filename.endswith(".sub"):

            config_file = filename[:-4]
            err_path = "{}/{}/{}.error".format(current_path, log_dir, config_file)

            if not exists(err_path):
                print("Re-submitting {}...".format(config_file))
                local_condor = "{}/{}/{}.sub".format(current_path, log_dir, config_file)
                os.system('condor_submit {}'.format(local_condor))

def main():

    log_dir = "logs_Aprime_Muons_Scan_z200_600_18_04_2022"
    re_submit_error(log_dir)
    #re_submit_missing(log_dir)
            
        
if __name__ == "__main__":
    main()