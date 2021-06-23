#!/usr/bin/env python
from pliers.extractors import FarnebackOpticalFlowExtractor
import numpy as np
import pandas as pd
import os
from pliers.stimuli import VideoStim
import sys

# usage:
# extract_optic_flow.py ../../path/to/stim.mp4 ../path/to/outdir/


#method to find the index of nearest value in an array
def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return idx,array[idx]

stimulus = sys.argv[1]
outdir = sys.argv[2]
stim = os.path.splitext( os.path.split(stimulus)[1] )[0] # split stim name eg 'TP'

vs = VideoStim(stimulus)
ext = FarnebackOpticalFlowExtractor()
results = ext.transform(vs)

optic_flow = results.to_df(object_id='auto')
optic_flow.to_pickle(f"{outdir}{stim}_optic_flow.pkl")
