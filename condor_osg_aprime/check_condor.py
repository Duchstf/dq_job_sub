import os, sys
import subprocess
from datetime import datetime
now = datetime.now()

from os.path import exists


def main():
    
    config_dir = "/mnt/T2_US_MIT/hadoop/mitgroups/DarkQuest/APrime_Configs/displaced_Aprime_Electrons_z200-600/"
    out_dir = "/mnt/T2_US_MIT/hadoop/mitgroups/DarkQuest/dhoang/Aprime_Electrons_Scan_z200_600_28_04_2022/"

    file_count = 0

    #Loop through the files
    for filename in os.listdir(config_dir):
        if filename.startswith("Eta"):
            config_file = filename[:-4]
            path_to_file = out_dir + config_file + ".root"
            if not exists(path_to_file): 
                file_count+=1
                print(config_file)
    

    print("Finished Checking!, Total missing files: {}".format(file_count))

            

        
if __name__ == "__main__":
    main()