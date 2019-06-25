import os
import xml.etree.ElementTree as ET
import json
from textblob import TextBlob
import pydub
from google.cloud.speech import types
from google.cloud import speech , translate
from google.cloud.speech import enums
import traceback
from time import sleep

# import nltk
# nltk.edit_distance("humpty", "dumpty")
import dialogflow_v2 as dialogflow
f="/home/roma/speech/Small-Talk-769554f11f51.json"
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]=f
project_id = 'small-talk-8f559'
session_id = "BatlabAIBot"
language_code = 'ru'

def truemess(update,language_code):
    
    response = detect_intent_texts(project_id, session_id, update,language_code)
    firstName=response.query_result.parameters.fields["firstName"].string_value
    lastName=response.query_result.parameters.fields["lastName"].string_value
    # date=response.query_result.parameters.fields["date"].string_value

    fulf=response.query_result.fulfillment_text
    print("first:",firstName, "lastName:", lastName)
    # print(response)
    print("update:",update)
    if firstName or lastName:
        return dict(firstName=firstName, lastName=lastName, query = update)
    else:
        return dict(firstName="None", lastName="None",query = "None")


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


def detect_intent_texts(project_id, session_id, texts, language_code):
    session_client = dialogflow.SessionsClient()
    
    session = session_client.session_path(project_id, session_id)
    text_input = dialogflow.types.TextInput(
        text=texts, language_code=language_code)

    query_input = dialogflow.types.QueryInput(text=text_input)

    response = session_client.detect_intent(
        session=session, query_input=query_input)

    # print('=' * 20)

    if response.query_result.fulfillment_text:
        print('Fulfillment text: {}\n'.format(
            response.query_result.fulfillment_text))

    
    try:
        # print(response.query_result.parameters.fields["lastName"].string_value)
        # print(response.query_result.parameters.fields["firstName"].string_value)
        return response
    except Exception as err:
        print('Ошибка:\n', traceback.format_exc())  
