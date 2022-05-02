import os, sys
import subprocess
from datetime import datetime
now = datetime.now()

from os.path import exists

def check_missing(log_dir):

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
    
    config_dir = "/mnt/T2_US_MIT/hadoop/mitgroups/DarkQuest/dhoang/Aprime_Muons_Scan_z200_600_18_04_2022/"
    out_dir = "/mnt/T2_US_MIT/hadoop/mitgroups/DarkQuest/dhoang/DCEM_Aprime_Muons_Scan_z200_600_21_04_2022/"

    file_count = 0
    #Loop through the files
    for filename in os.listdir(config_dir):
        if filename.endswith("_DST.root"):
            config_file = filename[:-9]
            path_to_file = out_dir + config_file + ".root"
            if not exists(path_to_file): 
                print(config_file)
                file_count+= 1

    print("Missing {} files in total".format(file_count))
            

        
if __name__ == "__main__":

    main()