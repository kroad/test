#!/usr/bin/env python
# coding: utf-8

# In[5]:


from pydub import AudioSegment
from pydub.playback import play
import moviepy.editor as mp
import subprocess
import pretty_midi
import glob
import os, sys, getopt, random, re
from pathlib import Path

def mp3_to_wav(input_mp3):
    
    sound = pydub.AudioSegment.from_mp3(input_mp3)
    sound.export("output.wav", format="wav")

#合成したいmidiファイルをカンマ区切りで渡す 
#ex.  midi_sticker('file_a',file_b,...)
def midi_sticker(path,midis,name):
    
    #出力用のpretty_midiファイルを作る
    pm_out=pretty_midi.PrettyMIDI()
    
    #各入力midiファイルをpretty_midiファイルにして各インストをpm_outにコピー
    for midi in midis:
        pm=pretty_midi.PrettyMIDI(midi_file=midi) 
        for inst in pm.instruments:
            pm_out.instruments.append(inst)
        
    #pm_outをmidiファイルとして書き出し
    #出力ファイル名は　sticked_file.mid
    pm_out.write(path + '/'+name+'.mid')
    
    


def extract_audio(input_video,token_name):
    cmd = 'ffmpeg -i '+input_video+' -vcodec copy -map 0:0 '+token_name+'/_movie'+'.mp4'
    print(cmd)
    subprocess.call(cmd.split())
           
    #clip_input = mp.VideoFileClip(input_video).subclip()
    #clip_input.write_videofile(token_name + '/_movie.mp4')
    
#使う前にffmpegをpipしてね❤️

def audio_composer(moviefile,audiofile,out_filename):
    cmd = 'ffmpeg -i '+ moviefile + ' -i ' +audiofile+' -c:v copy -c:a aac -map 0:v:0 -map 1:a:0 '+out_filename+'.mp4'
    print(cmd)
    subprocess.call(cmd.split())
    
def mashup_midis(real_dir_path,magenta_midi):
    #real_dir_pathはプールしてある楽曲のディレクトリのpathを想定
    #magenta_midiはmagentaから吐き出されたmidi一曲のフルパスを想定
    #returnは[rea_midisのパス,magenta_midiのパス]のリストを想定
    midi_list = glob.glob(real_dir_path + "/*")
    midi_list.append(magenta_midi)
    print(midi_list)
    
    return midi_list


from mido import MidiFile, MidiTrack, MetaMessage, bpm2tempo


def make_new_meta(base_meta, new_bpm):
    
    new_meta = MidiTrack(filter(lambda tag: tag.type != 'set_tempo', base_meta))
    new_meta.append(MetaMessage('set_tempo', tempo=bpm2tempo(new_bpm), time=0))
    return new_meta


def midi_tempo_changer(midi_file_path, output_file_name, new_bpm):
    """
    meta情報のbpmの部分を任意のbpmに矯正します
    :param midi_file_path: midiのfile path
    :param output_file_name: bpm
    :param new_bpm: 80~150（参考）の数値
    :return: new_midi_file_path
    """
    midi = MidiFile(midi_file_path)
    midi.tracks[0] = make_new_meta(midi.tracks[0], new_bpm)
    midi.save(output_file_name)


def midis_tempo_changer(midi_file_paths, output_file_path, new_bpm, main_midi_index=0):
    midis = [MidiFile(midi_path) for midi_path in midi_file_paths]
    meta = make_new_meta(midis[main_midi_index].tracks[0], new_bpm)
    new_midi = MidiFile()
    new_midi.tracks.append(meta)

    # 各midiの0番目（メタ）だけ使わない
    # 例 [[1,2,3],[4,5,6],[7,8,9]] -> [2,3,5,6,8,9]
    tracks = sum([midi.tracks[1:] for midi in midis], [])
    new_midi.tracks += tracks

    new_midi.save(output_file_path)
    
def inst_changer(midi_file,p_num,out_dir,name):
    pm=pretty_midi.PrettyMIDI(midi_file=midi_file)
    pm.instruments[0].program=p_num
    pm.write(out_dir+'/'+name+'.mid')

def midi_pitch_change(midi_file,change_pitch,out_dir,name):
    pm =  pretty_midi.PrettyMIDI(midi_file)
    for instrument in pm.instruments:
        if not instrument.is_drum:
            for note in instrument.notes:
                note.pitch += change_pitch            
                pm.write(out_dir+'/'+name+'.mid')
                
def to_audio(sf2, midi_file, out_dir, out_type='wav', txt_file=None, append=True):
    """ 
    Convert a single midi file to an audio file.  If a text file is specified,
    the first line of text in the file will be used in the name of the output
    audio file.  For example, with a MIDI file named '01.mid' and a text file
    with 'A    major', the output audio file would be 'A_major_01.wav'.  If
    append is false, the output name will just use the text (e.g. 'A_major.wav')
    
    Args:
        sf2 (str):        the file path for a .sf2 soundfont file
        midi_file (str):  the file path for the .mid midi file to convert
        out_dir (str):    the directory path for where to write the audio out
        out_type (str):   the output audio type (see 'fluidsynth -T help' for options)
        txt_file (str):   optional text file with additional information of how to name 
                          the output file
        append (bool):    whether or not to append the optional text to the original
                          .mid file name or replace it
    """
    fbase = os.path.splitext(os.path.basename(midi_file))[0]
    if not txt_file:
        out_file = out_dir + '/' + fbase + '.' + out_type
    else:
        line = 'out'
        with open(txt_file, 'r') as f:
            line = re.sub(r'\s', '_', f.readline().strip())
            
        if append:
            out_file = out_dir + '/' + line + '_' + fbase + '.' + out_type
        else:
            out_file = out_dir + '/' + line + '.' + out_type

    subprocess.call(['fluidsynth', '-T', out_type, '-F', out_file, '-ni', sf2, midi_file])
    
def wav_edit(back_wav_path,mel_wav_path,out_dir,file_name,back_vol,mel_vol):
    back = AudioSegment.from_file(back_wav_path)
    back1 = back + back_vol
    mel = AudioSegment.from_file(mel_wav_path)
    mel1 = mel + mel_vol
    mixed = mel1.overlay(back1)
    perfect = mixed.fade_in(8000).fade_out(8000)
    perfect.export(out_dir +'/' + file_name +".wav", format='wav')    
    
    
def remove(dirpath,per_mp4_path):

    path = Path(dirpath)  
    
    files = path.glob("*")
    
    for file in files:                 #1ファイルづつループ
        filepath = str(file) #現在のファイルフルパス取得
        if not filepath  in  per_mp4_path :       
            
            os.remove(filepath)