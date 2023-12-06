import os, io, datetime
from PIL import Image
    
def get_fsize(fileNames, index):
    size_units = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    fpath = fileNames[0][index]
    img = fpath.split('/')[-1].split('.')[0]
    
    file_size = os.path.getsize(filename=fpath)
    import math
    if file_size == 0:
        fsize ='0 B'
    else:
        i = int(math.floor(math.log(file_size, 1024)))
        p = math.pow(1024, i)
        fsize = str(round(file_size / p, 2)) + ' ' + size_units[i]
    
    return img, fpath, fsize

def create_dir(path: str, 
               dir: str):
    date = datetime.datetime.now().strftime("%Y%m%d")
    BGRESULT_DIR = path + dir + "_" + date
    try:
        if not os.path.exists(BGRESULT_DIR):
            os.makedirs(BGRESULT_DIR)
            print(f"[SET] {BGRESULT_DIR} is created.")
        else:
            print(f"[SET] {BGRESULT_DIR} already exist.")
        return BGRESULT_DIR + '/'
    except OSError:
        print("[ERROR] Failed to create the directory.")
        
# translation
def trans_prompt(user_prompt: str, platform: str):
    if platform == 'google':
        from googletrans import Translator

        translator = Translator()
        trans_result = translator.translate(user_prompt, dest='en')
        print(f"[RESULT] Translation result: {trans_result.text}")
        return trans_result.text
        
    elif platform == 'naver':
        import urllib.request
        import json
        client_id = 'KmRmvBgM0vWWz3HajCcf'
        client_secret = 'A09alTjzKI'
        
        encText = urllib.parse.quote(user_prompt)
        data = "source=ko&target=en&text=" + encText
        url = "https://openapi.naver.com/v1/papago/n2mt"
        
        request = urllib.request.Request(url)
        request.add_header("X-Naver-Client-Id",client_id)
        request.add_header("X-Naver-Client-Secret",client_secret)
        
        response = urllib.request.urlopen(request, data=data.encode("utf-8"))
        rescode = response.getcode()
        if rescode==200 :
            response_body = response.read()
            result = response_body.decode('utf-8')
            d = json.loads(result)
            trans_result = d['message']['result']['translatedText']
            print(f"[RESULT] Translation result: {trans_result}")
        else:
            print("Error Code:" + rescode)
        return trans_result
    
# size check
def convert_size(file_path: str, category: str):
    file_size = os.path.getsize(filename=file_path)
    
    import math
    if file_size == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(file_size, 1024)))
    p = math.pow(1024, i)
    s = round(file_size / p, 2)
    
    if category == 'BG':
        if (i == 2 and s < 20) or i < 2:
            BG_SIZE_CHECK = True
            print("[CHECK] File size pass.")
        else:
            BG_SIZE_CHECK = False
            print("[WARNING] File size fail.")
    elif category == 'UP':
        if (i == 2 and s < 30) or i < 2:
            UP_SIZE_CHECK = True
            print("[CHECK] File size pass.")
        else:
            UP_SIZE_CHECK = False
            print("[WARNING] File size fail.")
    
    return "%s %s" % (s, size_name[i])

# set img_obj_arr
def img_to_byte_array(img: Image):
    imgByteArr = io.BytesIO()
    img.save(imgByteArr, format=img.format)
    imgByteArr = imgByteArr.getvalue()
    return imgByteArr

# load and check img
def load_img(input: str, category: str):
    img_resolution = Image.open(input).size
    
    if category == 'BG':
        if img_resolution[0] > 2048 and img_resolution[1] > 2048:
            print("[WARNING] Resolution fail.")
        else:
            print("[CHECK] Resolution pass.")
    elif category == 'UP':
        if img_resolution[0] > 2048 and img_resolution[1] > 2048:
            print("[WARNING] Resolution fail.")
        else:
            print("[CHECK] Resolution pass.")
            if img_resolution[0] > img_resolution[1]:
                img_resolution = (4096, 4096*(img_resolution[1]/img_resolution[0]))
            elif img_resolution[0] > img_resolution[1]:
                img_resolution = (4096*(img_resolution[0]/img_resolution[1]), 4096)
            else:
                img_resolution = (4096, 4096)
    else:
        print("[WARNING] Check the category name")
    
    img_name = input.split('/')[-1].split('.')[0]
    img_format = input.split('/')[-1].split('.')[-1]
    file_size = convert_size(input, category)
    print(f"[CHECK] Loaded image: {img_name}, {img_format}, {img_resolution}, {file_size}")
   
    with Image.open(input) as input:
        image_file_object = img_to_byte_array(input)
    
    return img_name, img_resolution, image_file_object