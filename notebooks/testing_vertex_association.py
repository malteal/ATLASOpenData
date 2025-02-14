
# built-in packages
import pyrootutils

root = pyrootutils.setup_root(search_from=__file__, pythonpath=True)

import logging

# external packages
import pandas as pd
from tqdm import tqdm
import matplotlib.pyplot as plt
import numpy as np

# internal packages
from src import physics as phy
from src import root_utils, links_utils, track_association

# own packages
from tools import hydra_utils

logging.basicConfig(level=logging.INFO)


if __name__ == "__main__":
    config = hydra_utils.hydra_init("../config/config.yaml")
    
    data = root_utils.load_root(config['paths']["data_path"], config.variables, config['tree'])
    
    # track_particle_link = data['PrimaryVerticesAuxDyn.trackParticleLinks'][1].tolist()
    # data['AnalysisJetsAuxDyn.GhostTrack']
    
    # track_lst = links_utils.get_clean_links(data['PrimaryVerticesAuxDyn.trackParticleLinks'][0].tolist())
    
    # inDet_associated_link = links_utils.get_clean_links(data['InDetTrackParticlesAuxDyn.TTVA_AMVFVertices'][0].tolist())

    # 5: b, 0: light, 4: c, 15: tau
    color_map = {5: 'skyblue', 0: 'red', 4: 'green', 15: 'purple'}
    scaling = 2

    # Map labels to colors
    for nr in range(5):
        labels = data['AnalysisJetsAuxDyn.HadronConeExclTruthLabelID'][nr].to_numpy()
        colors = [color_map[label] for label in labels]

        for i, index in track_association.link_tracks_and_jets_by_persIndex(
            data['AnalysisJetsAuxDyn.GhostTrack'][nr].tolist(), labels
            ):
            
            plt.figure()

            plt.scatter(
                data['AnalysisJetsAuxDyn.eta'][nr].to_numpy()[i],
                data['AnalysisJetsAuxDyn.phi'][nr].to_numpy()[i],
                s = scaling*data['AnalysisJetsAuxDyn.pt'][nr].to_numpy()[i]/1000,
                color=colors[i],
                alpha=0.5,
            )
            for name, color in zip(['InDetTrackParticlesAuxDyn'], 
                                    ['black']):

                eta = phy.theta_to_eta(data[f'{name}.theta'][nr].to_numpy())

                phi = data[f'{name}.phi'][nr].to_numpy()

                pT = phy.qOverP_to_pT(data[f'{name}.qOverP'][nr].to_numpy(), phi)/1000

                all_index = np.arange(len(eta))
                all_index = np.delete(all_index, index)
                
                plt.scatter(eta[index], phi[index], s=scaling*np.abs(pT)[index], marker ='x', color=color)
                plt.scatter(eta[all_index], phi[all_index], s=scaling*np.abs(pT)[all_index], marker ='x', color='red')
                # jet_eta = data['AnalysisJetsAuxDyn.eta'][0,0]
                # jet_phi = data['AnalysisJetsAuxDyn.phi'][0,0]
                # dR = np.sum(phy.delta_R(jet_eta, jet_phi, eta, phi)<1)
                # print(dR)

                plt.xlabel('$\eta$')
                plt.ylabel('$\phi$')
