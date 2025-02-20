
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

def track_association(data, variables_to_extract,
                      track_var:str = 'InDetTrackParticlesAuxDyn',
                      verbose:bool=True):
    '''
    Adding eventNumber, runNumber and etc should be in its own function
    
    '''
    # loop over all events in the files
    jets_lst=[]
    tracks_lst = []
    events_lst = []

    for event_nr in tqdm(range(len(data)), disable=not verbose):
        
        # get labels and ghost tracks are used to associate tracks to jets
        ghost_tracks = data['AnalysisJetsAuxDyn.GhostTrack'][event_nr].tolist()
        
        # not present in data
        if 'AnalysisJetsAuxDyn.HadronConeExclTruthLabelID' in data.layout.fields:
            labels = data['AnalysisJetsAuxDyn.HadronConeExclTruthLabelID'][event_nr].to_numpy()
        else:
            labels = np.ones(len(ghost_tracks)) * -999
        
        jets = data[[f'{i}.{col}' for i,j in variables_to_extract['jet'].items() for col in j]][event_nr].tolist()
        tracks = data[[f'{i}.{col}' for i,j in variables_to_extract['track'].items() for col in j]][event_nr].tolist()
        events = data[[f'{i}.{col}' for i,j in variables_to_extract['event'].items() for col in j]][event_nr].tolist()
        
        # remove possible lists in events
        #'EventInfoAuxDyn.mcEventWeights' is a list which is an issue
        events = {i: j[0] if isinstance(j, list) else j for i,j  in events.items()}

        # loop over all jets in the event
        for i, index in link_tracks_and_jets_by_persIndex(ghost_tracks, labels):
            
            # get jet
            jet = {col: jets[col][i] for col in jets}
            
            # get tracks
            track = {col: np.array(tracks[col])[index] for col in tracks}
            
            track[f'{track_var}.eta'] = physics.theta_to_eta(track[f'{track_var}.theta'])

            track[f'{track_var}.pt'] = physics.qOverP_to_pT(track[f'{track_var}.qOverP'], track[f'{track_var}.phi'])
            
            # adding to list
            # event info will be duplicated for each jet in an event
            events_lst.append(events)
            tracks_lst.append(track)
            jets_lst.append(jet)
    
    if len(jets_lst)==0:
        raise ValueError('No jets found in the data')
    
    # this will take long time if there is alot of tracks
    tracks_lst, culens = utils.merge_dict_of_lists(tracks_lst)
    
    return jets_lst, tracks_lst, culens, events_lst