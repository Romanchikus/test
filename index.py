
import io
import json
# import pyowm
import os
from gtts import gTTS
import apiai
import pydub
from google.cloud.speech import types
from google.cloud import speech , translate
from google.cloud.speech import enums
from pydub import AudioSegment
from pydub.playback import play
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater
from textblob import TextBlob
import nltk
# nltk.download('averaged_perceptron_tagger')
# nltk.download()
from itertools import chain
from nltk.corpus import wordnet
res=True

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="/home/roma/speech/speechtotext-2bc1c0b4dc68.json"
updater = Updater(token='875809845:AAHxB49VM_TowQhXtaBz80fx07XrIvgcHIc') # Токен API к Telegram
dispatcher = updater.dispatcher

def startCommand(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text='Привет, давай пообщаемся?')
def textMessage(bot, update):

    request = apiai.ApiAI('f1470498e503467fa0199d2af6052762').text_request() # Токен API к Dialogflow
    request.lang = 'ru' # На каком языке будет послан запрос
    request.session_id = 'BatlabAIBot' # ID Сессии диалога (нужно, чтобы потом учить бота)
    request.query = update.message.text # Посылаем запрос к ИИ с сообщением от юзера
    responseJson = json.loads(request.getresponse().read().decode('utf-8'))
    response = responseJson['result']['fulfillment']['speech'] # Разбираем JSON и вытаскиваем ответ
    print()
    
    if response:
        # bot.send_message(chat_id=update.message.chat_id, text=response)
        blabla=trans(response,"uk")
        tts = gTTS(text=blabla, lang='uk')
        tts.save("/home/roma/speech/test.mp3")
        # bot.send_message(chat_id=update.message.chat_id, text=blabla)
        bot.send_audio(chat_id=update.message.chat_id, audio=open('/home/roma/speech/test.mp3', 'rb'))
    
    else:
        bot.send_message(chat_id=update.message.chat_id, text='Я Вас не совсем понял!')
def trans(city,lan):
    
    # Instantiates a client
    translate_client = translate.Client()
    # The text to translate
    text = city
    # The target language
    target = lan

    # Translates some text into Russian
    translation = translate_client.translate(
        text,
        target_language=target)
    
    print(u'Translation: {}'.format(translation['translatedText']))
    return translation['translatedText']

def voice_handler(bot, update):
    global res
    file = bot.getFile(update.message.voice.file_id)
    print ("file_id: " + str(update.message.voice.file_id))
    file.download('voice.ogg')
    bot.send_message(chat_id=update.message.chat_id, text="Обробка голоса")
    song = AudioSegment.from_ogg("voice.ogg")
    song.export("voice.flac",format = "flac")
    sound = AudioSegment.from_file("voice.flac", format="flac")
    
    client = speech.SpeechClient()
    file_name = os.path.join(
        os.path.dirname(__file__),
        '/home/roma/speech/',
        'voice.flac')

    # Loads the audio into memory
    from google.cloud.speech import types
    with io.open(file_name, 'rb') as audio_file:
        content = audio_file.read()
        audio = types.RecognitionAudio(content=content)
    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.FLAC,
        sample_rate_hertz=48000,
        language_code='uk-UA')
    response = client.recognize(config, audio)
    # if response:
    #     play(sound)
    for result in response.results:
        blabla=('{}'.format(result.alternatives[0].transcript))
    
    blabla=trans(blabla,"ru")
    request = apiai.ApiAI('f1470498e503467fa0199d2af6052762').text_request() # Токен API к Dialogflow
    request.lang = 'ru' # На каком языке будет послан запрос
    request.session_id = 'BatlabAIBot' # ID Сессии диалога (нужно, чтобы потом учить бота)
    request.query = blabla # Посылаем запрос к ИИ с сообщением от юзера
    responseJson = json.loads(request.getresponse().read().decode('utf-8'))
    response = responseJson['result']['fulfillment']['speech']
    city = responseJson['result']['resolvedQuery']
    if response== "About":
        print(city)
        text = trans(city,"en")
        text = TextBlob(text)
        
        for words, tag in text.tags:
            if tag == "NN":
                try:
                    print(text)
                    synset=wordnet.synsets(words)
                    print(synset[0].definition())
                    tran=trans(synset[0].definition(),"uk")
                    tts = gTTS(text=tran, lang='uk')
                    tts.save("/home/roma/speech/test.mp3")
                    bot.send_audio(chat_id=update.message.chat_id, audio=open('/home/roma/speech/test.mp3', 'rb'))
                except Exception :
                    bot.send_message(chat_id=update.message.chat_id, text="Повідомьте розробника про помилку")
                finally:
                    bot.send_message(chat_id=update.message.chat_id, text="Розпізнавання закінчено")
                      
        res=False
        

    if response =="Task":
        bot.send_message(chat_id=update.message.chat_id, text=responseJson['result'])
        res = False

    if res ==True:
        blabla=trans(response,"uk")
        tts = gTTS(text=blabla, lang='uk')
        tts.save("/home/roma/speech/test.mp3")
        # bot.send_message(chat_id=update.message.chat_id, text=blabla)
        bot.send_audio(chat_id=update.message.chat_id, audio=open('/home/roma/speech/test.mp3', 'rb'))
    res = True


dispatcher.add_handler(MessageHandler(Filters.voice, voice_handler))

# Хендлеры
start_command_handler = CommandHandler('start', startCommand)
text_message_handler = MessageHandler(Filters.text, textMessage)
# Добавляем хендлеры в диспетчер
dispatcher.add_handler(start_command_handler)
dispatcher.add_handler(text_message_handler)
# Начинаем поиск обновлений
updater.start_polling(clean=True)
# Останавливаем бота, если были нажаты Ctrl + C
updater.idle()
