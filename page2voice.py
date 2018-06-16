# encoding:utf-8

import uuid
import re
import os
import argparse
from pydub import AudioSegment
from aip import AipSpeech
from playsound import playsound
from goose3 import Goose
from goose3.text import StopWordsChinese

""" 你的 百度 APPID AK SK """
APP_ID = 'xx'
API_KEY = 'xx'
SECRET_KEY = 'xx'

# 命令行输入参数处理
parser = argparse.ArgumentParser()
parser.add_argument('-u', '--url', type=str, help="input the target url")

# 获取参数
args = parser.parse_args()
URL = args.url

client = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

def text_to_voice(text):
    file_name = str(uuid.uuid1()) + '.mp3'
    result = client.synthesis(text, 'zh', 3, {
        'vol': 5,
    })

    # 识别正确返回语音二进制 错误则返回 dict 参照下面错误码
    if not isinstance(result, dict):
        with open(file_name, 'wb+') as f:
            f.write(result)
    return file_name

def get_text(url):
    g = Goose({'stopwords_class': StopWordsChinese})
    article = g.extract(url=url)
    return article.cleaned_text

# 合并音频文件
def merge_voice(file_list):
    voice_dict = {}
    song = None
    for i,f in enumerate(file_list):
        if i == 0:
            song = AudioSegment.from_file(f,"mp3")
        else:
            # 拼接音频文件
            song += AudioSegment.from_file(f,"mp3")
        # 删除临时音频
        os.unlink(f)
 
    # 导出合并后的音频文件，格式为MP3格式
    file_name = str(uuid.uuid1()) + ".mp3"
    song.export(file_name, format="mp3")
    return file_name

if __name__ == "__main__":
    # url = "http://news.china.com/socialgd/10000169/20180616/32537640_all.html"
    text = get_text(URL)

    # 将文本按 500 的长度分割成多个文本
    text_list = [text[i:i+500] for i in range(0, len(text), 500)]
    file_list = []
    for t in text_list:
        file_list.append(text_to_voice(t))
    # print(file_list)
    final_voice = merge_voice(file_list)
    print(final_voice)
    # 播放音频
    playsound(final_voice)
