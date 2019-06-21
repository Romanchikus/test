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
send=True
name=""
what_ask = ""
fulf = ""
surname =""
def truemess(update):
    global send
    global name
    global what_ask
    global fulf
    global surname
    
    if send:
        fulf = dialog(project_id, session_id, update)

    if send == True and what_ask == "Повторіть ім'я" and fulf == "Повторіть ім'я":
        send = False
        name = update
        return str("Такого імені немає, додати "+update+"?")
    if what_ask == "Повторіть ім'я" and update.lower() == "так":
        send = True
        upd=[name]
        create_entity(project_id, "2e0391b0-0acc-4667-b9a9-a805d942ae80", name, upd)
        # sleep(3.55)
        fulf = dialog(project_id, session_id, name)
        return str("Збережено ім'я. || "+fulf)
    if send == False and what_ask == "Повторіть ім'я":
        send = True
        fulf = dialog(project_id, session_id, update)
        return str("Не збережено ім'я. || "+fulf)
    

    if send == True and what_ask == "Повторіть прізвище" and fulf == "Повторіть прізвище":
        send = False
        surname = update
        return str("Такого прізвище немає, додати "+update+"?")
    if what_ask == "Повторіть прізвище" and update.lower() == "так":
        send = True
        upd=[surname]
        create_entity(project_id, "2f27753e-97d6-4d10-ad12-36e816d85392", surname, upd)
        # sleep(3.55)
        fulf = dialog(project_id, session_id, surname)
        return str("Збережено прізвище. || "+fulf)
    if send == False and what_ask == "Повторіть прізвище":
        send = True
        fulf = dialog(project_id, session_id, update)


    what_ask = fulf
    if fulf:
        if send==True:
            return fulf
    else:
        if send==True:
            return str("result")
    # print("+="*10)


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

def create_entity_type(project_id, display_name, kind):
    """Create an entity type with the given display name."""
    import dialogflow_v2 as dialogflow
    entity_types_client = dialogflow.EntityTypesClient()

    parent = entity_types_client.project_agent_path(project_id)
    entity_type = dialogflow.types.EntityType(
        display_name=display_name, kind=kind)

    response = entity_types_client.create_entity_type(parent, entity_type)

    print('Entity type created: \n{}'.format(response))

def list_intents(project_id):
    import dialogflow_v2 as dialogflow
    intents_client = dialogflow.IntentsClient()

    parent = intents_client.project_agent_path(project_id)

    intents = intents_client.list_intents(parent)

    for intent in intents:
        print('=' * 20)
        print('Intent name: {}'.format(intent.name))
        print('Intent display_name: {}'.format(intent.display_name))
        print('Action: {}\n'.format(intent.action))
        print('Root followup intent: {}'.format(
            intent.root_followup_intent_name))
        print('Parent followup intent: {}\n'.format(
            intent.parent_followup_intent_name))

        print('Input contexts:')
        for input_context_name in intent.input_context_names:
            print('\tName: {}'.format(input_context_name))

        print('Output contexts:')
        for output_context in intent.output_contexts:
            print('\tName: {}'.format(output_context.name))

# list_entities(project_id)
def list_entities(project_id):
    client = dialogflow.EntityTypesClient()
    parent = client.project_agent_path(project_id)
    # Iterate over all results
    for element in client.list_entity_types(parent):
        # process element
        print(element)
    # Alternatively:
    # Iterate over results one page at a time
    # for page in client.list_entity_types(parent).pages:
    #     for element in page:
    #         # process element
    #         print(element)

# list_intents(project_id)
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

def dialog(project_id, session_id, update):
    response = detect_intent_texts(project_id, session_id, update, 'ru')# Разбираем JSON и вытаскиваем ответ
    # print(response)
    # boo=response.query_result.diagnostic_info.fields["end_conversation"].bool_value
    # firstName=response.query_result.parameters.fields["firstName"].string_value
    # lastName=response.query_result.parameters.fields["lastName"].string_value
    fulf=response.query_result.fulfillment_text
    # query_text = response.query_result.query_text
    return fulf

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
