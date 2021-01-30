# Telegram Bot: Speech-to-Text for the Ukrainian language based on VOSK

This is a repository with demonstration code that uses [the VOSK Model for Ukrainian](https://drive.google.com/file/d/1MdlN3JWUe8bpCR9A0irEr-Icc1WiPgZs/view?usp=sharing) 
in the task of Speech-to-Text recognition.

### How to run

Download model from this URL: https://drive.google.com/file/d/1MdlN3JWUe8bpCR9A0irEr-Icc1WiPgZs/view?usp=sharing (you can also check it out for newer versions here: https://github.com/egorsmkv/speech-recognition-uk)

Unpack the archive into the `model` folder.

Install dependencies and enter the python environment:

```
pipenv install
pipenv shell
```

Run the bot:

```
export TOKEN="...."
python bot.py
```
