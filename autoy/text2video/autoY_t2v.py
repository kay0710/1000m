'''
example of making contents
- option
    - youtube shorts form
    - english words (47)
- outputs
    - visit below link and see the outputs of this example
    - https://youtube.com/@cantalk247
'''
import time
from helpers import tts, composer
from helpers.t2v import T2V

print("\n============================================")
print("===== Let's make contents with autoY :) =====")
print("=============================================")
start = time.time()

# make audio file
tts.tts2mp3()

# make video file
T2V.make_inter_video()

# make finale output file
composer.make_output()

end = time.time()
print("Total pregress time:", end - start, "s")
print("\n=========================================")
print("===== Enjoy your output :) (from.K) =====")
print("=========================================")