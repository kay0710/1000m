'''
make video files using cv2 & pillow module
'''
import cv2
import numpy as np
import pandas as pd
import os, sys, random
# import datetime
from helpers import decor
from helpers import INIT as init
from PIL import ImageDraw, Image

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

# t2v class
class T2V:
    '''
    Class of fucntions for "text to video" process
    '''
    def __init__(self):
        print("[SETTING] Check settings ")
        print('========= Resolution:', init.resolution)
        print('========= Height:', init.height)
        print('========= Width:', init.width)
        print("========= Defalut font:", init.font_dict[init.font_default], init.font_size)
        print("========= Word Font:", init.font_dict[init.font_word], init.font_size_word)

    # setting of video
    def making_imageAraay(arg_list: list, 
                          arg_cols: list | None = init.columns,
                          bg_randomness: bool | None = init.bg_randeom):
        '''
        Make list of frames using data
        @ Args:
            arg_list:
                list of target data for make list of frames
            arg_cols:
                list of columns about data
            bg_randomness:
                T/F options for setting randon background
        @ Return:
            list of frames
        '''
        frame_array = []

        if bg_randomness == True:
            randNum = random.sample(range(0,len(init.background_dict)-1),1)
            bg_img_path = init.background_dict[randNum[0]]
            print("[SETTING] Bacground of video will be set randomly:", bg_randomness, randNum[0])
        else:
            bg_img_path = init.background_dict[999]
        
        # will make some options
        # xy_title = (init.width*(0.2/10), init.height*(1/20))
        # xy_logo = (init.width*(8.5/10), init.height*(1/20))
        # xy_subject = (init.width*(1/2), init.height*(2.5/5))
        
        xy_progress = (init.width*(8.8/10), init.height*(1.3/10))
        xy_world = (init.width*(1/2), init.height*(2.2/5))
        xy_meaning = (init.width*(1/2), init.height*(2.6/5))
        xy_sentence = (init.width*(1/2), init.height*(4/5))

        df = pd.DataFrame(arg_list, columns=arg_cols)

        for i in range(len(arg_list)):
            word = df[i:i+1]['word'].values[0]
            meaning = df[i:i+1]['meaning'].values[0]
            sentence = df[i:i+1]['sentence'].values[0]
            progress = str(i+1) + "/" + str(len(arg_list))

            if len(bg_img_path) == 0:
                bg_img = np.full(shape=(init.height,init.width,3), 
                                    fill_value=255, dtype=np.uint8)
            else:
                bg_img = cv2.imread(filename=bg_img_path)

            bg_img_pil = Image.fromarray(bg_img)
            draw=ImageDraw.Draw(bg_img_pil)

            draw.text(xy=xy_world, text=word,
                fill=(0,0,0), font=init.font_pil_word,
                anchor='mm', align='center')
            draw.text(xy=xy_meaning, text=meaning,
                fill=(0,0,0), font=init.font_pil_word,
                anchor='mm', align='center')
            draw.text(xy=xy_sentence, text=sentence,
                fill=(0,0,0), font=init.font_pil_sentence,
                anchor='mm', align='center')
            draw.text(xy=xy_progress, text=progress,
                fill=(0,0,0), font=init.font_pil,
                anchor='mm', align='center')

            bg_img_array = np.array(bg_img_pil)
            frame_array.append(bg_img_array)
            if (i+1)%5 == 0:
                print("[Process] Frame:", i+1, "/", len(arg_list))
            elif i == len(arg_list)-1:
                print("[Process] Frame:", i+1, "/", len(arg_list))

            progress = None

        print("total frames:", len(frame_array))
        return frame_array
    
    # function for make frames to video
    def saveVideo(start_num: str,
                  arg_frames: list,
                  arg_subject: str | None = init.subject,                
                  arg_fps: float | None = init.fps,
                  arg_fourcc: str | None = init.fourcc):
        '''
        Function for saving video file using frames
        @ Args:
            start_num:
                start number, set for video file name
            arg_frames:
                list of frames made with bg, words data
            arg_subject:
                subject of contents set by user-option
            arg_fps:
                frames per seconds
            arg_fourcc:
                CODEC for video file
        '''
        filename = init.inter_video_path + arg_subject + '/' + start_num + arg_fourcc
        out_video = cv2.VideoWriter(filename=filename, 
                                    fourcc=cv2.VideoWriter_fourcc(*init.fourcc_dict[arg_fourcc]), 
                                    fps=arg_fps, 
                                    frameSize=(init.width, init.height))
        frame_array = arg_frames
        for i in range(len(frame_array)):
            out_video.write(frame_array[i])
            out_video.write(frame_array[i])
            out_video.write(frame_array[i])
        out_video.release()
        frame_array = []
        print("[END] Video is created:", filename + '\n')

    # automation of process
    @decor.stop_watch
    def make_inter_video(arg_path: str | None = init.inter_video_path, 
                         arg_subject: str | None = init.subject,
                         arg_list: list | None = init.seperated_list):
        '''
        Process of making video file
        @ Args:
            arg_path:
                path of intermediate video (output of function)
            arg_subject:
                subject of contents set by user-option
            arg_list:
                list of seperated dictionaries, max word is set by user-option
        '''
        init.createDirectory(path=arg_path, folder_name=arg_subject)

        for i in range(len(arg_list)):
            TARGET_WORDS = arg_list[i]
            frames = T2V.making_imageAraay(TARGET_WORDS)
            print("[Process] Video:", i+1, '/', (len(init.target_dict)//10)+1)
        
            T2V.saveVideo(arg_frames=frames, start_num=str(i), arg_subject=arg_subject)