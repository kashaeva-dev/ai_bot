import argparse
import json

from environs import Env
from google.cloud import dialogflow


def get_df_answer(project_id, session_id, text, language_code):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)
    text_input = dialogflow.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)

    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input},
    )

    return response.query_result


def create_intent(project_id, display_name, training_phrases_parts, message_texts):
    intents_client = dialogflow.IntentsClient()

    parent = dialogflow.AgentsClient.agent_path(project_id)
    training_phrases = []
    for training_phrases_part in training_phrases_parts:
        part = dialogflow.Intent.TrainingPhrase.Part(text=training_phrases_part)
        training_phrase = dialogflow.Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)

    text = dialogflow.Intent.Message.Text(text=message_texts)
    message = dialogflow.Intent.Message(text=text)

    intent = dialogflow.Intent(
        display_name=display_name, training_phrases=training_phrases, messages=[message],
    )

    response = intents_client.create_intent(
        request={"parent": parent, "intent": intent},
    )

    print("Intent created: {}".format(response))


def create_parser():
    parser = argparse.ArgumentParser(
        prog="Create DialogFlow intents from json file",
    )
    parser.add_argument("filepath",
                        nargs="?",
                        help="You can spesify filepath to the intents' data in json format",
                        default="../intents.json",
                        )

    return parser


if __name__ == '__main__':
    env = Env()
    env.read_env()

    df_project_id = env('DF_PROJECT_ID')
    parser = create_parser()
    args = parser.parse_args()
    with open(args.filepath, 'r') as intents_file:
        intents = intents_file.read()

    intents = json.loads(intents)

    for intent_header, intent_body in intents.items():
        create_intent(df_project_id,
                      intent_header,
                      intent_body['questions'],
                      [intent_body['answer']],
                      )
