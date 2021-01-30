"""
URL: t.me/ukr_stt2_bot
"""

import warnings

warnings.simplefilter('ignore')

import wave
import os
import logging
import ffmpeg
import json

from os import remove

import telebot
from uuid import uuid4
from vosk import Model, KaldiRecognizer

TOKEN = os.environ['TOKEN']

if not TOKEN:
    print('You must set the TOKEN environment variable')
    exit(1)

START_MSG = '''Вітання!

Цей бот створений для тестування перекладу українських аудіозаписів в текст.

Двигун - VOSK.

Група для обговорення: https://t.me/speech_recognition_uk'''

FIRST_STEP = '''Використовувати бота просто: надішліть аудіоповідомлення і чекайте відповіді'''

CHUNK = 1024 * 4
MODEL_PATH = os.getcwd() + '/model'
RATE = 8000 * 2
rec = KaldiRecognizer(Model(MODEL_PATH), RATE)

bot = telebot.TeleBot(TOKEN, parse_mode=None)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, START_MSG)
    bot.reply_to(message, FIRST_STEP)


@bot.message_handler(content_types=['voice'])
def process_voice_message(message):
    # download the recording
    file_info = bot.get_file(message.voice.file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    # save the recording on the disk
    uuid = uuid4()
    filename = os.getcwd() + f'/recordings/{uuid}.ogg'
    with open(filename, 'wb') as f:
        f.write(downloaded_file)

    # convert OGG to WAV
    wav_filename = os.getcwd() + f'/recordings/{uuid}.wav'
    _, err = (
        ffmpeg
            .input(filename)
            .output(wav_filename, acodec='pcm_s16le', ac=1, ar='16k')
            .overwrite_output()
            .run(capture_stdout=False)
    )
    if err is not None:
        bot.reply_to(message, 'Помилка...')
        return

    # do the recognition
    wf = wave.open(wav_filename, 'rb')

    data = wf.readframes(CHUNK)

    while len(data) > 0:
        data = wf.readframes(CHUNK)
        rec.AcceptWaveform(data)

    # Close the file
    wf.close()

    # Process the result
    result = json.loads(rec.FinalResult())

    if 'text' in result:
        if not result['text']:
            # no results
            bot.reply_to(message, 'Я не зміг розпізнати 😢')
        else:
            # send the recognized text
            bot.reply_to(message, result['text'])
    else:
        # no results
        bot.reply_to(message, 'Я не зміг розпізнати 😢')

    # remove the original recording
    remove(filename)

    # remove WAV file
    remove(wav_filename)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)

    bot.polling()
