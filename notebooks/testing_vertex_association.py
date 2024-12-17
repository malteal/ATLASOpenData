
# built-in packages
import logging

# external packages
import pandas as pd
from tqdm import tqdm
import matplotlib.pyplot as plt
import numpy as np

# internal packages
from src import physics as phy
from src import utils

# own packages
from tools import hydra_utils

logging.basicConfig(level=logging.INFO)

def get_clean_links(link, allow_empty:bool=True):
    track_lst = {}
    for nr, i in tqdm(enumerate(link)):
        if len(i)==0:
            continue
        else:
            _df = pd.DataFrame(i)
            _mask = _df['m_persKey']!=0
            if (_mask.sum()==0) and (not allow_empty):
                continue
            track_lst[nr] = _df[_mask]
    return track_lst

if __name__ == "__main__":
    config = hydra_utils.hydra_init("config/config.yaml")
    
    data = utils.get_data(config['paths']["data_path"], config.variables, config['tree'])
    
    
    track_particle_link = data['PrimaryVerticesAuxDyn.trackParticleLinks'][1].tolist()
    # data['AnalysisJetsAuxDyn.GhostTrack']
    
    track_lst = get_clean_links(data['PrimaryVerticesAuxDyn.trackParticleLinks'][0].tolist())
    
    jet_associated_link = get_clean_links(data['AnalysisJetsAuxDyn.GhostTrack'][0].tolist())
    
    inDet_associated_link = get_clean_links(data['InDetTrackParticlesAuxDyn.TTVA_AMVFVertices'][0].tolist())

    # 5: b, 0: light, 4: c, 15: tau
    color_map = {5: 'skyblue', 0: 'red', 4: 'green', 15: 'purple'}
    scaling = 2

    labels = data['AnalysisJetsAuxDyn.HadronConeExclTruthLabelID'][0].to_numpy()
    # Map labels to colors
    colors = [color_map[label] for label in labels]
    nr = 0

    if len(jet_associated_link)!=len(labels):
        logging.warning('The number of jets and the number of associated tracks are not equal.')

    for i in tqdm(range(len(jet_associated_link))):
        
        plt.figure()

        plt.scatter(
            data['AnalysisJetsAuxDyn.eta'][0].to_numpy()[i],
            data['AnalysisJetsAuxDyn.phi'][0].to_numpy()[i],
            s = scaling*data['AnalysisJetsAuxDyn.pt'][i].to_numpy()[0]/1000,
            color=colors[i],
            alpha=0.5,
        )
        index = jet_associated_link[i]['m_persIndex'].values
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
