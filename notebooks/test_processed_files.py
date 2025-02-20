'test processed files from extract_variables_and_dump.py'

import h5py as h5
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

if __name__ == '__main__':
    file_path = Path('/home/algren/work/data/ATLASOpenData/dump_top_nominal/')
    
    data = h5.File(file_path / 'data.h5', 'r')
    mc = h5.File(file_path / 'ttbar.h5', 'r')
    
    data_jets = data['jets'][:]
    mc_jets = mc['jets'][:]
    culens = data['csts_culens'][:]
    mc_culens = mc['csts_culens'][:]
    
    _, counts = np.unique(culens, return_counts=True)
    _, mc_counts = np.unique(mc_culens, return_counts=True)
    
    plt_kwargs = {'alpha': 0.5, 'histtype': 'step', 'density': True}
    _, bins, _ = plt.hist(counts, bins=20, label='Data', **plt_kwargs)
    _, bins, _ = plt.hist(mc_counts, bins=bins, label='MC', **plt_kwargs)
    plt.legend()

    plt.xlabel('Number of tracks per jet')
    
    for nr, i in enumerate(['eta', 'phi', 'pt']):
        plt.figure()
        _,bins,_=plt.hist(data_jets[:, nr], bins=20, label='Data',
                          **plt_kwargs)
        plt.hist(mc_jets[:, nr], bins=bins, label='MC', **plt_kwargs)
        plt.xlabel(i)
        plt.legend()
    
    