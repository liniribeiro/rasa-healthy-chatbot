import os
from typing import Any, Text, Dict, List, Union

from rasa_sdk import Action, Tracker
from rasa_sdk.events import EventType
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.forms import FormAction, FormValidationAction
from dotenv import load_dotenv

import requests
import json


load_dotenv()

airtable_api_key = os.getenv("AIRTABLE_API_KEY")
base_id = os.getenv("BASE_ID")
table_name = os.getenv("TABLE_NAME")


def create_health_log(confirm_exercise, exercise, sleep, diet, stress, goal):
    request_url = f"https://api.airtable.com/v0/{base_id}/{table_name}"

    headers = {
        "Content-Type": "application/json",
        "Accept":  "application/json",
        "Authorization": f"Bearer {airtable_api_key}"
    }

    data = {
        "fields": {
            "Exercised?": confirm_exercise,
            "Type of exercise": exercise,
            "Amount of sleep": sleep,
            "Stress": stress,
            "Diet": diet,
            "Goal": goal
        }
    }

    try:
        response = requests.post(
            request_url, headers=headers, data=json.dumps(data)
        )
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)

    print(response.status_code)
    return response


class HealthFormSubmit(Action):

    def name(self) -> Text:
        return 'health_form_submit'

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        create_health_log(tracker.get_slot('confirm_exercise'),
                          tracker.get_slot('exercise'),
                          tracker.get_slot('sleep'),
                          tracker.get_slot('diet'),
                          tracker.get_slot('stress'),
                          tracker.get_slot('goal'))

        dispatcher.utter_message(text="Thanks, your answers have been recorded!")
        return []