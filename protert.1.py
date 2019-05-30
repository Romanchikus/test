from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import json
import pyowm
import os
import xml.etree.ElementTree as ET
from textblob import TextBlob
import nltk
from itertools import chain
from nltk.corpus import wordnet
import io
from gtts import gTTS
import pydub
from google.cloud.speech import types
from google.cloud import speech , translate
from google.cloud.speech import enums
from pydub import AudioSegment
from pydub.playback import play
import traceback
# nltk.download('averaged_perceptron_tagger')
import dialogflow_v2 as dialogflow
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="/home/roma/speech/small-talk-8f559-d0fe6cb9de3b.json"
project_id = 'small-talk-8f559'
session_id = "BatlabAIBot"
language_code = 'ru'
country= True 
sends = True



def detect_intent_texts(project_id, session_id, texts, language_code):
    """Returns the result of detect intent with texts as inputs.
    
    Using the same `session_id` between requests allows continuation
    of the conversation."""
    session_client = dialogflow.SessionsClient()
    
    session = session_client.session_path(project_id, session_id)
    print('Session path: {}\n'.format(session))
    texts=["Пусть вика сагайдачный уберёт в комнате завтра", "вика", "сагайдачный"]   
    for text in texts:
        text_input = dialogflow.types.TextInput(
            text=text, language_code=language_code)

        query_input = dialogflow.types.QueryInput(text=text_input)

        response = session_client.detect_intent(
            session=session, query_input=query_input)

        print('=' * 20)
        print('Query text: {}'.format(response.query_result.query_text))
        # print('Detected intent: {} (confidence: {})\n'.format(
        #     response.query_result.intent_detection_confidence,
        #     response.query_result.intent_detection_confidence))
        if response.query_result.fulfillment_text:
            print('Fulfillment text: {}\n'.format(
                response.query_result.fulfillment_text))
        # if response.query_result.parameters.fields["lastName"]:
    
    try:
        lastName=response.query_result.parameters.fields["lastName"].string_value
        print(lastName)
    except Exception as err:
        print('Ошибка:\n', traceback.format_exc())  
    

    return response
send=True
weathercity = "Kiev"
country="00"
tree = ET.parse('/home/roma/speech/set.xml')
root = tree.getroot()


updater = Updater(token='875809845:AAHxB49VM_TowQhXtaBz80fx07XrIvgcHIc') # Токен API к Telegram
dispatcher = updater.dispatcher

# Обработка команд
def startCommand(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text='Привет, давай пообщаемся?')


def textMessage(bot, update):
    global country
    global send
    # if country == "00":
    texts= update.message.text
    language_code = 'ru'
    response= detect_intent_texts(project_id, session_id, texts, language_code)# Разбираем JSON и вытаскиваем ответ
    stry=response.query_result.fulfillment_text
    bull=response.query_result.diagnostic_info.fields["end_conversation"].bool_value
    firstName=response.query_result.parameters.fields["firstName"].string_value
    lastName=response.query_result.parameters.fields["lastName"].string_value
    fulf=response.query_result.fulfillment_text

    if fulf ==  "Повторите имя":
        sends = False
        

    if send==True:
        bot.send_message(chat_id=update.message.chat_id, text=response)

    else:
        if send==True:
            bot.send_message(chat_id=update.message.chat_id, text='Я Вас не совсем понял!')
    send = True

def voice_handler(bot, update):
    global send     
    global country
    file = bot.getFile(update.message.voice.file_id)
    bot.send_message(chat_id=update.message.chat_id, text="Обробка голоса")
    blabla=Audio(file)
    blabla=trans(blabla,"ru")
    if country == "00":
        request = apiai.ApiAI('f1470498e503467fa0199d2af6052762').text_request() # Токен API к Dialogflow
        request.lang = 'ru' # На каком языке будет послан запрос
        request.session_id = 'BatlabAIBot' # ID Сессии диалога (нужно, чтобы потом учить бота)
        request.query = blabla # Посылаем запрос к ИИ с сообщением от юзера
        responseJson = json.loads(request.getresponse().read().decode('utf-8'))
        response = responseJson['result']['fulfillment']['speech']
        city = responseJson['result']['resolvedQuery']
        result=responseJson['result']
    else:   
        try:
            send=False
            blabla=str(blabla).title()
            city = trans(blabla,"en")
            bot.send_message(chat_id=update.message.chat_id, text=weather(city,country))
            country = "00"

        except Exception :
            bot.send_message(chat_id=update.message.chat_id, text="Помилка правопису")
        send=False

    if response == "taxi":
        bot.send_message(chat_id=update.message.chat_id, text=(city,result))
        send = False

    if response== "About":
        print(city)
        text = trans(city,"en")
        text = TextBlob(text)
        for words, tag in text.tags:
            if tag == "NN":
                try:
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
        send=False

    if response =="Task":

        bot.send_message(chat_id=update.message.chat_id, text=(city,result))

        send = False

    if response == "_-_":
        country=trans(responseJson['result']['parameters']['geo-country'],"ru")
        bot.send_message(chat_id=update.message.chat_id, text="***Обробка***")
        country= ua(country)
        bot.send_message(chat_id=update.message.chat_id, text="Скажіть назву міста!")
        send = False

    if response:
        if send ==True:
            blabla=trans(response,"uk")
            tts = gTTS(text=blabla, lang='uk')
            tts.save("/home/roma/speech/test.mp3")
            # bot.send_message(chat_id=update.message.chat_id, text=blabla)
            bot.send_audio(chat_id=update.message.chat_id, audio=open('/home/roma/speech/test.mp3', 'rb'))
    else:
        if send==True:
            blabla="Вибачте, не зрозуміла Вас!"
            tts = gTTS(text=blabla, lang='uk')
            tts.save("/home/roma/speech/test.mp3")
            # bot.send_message(chat_id=update.message.chat_id, text=blabla)
            bot.send_audio(chat_id=update.message.chat_id, audio=open('/home/roma/speech/test.mp3', 'rb'))
    send = True



def weather(city,country):
    owm = pyowm.OWM(language='ru')
    owm = pyowm.OWM('e5d6daaae4ad1b7f275cbab1a80af042')
    try:
        city=str(str(city)+","+country)
        observation = owm.weather_at_place(city)
        w = observation.get_weather()
        temp = w.get_temperature(unit='celsius')["temp"]
        return str(temp)+" °C"+ " у місті "+city
    except Exception :
        return "Vведіть містo!"

def ua(t):
    summ = 0
    for element in root.iter("country"):
        summ=summ+1
        for child in element:
            if child.text == t :
                i=summ

    return root[i][3].text.lower()

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

def Audio(file):
    file.download('voice.ogg')
    
    song = AudioSegment.from_ogg("voice.ogg")
    song.export("voice.flac",format = "flac")
    sound = AudioSegment.from_file("voice.flac", format="flac")
    
    client = speech.SpeechClient()
    file_name = os.path.join(
        os.path.dirname(__file__),
        '/home/roma/speech/',
        'voice.flac')

    # Loads the audio into memory
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
    return blabla
dispatcher.add_handler(MessageHandler(Filters.voice, voice_handler))
print('start')
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
