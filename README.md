# ATLASOpenData

## Install correct snakemake
- TODO: do a snakemake install 

    snakemake-executor-plugin-slurm==0.4.1 

    snakemake==8.4.1

`pip install git+https://github.com/snakemake/snakemake`
## Download files
### Get path locations
To download the files we use the `cernopendata-client` package.
First figureout what recid you need. As an example the recid number is the last number in this url: https://opendata.cern.ch/record/80020,
so 80020.
Then run:
1. `workflow/get_locations.smk`
    - This will output the path of all files in the record.
    - The paths should be contained in a `recid.txt`.
    - Following the example from above it should be `80020.txt`


### Download files



### Process file
To process the files, run `run/extract_variables_and_dump.py`. It will be slow if there are alot of events

The processed files can be plotted in `evaluate/test_processed_files.py`


# TODOs
1. write smk so `run/extract_variables_and_dump.py` handle a single file
2. afterwards write a merge scripts that merge all h5 files from `run/extract_variables_and_dump.py`

3. Add scalar variables to h5 
4. Add weighting scheme for MC
