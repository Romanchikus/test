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
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="/home/roma/speech/small-talk-8f559-055dcd826823.json"
project_id = 'small-talk-8f559'
session_id = "BatlabAIBot"
language_code = 'ru'
send=True
name=""
what_ask = ""
fulf = ""
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

def truemess(update):
    global send
    global name
    global what_ask
    global fulf
    upd=[str(update)]
    create_entity_type(project_id, "@test", 1)
    print("create_entity_type++++++++++++++++++++++++")
    # create_entity(project_id, "firstName", update, upd)
    create_entity(project_id, "@firstName", update, upd)
    
    if send == True and what_ask == update and fulf == "Повторіть ім'я":
        send = False
        name = update
        return str("Такого імені немає, додати "+update+"?")
    if send == False and update.lower() == "так":
        send = True
        create_entity(project_id, "firstName", name, name)
        return str("Збережено")
    what_ask = update
    print("+="*10)
    
    if send:
        response = detect_intent_texts(project_id, session_id, update, 'ru')# Разбираем JSON и вытаскиваем ответ
        # print(response)
        boo=response.query_result.diagnostic_info.fields["end_conversation"].bool_value
        firstName=response.query_result.parameters.fields["firstName"].string_value
        lastName=response.query_result.parameters.fields["lastName"].string_value
        fulf=response.query_result.fulfillment_text
        query_text = response.query_result.query_text
        
        if fulf:
            if send==True:
                return str(fulf)
        else:
            if send==True:
                return str("result")
        

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

def create_entity_type(project_id, display_name, kind):
    """Create an entity type with the given display name."""
    import dialogflow_v2 as dialogflow
    entity_types_client = dialogflow.EntityTypesClient()

    parent = entity_types_client.project_agent_path(project_id)
    entity_type = dialogflow.types.EntityType(
        display_name=display_name, kind=kind)

    response = entity_types_client.create_entity_type(parent, entity_type)

    print('Entity type created: \n{}'.format(response))

