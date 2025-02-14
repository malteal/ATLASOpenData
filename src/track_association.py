
import logging
import numpy as np
from tqdm import tqdm
from src import links_utils,physics, utils

def link_tracks_and_jets_by_persIndex(GhostTracks: list, truth_label: list):
    # get jet associated to tracks
    jet_associated_link = links_utils.get_clean_links(GhostTracks)
    
    if len(truth_label)!=len(GhostTracks):
        logging.warning('The number of jets and the number of associated tracks are not equal.')
        
    for key in tqdm(jet_associated_link, leave=False, disable=True):
        index = jet_associated_link[key]['m_persIndex'].values

        yield key, index

def track_association(data, verbose:bool=True):
    '''
    Adding eventNumber, runNumber and etc should be in its own function
    
    '''
    # loop over all events in the files
    jets=[]
    tracks = []
    for event_nr in tqdm(range(len(data)), disable=not verbose):
        
        # get labels and ghost tracks are used to associate tracks to jets
        ghost_tracks = data['AnalysisJetsAuxDyn.GhostTrack'][event_nr].tolist()
        
        # not present in data
        if 'AnalysisJetsAuxDyn.HadronConeExclTruthLabelID' in data.layout.fields:
            labels = data['AnalysisJetsAuxDyn.HadronConeExclTruthLabelID'][event_nr].to_numpy()
        else:
            labels = np.ones(len(ghost_tracks)) * -999
        
        # loop over all jets in the event
        for i, index in link_tracks_and_jets_by_persIndex(ghost_tracks, labels):
            
            # truth jet
            jet = {
                'eta': data['AnalysisJetsAuxDyn.eta'][event_nr].to_numpy()[i],
                'phi': data['AnalysisJetsAuxDyn.phi'][event_nr].to_numpy()[i],
                'pt': data['AnalysisJetsAuxDyn.pt'][event_nr].to_numpy()[i]/1000,
                'HadronConeExclTruthLabelID': labels[i],
                'eventNumber': data['EventInfoAuxDyn.eventNumber'][event_nr],
                'runNumber': data['EventInfoAuxDyn.runNumber'][event_nr],
            }
            
            track_var = 'InDetTrackParticlesAuxDyn'
            track_eta = physics.theta_to_eta(data[f'{track_var}.theta'][event_nr][index].to_numpy())
            track_phi = data[f'{track_var}.phi'][event_nr][index].to_numpy()
            track_pt = physics.qOverP_to_pT(data[f'{track_var}.qOverP'][event_nr][index].to_numpy(), track_phi)
            
            track = {
                'eta': track_eta,
                'phi': track_phi,
                'pt': track_pt/1000,
            }
            
            tracks.append(track)
            jets.append(jet)
    
    # this will take long time if there is alot of tracks
    tracks, culens = utils.merge_dict_of_lists(tracks)
    
    return jets, tracks, culens