# -----------------------------------------------------------
# script to extract basic audio features from audio files
#
# 
# -----------------------------------------------------------
"""
script to extract a few basic audio features from an audio file at 10hz
pycochleagram is required to get cochleagrams
tensorflow and tensorflow_hub required for yamnet/audioset
other dependencies: librosa, soundfile
Standard usage: python extract_audiofeatures.py '/user/home/test.wav' -o '/user/home/exports/' -l
"""
#output: 2d array [time, features]
import argparse
from pathlib import Path
import numpy as np
#import soundfile as sf
import os
os.environ[ 'NUMBA_CACHE_DIR' ] = '/tmp/' #this fixes a numba bug to allow librosa import
import librosa

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("wav_in", type=str, help="input wav file", nargs='+')
    parser.add_argument("-o", "--output_dir", type=str, help="path to dir to save output", required=True)
    parser.add_argument("-c", "--cochleagram", action='store_true', help="extract 40 band cochleagram with pycochleagram")
    parser.add_argument("-c6", "--cochleagram6", action='store_true', help="extract 6 band cochleagram with pycochleagram")
    parser.add_argument("-l", "--low", action='store_true', help="extract low level features")
    parser.add_argument("-a", "--audioset", action='store_true', help="extract audioset features and embeddings")
    args = parser.parse_args()
    for wav in args.wav_in:
        basename = Path(wav).stem
        y,sr,dur_10hz=load_wav(wav)
        if args.low:
            extract_low_level(args,basename,y,sr,dur_10hz)
        if args.cochleagram:
            extract_cochleagram(args,basename,y,sr,dur_10hz)
        if args.cochleagram6:
            extract_voxel_decomp_cochleagram(args,basename,y,sr,dur_10hz)
        if args.audioset:
            extract_audioset(args,basename,y,sr,dur_10hz)

def load_wav(wav_in):
    #wav_data, sr = sf.read(wav_in, dtype=np.int16)
    #waveform = wav_data / 32768.0 # because it is 16bit this will scale it to -1 to 1
    y, sr = librosa.load(wav_in,sr=16000,mono=True)
    mod = y.size%(sr/10) #remainder
    dur_10hz = int( y.size/(sr/10)-(mod/(sr/10)) ) # duration in 10hz samples w/out remainder
    y=y[:-(int(mod))] # trim y to be multiple of 10hz samples
    return y,sr,dur_10hz

def extract_low_level(args,basename,y,sr,dur_10hz):
    rms = librosa.feature.rms(y=y, hop_length=1600)[:dur_10hz]
    chroma = librosa.feature.chroma_stft(y=y, sr=sr, hop_length=1600)[:dur_10hz]
    mfs = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128,fmax=8000, hop_length=1600)[:dur_10hz]
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13, hop_length=1600)[:dur_10hz]
    np.save(args.output_dir+'/'+basename+'_chroma.npy', chroma.T)
    np.save(args.output_dir+'/'+basename+'_mfcc.npy', mfcc.T)
    np.save(args.output_dir+'/'+basename+'_mfs.npy', mfs.T)
    np.save(args.output_dir+'/'+basename+'_rms.npy', rms.T)

def extract_cochleagram(args,basename,y,sr,dur_10hz):
    #requires pycochleagram
    print('double chek the dimensions!!! it should be 2d output time x feature')

    from pycochleagram.cochleagram import cochleagram
    from scipy.signal import resample
    #y=y[:-(y.size % sr)] #trim end of audio
    pc = cochleagram(signal=y, sr=sr, n=40,low_lim=186, hi_lim=6817, sample_factor=1)
    #np.save("/om2/user/jsmentch/data/audio_features/merlin_pycochleagram.npy",pc)
    #pc_downsampled = apply_envelope_downsample(pc, mode='poly', audio_sr=sr, env_sr=16)
    pc_downsampled = resample(pc, dur_10hz)
    np.save(args.output_dir+'/'+basename+"_pycochleagram.npy",pc_downsampled)
    
def extract_voxel_decomp_cochleagram(args,basename,y,sr,dur_10hz):
    print('double chek the dimensions!!! it should be 2d output time x feature')
    from pycochleagram.cochleagram import cochleagram
    from scipy.signal import resample
    #y=y[:-(y.size % sr)] #trim end of audio
    pc = cochleagram(signal=y, sr=sr, n=6,low_lim=200, hi_lim=6400, sample_factor=1)
    # the first and last must be high and low pass filters (for reconstruction) that can be discarded
    #from pycochleagram.cochleagram import apply_envelope_downsample
    #pc_downsampled = apply_envelope_downsample(pc, mode='poly', audio_sr=sr, env_sr=16)
    pc_downsampled = resample(pc, dur_10hz)
    np.save(args.output_dir+basename+"_pycochleagram_6.npy",pc_downsampled)
    
def extract_audioset(args,basename,y,sr,dur_10hz):
    import tensorflow as tf
    import tensorflow_hub as hub
    import numpy as np
    model = hub.load('https://tfhub.dev/google/yamnet/1')
    scores, embeddings, log_mel_spectrogram = model(y)
    np.save(args.output_dir+'/'+basename+"_as_scores.npy",scores.numpy())
    np.save(args.output_dir+'/'+basename+"_as_embed.npy",embeddings.numpy())
    
if __name__ == "__main__":
    main()
