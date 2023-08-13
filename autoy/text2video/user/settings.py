'''
SETTINGS for autoY - text2video

file naming rule
@inter_audio: intermediate/audio/words/SUBJECT/word.mp3
@inter_video: intermediate/video/SUBJECT/#.mp4
@output: output/SUBJECT_#.mp4

#TODO: change settings for your contents
'''
# settings
class SETTINGS:
    # settings of contents
    SUBJECT = 'Travel_EngWordsTop50' # using for video file name
    TTS_LANG = 'en' # audio language option (google tts)
    NUM_OF_WORD = 10 # max number of words in video
    DICT_NAME = 'travel50' # name of using word dictionary

    # settings of design
    RESOLUTION = 'yshorts_1500' # resolution of video
    FONT_DEFAULT = 'nanumGothic' # font type of text (except words)
    FONT_WORD = 'maruburi_bold' # font type of words
    FONT_SIZE = 30 # font size of text (except words)
    FONT_SIZE_WORD = 70 # font type of words
    BG_RANDOM = True # set the background randomly

    # settings of video
    FPS = 0.6 # frames per seconds >> 0.6 = 5s/frame
    FOURCC = '.mp4' # file type of video file

    # settings of automation options
    AUTO_VIDEO = True # option for make series of video
    AUTO_CONCAT = True # concatanate audio files of word and sentence
    AUTO_CLEAR = True # delete the intermediate files of audio and video

    # AUDIO = False
    # START_IDX = 0 # start index of choosen word