#!/usr/bin/env python
# coding: utf-8

import os,glob
import subprocess
from pathlib import Path
import re
import pretty_midi
import csv
import os
import subprocess


def melody_validator(melody: list):
    if type(melody) == str:
        try:
            melody = list(map(int, melody.replace("[", "").replace("]", "").split(",")))
        except ValueError:
            print('primer_melodyの値が適切ではありません。-2~127の整数のリストで入力してください。')
            print("[60]をセットします")
            melody = [60]
    elif type(melody) != list:
        print("primer_melodyの値が適切ではありません。-2~127の整数のリストで入力してください。")
        print("[60]をセットします")
        melody = [60]
    else:
        try:
            melody = list(map(int, melody))
        except ValueError:
            print('primer_melodyの値が適切ではありません。-2~127の整数のリストで入力してください。')
            print("[60]をセットします")
            melody = [60]
    melody = [(m if -2 <= m <= 127 else 60) for m in melody]
    return melody


def call_improv_rnn(token, primer_melody, backing_chords):
    
    os.mkdir(os.path.dirname(os.path.abspath(__file__))+"/improv_rnn/" + token)
    config = "chord_pitcher_improv"
    bundle_file = os.path.dirname(os.path.abspath(__file__)) + "/chord_pitches_improv.mag"    
    output_dir = os.path.dirname(os.path.abspath(__file__))+"/improv_rnn/" + token
    num_outputs = 1
    primer_melody = melody_validator(primer_melody)
    backing_chords = backing_chords
    render_chords = False
    
    cmd = [
         'improv_rnn_generate',
        f'--config={config}',
        f'--bundle_file={bundle_file}',
        f'--output_dir={output_dir}',
        f'--num_outputs={num_outputs}',
        f'--primer_melody={primer_melody}',
        f'--backing_chords={backing_chords}',
        f'--render_chords={render_chords}',]
    subprocess.run(cmd)
    mid_name = glob.glob(os.path.dirname(os.path.abspath(__file__)) + '/improv_rnn/' + token+'/*')
    name_1 = mid_name[0]
    return name_1
    
def call_music_vae(token, input_midi1, input_midi2):

    config = "hierdec-mel_16bar"

    checkpoint_file = os.path.dirname(os.path.abspath(__file__)) + "/hierdec-mel_16bar.tar"
    
    mode = "interpolate"
    
    output_dir = os.path.dirname(os.path.abspath(__file__))+"/improv_rnn/" + token

    num_outputs = 5
    
    input_midi_1 = input_midi1
    
    input_midi_2 = input_midi2
    
    cmd = [
        'music_vae_generate',
        f'--config={config}',
        f'--checkpoint_file={checkpoint_file}',
        f'--output_dir={output_dir}',
        f'--num_outputs={num_outputs}',
        f'--input_midi_1={input_midi_1}',
        f'--input_midi_2={input_midi_2}',
        f'--mode={mode}',
    ]
    subprocess.run(cmd)
    

def get_vae_pathlist(dir_path):
    
    files = glob.glob(dir_path + "/hierdec-mel_16bar_interpolate" + "*")
    
    vae_file_paths = []
    for file in files:                 #1ファイルづつループ
        filepath = str(file) #現在のファイルフルパス取得
        vae_file_paths.append(filepath) #pathlist作成
    
    return vae_file_paths

def main(token, primer_melody, backing_chords, real_mid):
    
    name = call_improv_rnn(token=token, primer_melody=primer_melody, backing_chords = backing_chords)
    call_music_vae(token=token, 
                   input_midi1= name,
                   input_midi2=real_mid)
    path_names = get_vae_pathlist(os.path.dirname(os.path.abspath(__file__))+ '/improv_rnn/' + token)
    
    return path_names
    

if __name__ == '__main__':
    main()
    
    
    
    