from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

import robocorp.vault as vault

CHANNEL_NAME = "robotflashscoreproject"

def credentials():
    vault_secret = vault.get_secret("SLACK")
    return vault_secret

def authenticate() -> WebClient:
    secrets = credentials()
    client = WebClient(token=secrets["SLACK_TOKEN"])    
    return client

def send_message(client: WebClient,message:str):
    try:
        response = client.chat_postMessage(
            channel=CHANNEL_NAME,
            text=message
        )
    except SlackApiError as e:
        assert e.response["error"] 
    
def merge_data(data: dict[str,str]) -> str:
    message = f"{data['home']} - {data['away']} {data['home_goals']} - {data['away_goals']}"
    return message

def league_name(league:str):
    message = f"Results for {league.capitalize()}"
    return message