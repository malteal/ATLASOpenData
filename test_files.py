
# built-in packages
from glob import glob

# external packages
import hydra
import uproot
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import awkward as ak

# internal packages
from src import physics as phy
from src import utils

# own packages
from tools import misc, hydra_utils

if __name__ == "__main__":
    config = hydra_utils.hydra_init("config/config.yaml")
    
    paths = list(Path(config['paths']["data_path"]).rglob("*.root*"))[:1]
    
    vars, vars_all = utils.create_root_keys(config.variables)
    
    for path in paths:
        tree = uproot.open(path)[config['tree']]
        tree_keys = tree.keys()
        
        vars_all = [i for i in tree_keys if np.isin(vars_all, i.split('.')[0]).any() & (('/') not in i)]
        
        data = tree.arrays(vars+vars_all)

    # 5: b, 0: light, 4: c, 15: tau
    color_map = {5: 'skyblue', 0: 'red', 4: 'green', 15: 'purple'}
    scaling = 2
    for i in range(1):

        labels = data['AnalysisJetsAuxDyn.HadronConeExclTruthLabelID'][i].to_numpy()

        # Map labels to colors
        colors = [color_map[label] for label in labels]
        

        plt.figure()

        plt.scatter(
            data['AnalysisJetsAuxDyn.eta'][i].to_numpy(),
            data['AnalysisJetsAuxDyn.phi'][i].to_numpy(),
            s = scaling*data['AnalysisJetsAuxDyn.pt'][i].to_numpy()/1000,
            color=colors,
            alpha=0.5,
        )
        
        for name, color in zip(['InDetTrackParticlesAuxDyn',
                    
                    # 'ExtrapolatedMuonTrackParticlesAuxDyn',
                    # 'CombinedMuonTrackParticlesAuxDyn',
                    # 'MuonSpectrometerTrackParticlesAuxDyn',
                  ], ['black', 'orange', 'brown', 'pink', 'blue']):

            eta = phy.theta_to_eta(data[f'{name}.theta'][i].to_numpy())

            phi = data[f'{name}.phi'][i].to_numpy()

            pT = phy.qOverP_to_pT(data[f'{name}.qOverP'][i].to_numpy(), phi)/1000
            
            plt.scatter(eta, phi, s=scaling*np.abs(pT), marker ='x', color=color)
            jet_eta = data['AnalysisJetsAuxDyn.eta'][0,0]
            jet_phi = data['AnalysisJetsAuxDyn.phi'][0,0]
            dR = np.sum(phy.delta_R(jet_eta, jet_phi, eta, phi)<1)
            print(dR)

        plt.xlabel('$\eta$')
        plt.ylabel('$\phi$')
        # for name, color in zip([
        #     'AnalysisMuonsAuxDyn',
        #     'AnalysisElectronsAuxDyn',
        #           ], ['black', 'orange', 'brown', 'pink', 'blue']):

        #     plt.scatter(data[f'{name}.eta'], 
        #                 data[f'{name}.phi'],
        #                 s=scaling*np.abs(data[f'{name}.pt']), marker ='x', color=color)

        # plt.xlabel('$\eta$')
        # plt.ylabel('$\phi$')

    plt.figure()
    n_track = ak.flatten(data['AnalysisJetsAuxDyn.DFCommonJets_QGTagger_NTracks']).to_numpy()
    plt.hist(n_track[n_track>0], bins=30)
    plt.yscale('log')