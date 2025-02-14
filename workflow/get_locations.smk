
configfile: "/home/users/a/algren/work/ATLASOpenData/workflow/config/download_files.yaml"
workdir: config['workdir']
pipeline = config['pipeline']

command_to_get_locs = 'cernopendata-client  get-file-locations --recid'

out_get_locations = {}

for recid, lst in config['recid'].items():
    out_get_locations[recid] = f"{recid}.txt"

# if pipeline['get_location']:
rule all:
    input:
        list(out_get_locations.values())

for recid, out in out_get_locations.items():
    rule:
        name: f"get_locations_{recid}"
        params:
            recid=recid,
        output:
            out
        shell:
            f""" 
             pip install cernopendata-client[pycurl] && 
            {command_to_get_locs} {{params.recid}} > {{output}}
            """
