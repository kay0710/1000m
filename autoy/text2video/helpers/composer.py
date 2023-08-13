'''
make final output using moviepy module
'''
import os
import math
import pandas as pd
from helpers import INIT as init
from moviepy.editor import VideoFileClip, AudioFileClip,\
                            CompositeAudioClip, concatenate_audioclips

def concat_audio5s(arg_word,
                   arg_subject=init.subject,
                   auto_concat=init.auto_concat):
    # will make some options
                #    arg_mute_path=init.resource_path+'audio/',
                #    arg_mute_sec=0.5,):
    # mute_file = arg_mute_path + str(arg_mute_sec) + 's.mp3'
    # mute_clip = AudioFileClip(mute_file)

    if auto_concat == True:
        concat_file = init.inter_audio_path + 'words/' + arg_subject + '/' + arg_word + '_concat.mp3'
        concat_clip = AudioFileClip(concat_file)
        concat_list = [concat_clip]
        play_time = concat_clip.duration
    else:
        word_file = init.inter_audio_path + 'words/' + arg_subject + '/' + arg_word + '_word.mp3'
        sent_file = init.inter_audio_path + 'words/' + arg_subject + '/' + arg_word + '_sent.mp3'
        word_clip = AudioFileClip(word_file)
        sent_clip = AudioFileClip(sent_file)
        concat_list = [word_clip, sent_clip]
        play_time = word_clip.duration + sent_clip.duration

    print("[CHECK] Original Play time:", math.floor(play_time*10)/10)
    if play_time > 5:
        print('[WARNING] Audio length(long):', arg_word)

    concat = concatenate_audioclips(concat_list)
    
    print("[Pregress] Concat elements:", len(concat_list))
    print("[CHECK] Final play time:", concat.duration, "s")
    print("[END] Audio editing:", arg_word)

    return concat

def make_compo_dict(arg_dict=init.seperated_dict_list, 
                    arg_cols=init.columns):
    compo_dict = {}
    for j in range(len(arg_dict)):
        TARGET_WORDS = arg_dict[j]
        temp_concat_list = []
        df = pd.DataFrame(TARGET_WORDS, columns=arg_cols)

        for i in range(len(TARGET_WORDS)):
            word = df[i:i+1]['word'].values[0]
            print("\n[START] Audio editing:", word)
            concat = concat_audio5s(arg_word=word)
            temp_concat_list.append(concat)
        compo_dict[j] = temp_concat_list
    return compo_dict

def make_output(arg_subject=init.subject,
                arg_inter_audio_path=init.inter_audio_path+'words/',
                arg_inter_video_path=init.inter_video_path,
                arg_output_path=init.output_path,
                arg_fourcc=init.fourcc,
                auto_clear=init.auto_clear):
    
    temp_compo_dict = make_compo_dict()
    for j in range(len(temp_compo_dict)):
        compo_list = []
        temp_compo_list = []
        inter_video_file = arg_inter_video_path + arg_subject + '/' + str(j) + arg_fourcc
        output_file = arg_output_path + arg_subject + "_" + str(j) + arg_fourcc

        temp_compo_list = temp_compo_dict[j]
        for i in range(len(temp_compo_list)):
            compo_list.append(temp_compo_list[i].set_start(5*i))
        compo = CompositeAudioClip(compo_list)
        video_clip = VideoFileClip(inter_video_file)

        if compo.duration > video_clip.duration:
            print('\n[WARNNING] Duration match(audio and video):')
            print('>> Audio:', compo.duration, 'Video:', video_clip.duration)
        else:
            final_clip = video_clip.set_audio(compo)
            final_clip.write_videofile(output_file)
            final_clip.close()
            print("[END] ALL output video is created:", output_file)

        compo.close()
        video_clip.close()
        if (i+1)%5 == 0:
                print("[Pregress] Frame:", i+1, "/", len(temp_compo_list))
        elif i == len(temp_compo_dict)-1:
            print("[Pregress] Frame:", i+1, "/", len(temp_compo_list))

    while(auto_clear):
        ans = input("\nDo yo want to clear intermeidate files? (y/n): ")
        if ans == 'n':
            auto_clear = False
        elif ans == 'y':
            auto_clear = False
            dir_audio = arg_inter_audio_path + arg_subject
            dir_video = arg_inter_video_path + arg_subject

            for f in os.listdir(dir_audio):
                os.remove(os.path.join(dir_audio, f))
            print("[DELETE] Intermediate audio files are deleted")

            for f in os.listdir(dir_video):
                os.remove(os.path.join(dir_video, f))
            print("[DELETE] Intermediate video files are deleted")
        else:
            print("Plz answer wtih 'y' or 'n'.")