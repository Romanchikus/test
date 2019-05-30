import os
import xml.etree.ElementTree as ET
import json
from textblob import TextBlob
import pydub
from google.cloud.speech import types
from google.cloud import speech , translate
from google.cloud.speech import enums
import traceback
# import nltk
# nltk.edit_distance("humpty", "dumpty")
import dialogflow_v2 as dialogflow
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="/home/roma/speech/small-talk-8f559-d0fe6cb9de3b.json"
project_id = 'small-talk-8f559'
session_id = "BatlabAIBot"
language_code = 'ru'

def detect_intent_texts(project_id, session_id, texts, language_code):
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
                type(response.query_result.fulfillment_text)))
        # if response.query_result.parameters.fields["lastName"]:
    
    try:
        lastName=response.query_result.parameters.fields["lastName"].string_value
        print(lastName)
    except Exception as err:
        print('Ошибка:\n', traceback.format_exc())  
    
    return str(response.query_result.fulfillment_text)

send=True
weathercity = "Kiev"
country="00"
tree = ET.parse('/home/roma/speech/set.xml')
root = tree.getroot()
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="/home/roma/speech/speechtotext-2bc1c0b4dc68.json"
def truemess(update):
    global country
    global send
    texts= update
    language_code = 'ru'
    response = detect_intent_texts(project_id, session_id, texts, language_code)# Разбираем JSON и вытаскиваем ответ
    stry=response.query_result.fulfillment_text
    boo=response.query_result.diagnostic_info.fields["end_conversation"].bool_value
    firstName=response.query_result.parameters.fields["firstName"].string_value
    lastName=response.query_result.parameters.fields["lastName"].string_value
    fulf=response.query_result.fulfillment_text

    # if response== "Повторите имя":
        # request = apiai.ApiAI('f1470498e503467fa0199d2af6052762').text_request() # Токен API к Dialogflow
        # request.lang = 'ru' # На каком языке будет послан запрос
        # request.session_id = 'BatlabAIBot' # ID Сессии диалога (нужно, чтобы потом учить бота)
        # request.query = 'Рома' # Посылаем запрос к ИИ с сообщением от юзера
        # responseJson = json.loads(request.getresponse().read().decode('utf-8'))
        # response = responseJson['result']['fulfillment']['speech']
        # return response

    if fulf== "About":
        print(city)
        text = trans(city,"en")
        text = TextBlob(text)
        for words, tag in text.tags:
            if tag == "NN":
                print(words)
                synset=wordnet.synsets(words)
                tran=trans(synset[0].definition(),"ru")
                return str(tran)
                send = False
            else:
                send = True

    elif fulf:
        if send==True:
            return str(fulf)

    else:
        if send==True:
            return str("result")
    send = True

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

def create_entity(project_id, entity_type_id, entity_value, synonyms):
    """Create an entity of the given entity type."""
    entity_types_client = dialogflow.EntityTypesClient()

    # Note: synonyms must be exactly [entity_value] if the
    # entity_type's kind is KIND_LIST
    synonyms = synonyms or [entity_value]

    entity_type_path = entity_types_client.entity_type_path(
        project_id, entity_type_id)

    entity = dialogflow.types.EntityType.Entity()
    entity.value = entity_value
    entity.synonyms.extend(synonyms)

    response = entity_types_client.batch_create_entities(
        entity_type_path, [entity])

    print('Entity created: {}'.format(response))