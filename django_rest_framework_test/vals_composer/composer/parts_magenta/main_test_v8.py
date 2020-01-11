from .main_test_parts import music_module_beta_v2 as beta
from .main_test_parts import music_module_alpha_v2 as alpha
import glob,os


def main(token_name,real_midi_name,primer_melody_list,chord_name,backing_dir,mp4_path,bpm,score):
    
    '''
    (example)
    
    token_name = 'takashitakashi_91'
    real_midi_name =  os.path.dirname(os.path.abspath(__file__)) + "/music_database/hakujitu/melody/hakujitu_64_Reed_v2.mid",
    primer_melody_list = [82,-2,-2],
    chord_name = 'Am G E7 F#m7b5 Am G E7 F#m7b5 Am G E7 F#m7b5 Am G E7 F#m7b5',
    backing_dir = os.path.dirname(os.path.abspath(__file__)) +" music_database/hakujitu/backing"
    mp4_path = "/Users/nemototakashi/Downloads/10592513530727.MP4"
    bpm = 93 
    score = 1
    '''


    
    path_names = beta.main(token=token_name,
             primer_melody = primer_melody_list,
             backing_chords = chord_name,
             real_mid = real_midi_name)
    
    dir_path =  os.path.dirname(os.path.abspath(__file__))+ '/main_test_parts/improv_rnn/' + token_name

    backing_midis_path = glob.glob(backing_dir + "/*")
    only_backing = backing_midis_path
    magenta_midi = glob.glob(dir_path + '/*003-of-005.mid')
    #backing_midis_path.extend(magenta_midi)
    
    
    midis = []
    
    for i,name in enumerate(only_backing):
        alpha.midi_tempo_changer(name, dir_path+"/"+str(i)+".mid", bpm)
        midis.append(dir_path+"/"+str(i)+".mid")
    
    alpha.midi_sticker(dir_path,midis,'sticked_file')
    
    #alpha.midi_tempo_changer(dir_path + '/sticked_file.mid',dir_path + '/tempo_changed_backing.mid',bpm)
    alpha.midi_tempo_changer(magenta_midi[0],dir_path + '/no_sticked_file.mid',bpm)
    
    for i in path_names:
        os.remove(i)
    
    
    for n in midis:
        if os.path.exists(n):
            os.remove(n)
        else:
            pass

    #0~7 バイオリン
    if 0<= score <=7:
        alpha.inst_changer(dir_path+'/no_sticked_file.mid',40,dir_path,'per1') 
        #alpha.midi_pitch_change(dir_path+'/per1.mid',-5,dir_path,'per11')
        #alpha.midi_pitch_change(dir_path+'/per1.mid',12,dir_path,'per12')
        back_vol = 0
        mel_vol = 10
   
    
    #18,21,22~27 piano
    elif 22<= score <=27 or score == 18 or score == 21:
        alpha.inst_changer(dir_path+'/no_sticked_file.mid',0,dir_path,'per1')  
        #alpha.midi_pitch_change(dir_path+'/per1.mid',-5,dir_path,'per11')
        #alpha.midi_pitch_change(dir_path+'/per1.mid',12,dir_path,'per12')
        back_vol = 0
        mel_vol = 10
    
    # 8~15ストリング
    elif 8<= score <=15 :
        alpha.inst_changer(dir_path+'/no_sticked_file.mid',41,dir_path,'per1') 
        #alpha.midi_pitch_change(dir_path+'/per1.mid',-5,dir_path,'per11')
        #alpha.midi_pitch_change(dir_path+'/per1.mid',12,dir_path,'per12')
        back_vol = 0
        mel_vol = 10
     
    
    # 16,19 epiano
    elif score ==16 or score == 19 :
        alpha.inst_changer(dir_path+'/no_sticked_file.mid',2,dir_path,'per1') 
        #alpha.midi_pitch_change(dir_path+'/per1.mid',-5,dir_path,'per11')
        #alpha.midi_pitch_change(dir_path+'/per1.mid',12,dir_path,'per12')
        back_vol = 0
        mel_vol = 10
        
    
    # 17,20 sax
    elif score ==17 or score == 20 :
        alpha.inst_changer(dir_path+'/no_sticked_file.mid',65,dir_path,'per1') 
        alpha.inst_changer(dir_path+'/no_sticked_file.mid',71,dir_path,'per1') 
        #alpha.midi_pitch_change(dir_path+'/per1.mid',-5,dir_path,'per11')
        #alpha.midi_pitch_change(dir_path+'/per1.mid',12,dir_path,'per12')
        back_vol = 0
        mel_vol = 5
    
    
    
    
    

    
    mel_midis = glob.glob(dir_path+'/per*.mid')
    print(mel_midis)
    alpha.midi_sticker(dir_path,mel_midis,'mel_file')


    

    
    
    
    alpha.to_audio(os.path.dirname(os.path.abspath(__file__))+ '/main_test_parts/soundfont/main.sf2',
                  dir_path+'/mel_file.mid',
                  dir_path)
    
    alpha.to_audio(os.path.dirname(os.path.abspath(__file__))+ '/main_test_parts/soundfont/main.sf2',
                  dir_path+'/sticked_file.mid',
                  dir_path)
    
    
    alpha.wav_edit(dir_path + '/sticked_file.wav',dir_path + '/mel_file.wav',dir_path,'perfect',back_vol,mel_vol)
    
    #alpha.extract_audio(mp4_path,dir_path)
    
    
    
    alpha.audio_composer(moviefile = mp4_path,audiofile = dir_path + '/perfect.wav',out_filename = dir_path + '/perfect')
   
    #alpha.remove(dir_path , dir_path + '/perfect.mp4')
    
    return dir_path +'/perfect.mp4'
    

    

if __name__ == '__main__':
    main()



