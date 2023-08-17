'''
make audio files using tts service
'''
import pandas as pd
from gtts import gTTS
from helpers import decor
from helpers import INIT as init

@decor.stop_watch
def tts2mp3(arg_list: list | None = init.seperated_list, 
            arg_lang: str | None = init.tts_lang, 
            auto_concat: bool | None = init.auto_concat,
            arg_path: str | None = init.inter_audio_path, 
            arg_subject: str | None = init.subject,
            arg_cols: list | None = init.columns):
    '''
    Make mp3 file using tts
    @ Args:
        arg_list:
            list of seperated dictionaries, max word is set by user-option
        arg_lang:
            language option for tts, set by user-option
        auto_concat:
            T/F option for concatenate audio files of word and sentece
        arg_path:
            path of output audio file
        arg_subject:
            set target subject to select audio file
        arg_cols:
            list of columns about data
    '''
    file_path = arg_path + 'words/' + arg_subject + '/'
    for j in range(len(arg_list)):
        TARGET_WORDS = arg_list[j]
        df = pd.DataFrame(TARGET_WORDS, columns=arg_cols)

        for i in range(len(TARGET_WORDS)):
            word = df[i:i+1]['word'].values[0]
            meaning = df[i:i+1]['meaning'].values[0]
            sentence = df[i:i+1]['sentence'].values[0]

            tts_word = gTTS(text=word, lang=arg_lang)
            tts_sentence = gTTS(text=sentence, lang=arg_lang)

            if auto_concat == True:
                concat_file = file_path + word + '_concat.mp3'
                f = open(file=concat_file, mode='wb')
                tts_word.write_to_fp(f)
                tts_sentence.write_to_fp(f)
                f.close()
                print('[SAVED] Audio file(concat):', concat_file)
            
            elif auto_concat == False:
                word_file = file_path + word + '_word.mp3'
                tts_word.save(word_file)
                print('[SAVED] Audio file(Word):', word_file)

                sent_file = file_path + word + '_sent.mp3'
                tts_sentence.save(sent_file)
                print('[SAVED] Audio file(Sentence):', sent_file)