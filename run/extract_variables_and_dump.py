"Run full pipeline from pdf to token space"

import logging
import hydra
import pyrootutils
import numpy as np
import pandas as pd
import h5py

logging.basicConfig(level=logging.INFO)

root = pyrootutils.setup_root(__file__, dotenv=True, pythonpath=True, cwd=False)

from src import track_association

@hydra.main(config_path=str(root / "config/"), config_name="config", version_base=None)
def main(config):
    config = hydra.utils.instantiate(config)

    logging.info("Load data samples")
    data = config.root(variable_list=config.variables)
    
    logging.info("Load data samples")
    jets, tracks, culens = track_association.track_association(data, verbose=True)
        
    df_jets = pd.DataFrame(jets)
    df_merged_tracks = pd.DataFrame(tracks)
    
    logging.info(f"Save data samples at {config.paths.save_path}")
    
    with h5py.File(f"{config.paths.save_path}/ttbar.h5", "w") as f:
        f.create_dataset("csts", data=df_merged_tracks.values)
        f.create_dataset("csts_columns", data=df_merged_tracks.columns.values.astype("S"))
        
        f.create_dataset("jets", data=df_jets.values)
        f.create_dataset("jets_columns", data=df_merged_tracks.columns.values.astype("S"))

        f.create_dataset("csts_culens", data=culens)

if __name__ == '__main__':
    main()
    