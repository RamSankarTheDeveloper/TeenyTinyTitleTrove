import os
import librosa
import numpy as np
from fastdtw import fastdtw
from multiprocessing import Pool
import config

def extract_mfcc(audio_file):
    print(f'extracting {audio_file}')
    y, sr = librosa.load(audio_file)
    mfcc = librosa.feature.mfcc(y=y, sr=sr)
    return mfcc

def calculate_dtw_distance(args):
    mfcc1, mfcc2 = args
    distance, _ = fastdtw(mfcc1.T, mfcc2.T)
    return distance

def create_mfcc_dict(directory):
    print(f'getting {directory}')
    mfcc_dict = {}
    audio_files = [audio_file for audio_file in os.listdir(directory) if audio_file.endswith(f"{config.audio_format}")]
    
    with Pool() as pool:
        mfcc_list = pool.map(extract_mfcc, [os.path.join(directory, audio_file) for audio_file in audio_files])

    for audio_file, mfcc in zip(audio_files, mfcc_list):
        audio_name = os.path.splitext(audio_file)[0]
        mfcc_dict[audio_name] = mfcc

    return mfcc_dict

def compare_audio_files(dir1, dir2):
    mfcc_dict1 = create_mfcc_dict(dir1)
    mfcc_dict2 = create_mfcc_dict(dir2)

    comparison_result = {}
    for audio_file1, mfcc1 in mfcc_dict1.items():
        comparison_result[audio_file1] = {}
        for audio_file2, mfcc2 in mfcc_dict2.items():
            print(f'{audio_file1} is comparing with {audio_file2}')
            distance = calculate_dtw_distance((mfcc1, mfcc2))
            comparison_result[audio_file1][audio_file2] = distance

    return comparison_result

if __name__ == "__main__":
    dir1 = "path/to/first_directory"
    dir2 = "path/to/second_directory"
    
    result = compare_audio_files(dir1, dir2)
    print(result)
