from google.cloud import dialogflow


def detect_intent_texts(project_id, session_id, text, language_code):
    """Returns the result of detect intent with texts as inputs.

    Using the same `session_id` between requests allows continuation
    of the conversation."""

    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)
    print("Session path: {}\n".format(session))

    text_input = dialogflow.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)

    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )

    output = f'{"=" * 20}\n' \
             f'Query text: {response.query_result.query_text}\n' \
             f'Detected intent: {response.query_result.intent.display_name}' \
             f' (confidence: {response.query_result.intent_detection_confidence})\n' \
             f'Fulfillment text: {response.query_result.fulfillment_text}'

    print(output)


def get_df_answer(project_id, session_id, text, language_code):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)
    text_input = dialogflow.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)

    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )

    return response.query_result.fulfillment_text

if __name__ == 'main':
    detect_intent_texts("ai-devman-bot", "123456789", "Тук-тук", "ru")
