
import numpy as np
import sys
import os

configfile: "/home/users/a/algren/work/atlas_open_data/workflow/config/download_files.yaml"
workdir: config['workdir']
scriptdir = config['scriptdir']
# container: config["container_path"]
pipeline = config['pipeline']

# out_get_locations={}
# if not pipeline['get_location']:  # do not chain the two workflows. RUN get_locations first!!!
#     include: f"{scriptdir}/workflow/get_locations.smk"

# command_to_run = 'cernopendata-client download-files --recid 80017 --filter-regexp 37620506'
command_to_download = 'cernopendata-client download-files'

out_download_files = {}

for recid, regexp_lst in config['recid'].items():

    # Need to know the name of the downloaded files
    try:
        recid_files = np.array(np.loadtxt(f"{recid}.txt", dtype=str))
    except:
        print(f"ERROR FILE MISSING: File {recid}.txt not found. Run get_locations first.")
        sys.exit()

    recid_vals = [
        int(i.split('PHYSLITE.')[-1].split('._')[0]) for i in recid_files
        ]

    if len(regexp_lst)==0:
        #calculate recid number from all files
        regexp_lst = recid_vals
    
    for regexp_value in regexp_lst:
        mask = np.in1d(recid_vals, regexp_value)

        out_recid_files = recid_files[mask]
        out_files = [f'{recid}/{out_file.split("/")[-1]}' for out_file in out_recid_files]

        out_download_files[f'{recid},{regexp_value}'] = out_files
# print(    list(out_download_files.values()))
if pipeline['download_files']:  # do not chain the two workflows. RUN get_locations first!!!
    rule all:
        input:
            list(out_download_files.values())

for inputs, out_file in out_download_files.items():

    recid, regexp = inputs.split(',')
    print()
    print('Inputs: ', recid, regexp)
    print('Outputs: ', out_file)
    rule:
        name: f"download_files_{inputs}"
        # input:
        #     inpt
        params:
            recid=recid,
            regexp=regexp,
        output: 
            out_file
        shell:
            f"""{command_to_download} --recid {{params.recid}} --filter-regexp {{params.regexp}} --server https://opendata-qa.cern.ch"""
