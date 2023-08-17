'''
helpers package for t2v
'''

__author__  = "kay <reddevil8407@gmail.com>"
__status__  = "production"
__version__ = "2.0.0"
__date__    = "13 Aug 2023"

import sys, os
import pandas as pd
from PIL import ImageFont

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from data import en_words
from user.settings import SETTINGS as user

class INIT:
    '''
    Class of initialization user-option driven settings
    '''
    prj_path = os.getcwd()
    data_path = prj_path + '/data/'
    output_path = prj_path + '/output/'
    resource_path = prj_path + '/resources/'
    intermediate_path = prj_path + '/intermediate/'
    inter_audio_path = intermediate_path + 'audio/'
    inter_video_path = intermediate_path + 'video/'

    columns = en_words.columns
    tts_lang = user.TTS_LANG
    auto_concat = user.AUTO_CONCAT
    auto_clear = user.AUTO_CLEAR

    subject = user.SUBJECT
    dict_name = user.DICT_NAME
    numOFword = user.NUM_OF_WORD

    resolution = user.RESOLUTION
    font_default = user.FONT_DEFAULT
    font_word = user.FONT_WORD
    font_size = user.FONT_SIZE
    font_size_word = user.FONT_SIZE_WORD
    
    fps = user.FPS
    fourcc = user.FOURCC

    auto_video = user.AUTO_VIDEO
    bg_randeom = user.BG_RANDOM
    # audio = user.AUDIO
    # start_idx = user.START_IDX

    seperated_list = []
    target_list = en_words.target_word_dict[dict_name]
    for stx in range(0, ((len(target_list)+numOFword)//numOFword)):
        etx = stx*10+numOFword
        seperated_list.append(target_list[stx*10:etx])

    resolution_dict = {'square_500': (500,500,3),
                    'square_1000': (1000,1000,3),
                    'yshorts_1500': (1500,843,3),
                    'yshorts_1900': (1920,1080,3),
    }
    height = resolution_dict[resolution][0]
    width = resolution_dict[resolution][1]

    location_dict = {'yshorts_1500': {'xy_title': ((0.2/10), (1/20)),
                                    'xy_logo': ((8.5/10), (1/20)),
                                    'xy_progress': ((8.8/10), (1.3/10)),
                                    'xy_world': ((1/2), (2.2/5)),
                                    'xy_meaning': ((1/2), (2.6/5)),
                                    'xy_subject': ((1/2), (2.5/5)),
                                    'xy_sentence': ((1/2), (4/5))}
    }

    font_dict = {'marunuri_light': resource_path + 'fonts/마루 부리/MaruBuriTTF/MaruBuri-Light.ttf',
                'maruburi_bold': resource_path + 'fonts/마루 부리/MaruBuriTTF/MaruBuri-Bold.ttf',
                'nanumGothic': resource_path + 'fonts/나눔 글꼴/나눔고딕/NanumFontSetup_TTF_GOTHIC/NanumGothic.ttf',
    }
    font_pil = ImageFont.truetype(font=font_dict[font_default],
                                            size=font_size)
    font_pil_word = ImageFont.truetype(font=font_dict[font_word],
                                            size=font_size_word)
    font_pil_sentence = ImageFont.truetype(font=font_dict[font_word],
                                                size=font_size)

    background_dict = {0: resource_path + 'background/can Talk 1.png',
                    1: resource_path + 'background/can Talk 2.png',
                    2: resource_path + 'background/can Talk 3.png',
                    3: resource_path + 'background/can Talk 4.png',
                    4: resource_path + 'background/can Talk 5.png',
                    5: resource_path + 'background/can Talk 6.png',
                    999: '' # fixed background
    }

    fourcc_dict = {'.avi': 'DIVX',
                #    '.mp4': 'MP4S',
                '.mp4': 'MP4V',
                '.wmv': 'WMV1'
    }

    def createDirectory(path: str,
                        folder_name: str | None = subject):
        directory = path + folder_name
        try:
            if not os.path.exists(directory):
                os.makedirs(directory)
                print('[CREATED] Folder:', directory)
                return directory + '/'
        except OSError:
            print("Error: Failed to create the directory.")