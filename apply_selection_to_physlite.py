# import pyrootutils

# root = pyrootutils.setup_root(search_from=__file__, pythonpath=True)

import logging

# Import necessary modules
import hydra
from omegaconf import DictConfig
from src import utils

@hydra.main(config_path=str("config"),
            config_name="config.yaml",
            version_base=None)
def main(config: DictConfig) -> None:
    # Your script logic here
    
    # get files
    paths = utils.get_all_files(config['paths']["data_path"], "*.root*")[:1]
    
    # create root keys
    vars, vars_all = utils.create_root_keys(config.variables)
    
    # 
    print(f"Parameter 1: {paths}")

if __name__ == "__main__":
    main()