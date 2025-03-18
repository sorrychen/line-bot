from flask import Flask, request, abort

from linebot.v3 import (
    WebhookHandler
)
from linebot.v3.exceptions import (
    InvalidSignatureError
)
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage
)
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent
)
import os
from dotenv import load_dotenv
from openai import OpenAI
from gpt_funcs import create_assistant, create_thread, add_user_message_to_thread, wait_for_assistant_run, update_assistant

load_dotenv()

client = OpenAI(api_key=os.getenv("LINE_BOT_API_KEY"))

CHANNEL_ACCESS_TOKEN = os.getenv("CHANNEL_ACCESS_TOKEN")  
CHANNEL_SECRET = os.getenv("CHANNEL_SECRET")  


assistant_id = create_assistant(client)
# assistant_id = "xxxxxxx" 可以寫死
thread_id = create_thread(client)
# thread_id = "xxxxxx"
update_assistant(client, assistant_id)

app = Flask(__name__)

configuration = Configuration(access_token=CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)


@app.route("/", methods=["POST"])
def callback():
    # get X-Line-Signature header value
    signature = request.headers["X-Line-Signature"]

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        app.logger.info("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return "OK"


# def use_gpt(user_message):
#     completion = client.chat.completions.create(
#         model="gpt-4o",
#         messages=[
#             {"role": "system", "content": "You are a helpful cafe assistant.我們的類別有: 咖啡飲品 其他飲品 餐點 甜點 特調" + menu},
#             {"role": "user", "content": user_message},
#         ]
#     )
#     gpt_response = completion.choices[0].message.content
#     return gpt_response


@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    user_message = event.message.text
    add_user_message_to_thread(client, thread_id, user_message)
    assistant_r = wait_for_assistant_run(client, thread_id, assistant_id)

    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text = assistant_r)],
            )
        )


if __name__ == "__main__":
    app.run()
