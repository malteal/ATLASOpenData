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
    
    
    output_file = f"{config.paths.save_path}/{config.paths.output_name}.h5"
    logging.info(f"Name of output file {output_file}")

    logging.info("Load sample from root")
    data = config.root(variable_list=config.variables_from_root)
    
    logging.info("Do track association and add features")
    jets, tracks, culens, events = track_association.track_association(
        data[:config.maxevents], variables_to_extract=config.variables_to_save,
        verbose=True
        )
 
    df_jets = pd.DataFrame(jets)
    df_events = pd.DataFrame(events)
    df_merged_tracks = pd.DataFrame(tracks)
    logging.info(f"Number of jets: {len(df_jets)}")
    logging.info(f"Number of tracks: {len(df_merged_tracks)}")
    
    logging.info(f"Saving samples at {output_file}")
    with h5py.File(output_file, "w") as f:
        f.create_dataset("tracks", data=df_merged_tracks.values)
        f.create_dataset("tracks_columns", data=df_merged_tracks.columns.values.astype("S"))
        
        f.create_dataset("jets", data=df_jets.values)
        f.create_dataset("jets_columns", data=df_jets.columns.values.astype("S"))

        f.create_dataset("event_info", data=df_events.values)
        f.create_dataset("event_info_columns", data=df_events.columns.values.astype("S"))

        f.create_dataset("csts_culens", data=culens)

if __name__ == '__main__':
    main()
    