import telebot


import os
import time
import validators
from dotenv import load_dotenv


from utils import generate_keyboard_buttons, main_buttons, get_videos_by_keyword, extract_audio_from_yt_video

load_dotenv()

SECRET_ID = os.getenv('BOT_ID')
bot = telebot.TeleBot(SECRET_ID)
bot_messages = []


@bot.message_handler(commands=['start'])
def start(info):

    bot.send_message(info.chat.id, f'Привет, {info.from_user.first_name} {info.from_user.last_name}', reply_markup=generate_keyboard_buttons(main_buttons))
    bot.register_next_step_handler(info, post_keybord_buttons)


def post_keybord_buttons(сallback):
    if сallback.text == 'Найти песню в youtube🎵':
        bot.send_message(сallback.chat.id, 'Напишите название видео и ее исполнителя/исполнительницу🎤')
        bot.register_next_step_handler(сallback, get_name_for_song)


def get_name_for_song(message):
    global bot_messages
    song_name = message.text
    videos = get_videos_by_keyword(song_name)
    counter = 0
    for video in videos:
        counter += 1
        title_msg = bot.send_message(message.chat.id, f"Видео номер {counter}, Название: {video.title}:")
        title_msg_id = title_msg.message_id
        video_msg = bot.send_message(message.chat.id, video.watch_url)
        video_msg_id = video_msg.message_id
        bot_messages.append(title_msg_id)
        bot_messages.append(video_msg_id)
        time.sleep(2)
        if counter == 5:
            break
    bot.send_message(message.chat.id, 'Выберите песню которую вы хотите сохранить(ответье на ссылку с видео, написав любой текст)')
    bot.register_next_step_handler(message, analyze_results)


@bot.message_handler(func=lambda message: message.reply_to_message and message.reply_to_message.message_id in bot_messages)
def analyze_results(message):
    global bot_messages
    chat_id = message.chat.id

    if not message.reply_to_message:
        bot.send_message(chat_id, "Пожалуйста, выберите видео.")
        bot.register_next_step_handler(message, analyze_results)
        return
    else:
        selected_message_id = message.reply_to_message.message_id
        selected_message = str(message.reply_to_message.text)
        print(selected_message)
    
    if not validators.url(selected_message):
        bot.send_message(chat_id, "Пожалуйста, выберите видео.")
        bot.register_next_step_handler(message, analyze_results)
        return
    
    audio_file = extract_audio_from_yt_video(selected_message)
    
    for msg_id in bot_messages:
        if msg_id != selected_message_id:
            bot.delete_message(chat_id, msg_id)
    
    bot_messages = [selected_message_id]
    bot.send_audio(chat_id, audio=open(audio_file, 'rb'))
    time.sleep(2)
    os.remove(audio_file)
    bot.register_next_step_handler(message, post_keybord_buttons)


bot.polling(none_stop=True)