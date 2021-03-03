# -----------------------------------------------------------
# script to extract basic audio features from audio files
#
# first time using argparse believe it or not
# -----------------------------------------------------------
"""
script to extract a few basic audio features from an audio file.
pycochleagram is required to get cochleagrams
other dependencies: librosa, soundfile
Standard usage: extract_audiofeatures.py '/user/home/test.wav' 'test' '/user/home/exports/' -l
"""
import argparse
import numpy as np
import soundfile as sf
import librosa

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("wav_in", type=str, help="input wav file")
    parser.add_argument("output_base", type=str, help="basename of file output") # i can get this myself..
    parser.add_argument("output_dir", type=str, help="path to dir to save output")
    parser.add_argument("-c", "--cochleagram", help="extract 40 band cochleagram with pycochleagram")
    parser.add_argument("-c6", "--cochleagram6", help="extract 6 band cochleagram with pycochleagram")
    parser.add_argument("-l", "--low", help="extract low level features")
    args = parser.parse_args()
    y,sr=load_wave(args.wav_in)
    if args.low:
        extract_low_level(y,sr)
    if args.cochleagram:
        extract_cochleagram(y,sr)
    if args.cochleagram6:
        extract_voxel_decomp_cochleagram(y,sr)

def load_wav(wav_in):
    wav_file_name = wav_in
    wav_data, sr = sf.read(wav_file_name, dtype=np.int16)
    waveform = wav_data / 32768.0 # because it is 16bit this will scale it to -1 to 1
    y, sr = librosa.load(wav_file_name)
    return y,sr

def extract_low_level(y,sr):
    chroma = librosa.feature.chroma_stft(y=y, sr=sr, hop_length=2048)
    mfs = librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128,fmax=8000, hop_length=2048)
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13, hop_length=2048)
    np.save(args.output_dir+'/'args.output_base+'_chroma.npy', chroma)
    np.save(args.output_dir+'/'args.output_base+'_mfcc.npy', mfcc)
    np.save(args.output_dir+'/'args.output_base+'_mfs.npy', mfs)
    
def extract_cochleagram(y,sr):
    #requires pycochleagram
    from pycochleagram.cochleagram import cochleagram
    pc = cochleagram(signal=y, sr=sr, n=40,low_lim=186, hi_lim=6817, sample_factor=1)
    #np.save("/om2/user/jsmentch/data/audio_features/merlin_pycochleagram.npy",pc)
    from pycochleagram.cochleagram import apply_envelope_downsample
    pc_downsampled = apply_envelope_downsample(pc, mode='poly', audio_sr=sr, env_sr=22, )
    np.save(args.output_dir+'/'args.output_base+"_pycochleagram.npy",pc_downsampled)
    
def extract_voxel_decomp_cochleagram(y,sr):
    from pycochleagram.cochleagram import cochleagram
    pc = cochleagram(signal=y, sr=sr, n=6,low_lim=200, hi_lim=6400, sample_factor=1)
    # the first and last must be high and low pass filters (for reconstruction) that can be discarded
    from pycochleagram.cochleagram import apply_envelope_downsample
    pc_downsampled = apply_envelope_downsample(pc, mode='poly', audio_sr=sr, env_sr=22, )
    np.save(args.output_dir+'/'args.output_base+"_pycochleagram_6.npy",pc_downsampled)
    
if __name__ == "__main__":
    main()
