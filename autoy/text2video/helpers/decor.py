'''
Decorator for recording process time
'''
import time

def stop_watch(func):
    def wrapper():
        # str = time.time()
        # func()
        # end = time.time()
        if func.__name__ == 'tts2mp3':
            print('[START] Making audio files.')
            str = time.time()
            func()
            end = time.time()
            print('=================================================')
            print("[RECORD] TTS process time:", end - str, "s")
            print('[COMPLETE] Every audio file is ready.')
            print('=================================================\n\n')
        elif func.__name__ == 'make_inter_video':
            print('\n[START] Making video files.')
            str = time.time()
            func()
            end = time.time()
            print('=================================================')
            print("[RECORD] T2V process time:", end - str, "s")
            print("[COMPLETE] Every video is ready.")
            print('=================================================\n\n')
        elif func.__name__ == 'make_output':
            print('[START] Making final output files.')
            str = time.time()
            func()
            end = time.time()
            print('=================================================')
            print("[RECORD] Composer process time:", end - str, "s")
            print("[COMPLETE] Final output is ready.")
            print('=================================================\n\n')
    return wrapper

    

