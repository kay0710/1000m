# autoY - Text to Video

## Example of output
Visit **[Can Talk](https://youtube.com/@cantalk247)** channel if you want to see more outputs

https://github.com/kay0710/1000m/assets/100210846/e5575970-6a82-4166-9e21-505293473909

-----------

## Introduction

autoY - Text to Video is a program making video automatically for study language

- Just set some options & prepare text data
- ✨You can make a video EASILY✨

-----------

## Tech
![stack_anaconda](https://img.shields.io/badge/Anaconda-44a833?style=for-the-badge&logo=anaconda&logoColor=white) ![stack_python](https://img.shields.io/badge/python-3776AB?style=for-the-badge&logo=python&logoColor=white) ![stack_opencv](https://img.shields.io/badge/OpenCV-5c3ee8?style=for-the-badge&logo=opencv&logoColor=white) ![stack_googlecloud](https://img.shields.io/badge/google_tts-4285f4?style=for-the-badge&logo=googlecloud&logoColor=white) ![stack_moviepy](https://img.shields.io/badge/moviepy-f9d72c?style=for-the-badge&logo=&logoColor=white)

-----------

## Features

- Make audio using TTS service
    - Can select language, voice, accent (See detail: [Google TTS](https://cloud.google.com/text-to-speech/docs/voices?hl=ko))
- Make frames using text and it becomes a video
    - Can set background and text for you video
- Can combine audio and video
- Usage: [Demo](##Demo)

-----------

## Installation

1. autoY recommand using [Anaconda](https://www.anaconda.com/) **ver 22.9.0** to run.

Create conda environment with python **ver 3.10.0**
```sh
$ conda create -n <your_env_name> python=3.10
...
$ conda activate your_env_name
```

2. Install the dependencies and devDependencies using **resuirements.txt**

```sh
$ cd autoy/text2video
$ pip install -r requirements.txt
```

-----------

## Tree (Directory)
```txt
├── data
│   └── en_words.py
├── helpers
│   ├── __init__.py
│   ├── composer.py
│   ├── decor.py
│   ├── t2v.py
│   └── tts.py
├── intermediate
│   ├── audio
│   │   └── words
│   └── video
├── output
├── resources
│   ├── audio
│   │   └── 0.5s.mp3
│   ├── background
│       └── ...
│   └── fonts
│       └── ...
├── user
│   └── settings.py
├── requirements.txt
├── t2v_v1_2.ipynb
└── autoY_t2v.py
```

-----------

## Settings (with examples)
### User options
Can set some options easily at below path
PATH: `~/user/settings.py`
#### Subjcet options
>SUBJECT = 'Travel_EngWordsTop50' # using for video file name  
TTS_LANG = 'en' # audio language option (google tts)  
NUM_OF_WORD = 10 # max number of words in video  
DICT_NAME = 'travel50' # name of using word dictionary  
#### Design options
> RESOLUTION = 'yshorts_1500' # resolution of video  
FONT_DEFAULT = 'nanumGothic' # font type of text (except words)  
FONT_WORD = 'maruburi_bold' # font type of words  
FONT_SIZE = 30 # font size of text (except words)  
FONT_SIZE_WORD = 70 # font type of words  
BG_RANDOM = True # set the background randomly  
#### Video options
> FPS = 0.6 # frames per seconds >> 0.6 = 5s/frame  
FOURCC = '.mp4' # file type of video file  
#### Automation options
> AUTO_VIDEO = True # option for make series of video  
AUTO_CONCAT = True # concatanate audio files of word and sentence  
AUTO_CLEAR = True # delete the intermediate files of audio and video  

### Data setting
Should set 3 options to add data (below path)
PATH: `~/data/<yourdata>.py`

```python
columns=['word', 'meaning', 'sentence']
your_data_list=[
['word1', 'meaning1', 'sentence1'],
['word2', 'meaning2', 'sentence2'],
...
]
all_data_dict={
"nick_name_of_your_data_list": your_data_list,
...
}
```

-----------

## Demo
You can see demo of **autoy_t2v**
### How to start?
```sh
$ cd text2video
$ python autoY_t2v.py
```
### Where is the outputs?
PATH: `~/text2video/output`

-----------

## License

MIT

**Free Software!!**
**Feedback on the project is always welcome**
**Contact: reddevil8407@gmail.com**
