from telebot import types

from pytube import Search
from pytube import YouTube

import os


# создаем клавиатурные кнопки
main_buttons = {
    "Найти песню в youtube🎵": 'new_post'
}
def generate_keyboard_buttons(btns_dict):
    keyboard = types.ReplyKeyboardMarkup(row_width=2)
    btns = list(btns_dict.keys())
    for i in range(0, len(btns), 2):
        if i + 1 < len(btns):
            keyboard.add(btns[i], btns[i+1])
        else:
            keyboard.add(btns[i])
    return keyboard


# Функция которая возвращает видео из ютуба по keyword
def get_videos_by_keyword(keyword: str):
    s = Search(keyword)
    videos = s.results
    return videos


def extract_audio_from_yt_video(video_link: str):
    yt = YouTube(video_link)
    name = f'./audios/{yt.streams[0].title}.mp3'
    yt.streams.filter(only_audio=True).first().download(filename=name)
    return name