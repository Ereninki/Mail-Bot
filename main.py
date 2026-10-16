import os
from dotenv import load_dotenv
load_dotenv()
import requests

from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

app = App(token=os.getenv("SLACK_BOT_TOKEN"))

@app.command("/my-mail-ids")
def health(ack, respond, command):
    ack()

    if command["text"].strip() == "":
        respond("you didnt give me any api keys :hs:")
        return

    headers = {
        "Authorization": f"Bearer {command["text"].strip()}"
    }

    try:
        raw_mail_response = requests.get("https://mail.hackclub.com/api/public/v1/mail", headers=headers)
        raw_mail_response.raise_for_status()
    except Exception as e:
        respond(f"sorry but there's a problem, error: {e}", response_type="ephemeral")

    cooked_mail_response = raw_mail_response.json()
    
    ids = []
    for a in cooked_mail_response["mail"]:
        ids.append(a["id"])

    blocks = [
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": "Your Mail IDS",
                "emoji": True,
            },
        },
        {
            "type": "divider"
        },
        {
            "type": "section",
            "fields": [
                {
                    "type": "mrkdwn",
                    "text": "\n ".join(ids)
                }
            ]
        }
    ]

    respond(blocks=blocks, response_type="ephemeral")

if __name__ == "__main__":
    handler = SocketModeHandler(app, os.getenv("SLACK_APP_TOKEN"))
    handler.start()
