# handle links in open dataset

from tqdm import tqdm
import pandas as pd

def get_clean_links(link, allow_empty:bool=True):
    "should write some docs"
    track_lst = {}
    for nr, i in tqdm(enumerate(link), disable=True):
        if len(i)==0:
            continue
        else:
            _df = pd.DataFrame(i)
            _mask = _df['m_persKey']!=0
            if (_mask.sum()==0) and (not allow_empty):
                continue
            track_lst[nr] = _df[_mask]
    return track_lst

