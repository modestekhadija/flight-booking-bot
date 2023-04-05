# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
from enum import Enum
from typing import Dict, Tuple
from botbuilder.ai.luis import LuisRecognizer
from botbuilder.core import IntentScore, TopIntent, TurnContext
from booking_details import BookingDetails
import datetime

def extract_year_from_date(timex_string):
    try:
        year = int(timex_string.split("-")[0])
    except ValueError:
        year = datetime.datetime.now().year
    return year

def extract_month_from_date(timex_string):
    try:
        month = int(timex_string.split("-")[1])
    except ValueError:
        month = datetime.datetime.now().month
    return month

def extract_day_from_date(timex_string):
    try:
        day = int(timex_string.split("-")[2])
    except ValueError:
        day = datetime.datetime.now().day

    return day

def extract_date_from_timex(timex_string):
    year = extract_year_from_date(timex_string)
    print(year)
    month = extract_month_from_date(timex_string)
    print(month)
    day = extract_day_from_date(timex_string)
    print(day)
    date_obj = datetime.datetime(year, month, day)
    date_formatee = date_obj.strftime('%Y-%m-%d')

    return date_formatee

def extract_date_from_timex(timex_string):
    year = extract_year_from_date(timex_string)
    month = extract_month_from_date(timex_string)
    day = extract_day_from_date(timex_string)
    date_obj = datetime.datetime(year, month, day)
    date_formatee = date_obj.strftime('%Y-%m-%d')

    return date_formatee


class Intent(Enum):
    # Modification de l'intention <BOOK_FLIGHT>
    BOOK_FLIGHT = "FlightBooking"
    CANCEL = "Cancel"
    GET_WEATHER = "GetWeather"
    NONE_INTENT = "NoneIntent"


def top_intent(intents: Dict[Intent, dict]) -> TopIntent:
    max_intent = Intent.NONE_INTENT
    max_value = 0.0

    for intent, value in intents:
        intent_score = IntentScore(value)
        if intent_score.score > max_value:
            max_intent, max_value = intent, intent_score.score

    return TopIntent(max_intent, max_value)


class LuisHelper:
    @staticmethod
    async def execute_luis_query(luis_recognizer: LuisRecognizer, turn_context: TurnContext) -> Tuple[Intent, object]:
        """
        Returns an object with preformatted LUIS results for the bot's dialogs to consume.
        """
        result = None
        intent = None

        try:
            recognizer_result = await luis_recognizer.recognize(turn_context)
            print('\n Recognizer_result :')
            print(recognizer_result)
            print("\n")

            intent = (
                sorted(recognizer_result.intents, key=recognizer_result.intents.get, reverse=True)[:1][0]
                if recognizer_result.intents
                else None
            )

            if intent == Intent.BOOK_FLIGHT.value:
                result = BookingDetails()

                # We need to get the result from the LUIS JSON which at every level returns an array.

                # Destination
                to_entities = recognizer_result.entities.get("$instance", {}).get("dst_city", [])
                print('To_entities:', to_entities)
                print("\n")

                if len(to_entities) > 0:
                    print('Recognizer_result.entities.get("dst_city", [{"$instance": {}}])[0]:',recognizer_result.entities.get("dst_city", [{"$instance": {}}])[0])
                    print("\n")
                    if recognizer_result.entities.get("dst_city", [{"$instance": {}}])[0]:
                        result.destination = to_entities[0]["text"].capitalize()

                    else:
                        result.unsupported_airports.append(to_entities[0]["text"].capitalize())


                # Origin
                from_entities = recognizer_result.entities.get("$instance", {}).get("or_city", [])
                print('From_entities :', from_entities, "\n") 

                if len(from_entities) > 0:

                    if recognizer_result.entities.get("or_city", [{"$instance": {}}])[0]:
                        result.origin = from_entities[0]["text"].capitalize()

                    else:
                        result.unsupported_airports.append(from_entities[0]["text"].capitalize())

                # Travel Date and Return Date
                try:       
                    date_entities = recognizer_result.entities.get("datetime", [])
                    print("Date entities :", date_entities, "\n") 

                    if [x['timex'][0] for x in date_entities if x['type']=='date']:
                        date_entities_list = [x['timex'][0] for x in date_entities if x['type']=='date']
                        date_entities_formated = [extract_date_from_timex(x) for x in date_entities_list]
                        print("date_entities_list :", date_entities_list)

                        print(len(date_entities_list),"\n")   

                        if len(date_entities_list) > 1 :
                            result.travel_date = min(date_entities_formated)
                            result.return_date = max(date_entities_formated)
                            print("result.travel_date :", result.travel_date, "\n")   
                            print("result.return_date :", result.return_date, "\n")   

                        elif len(date_entities_list) == 1 :
                            result.travel_date = date_entities_formated[0]
                            print("result.travel_date :", result.travel_date, "\n")  

                    else :
                        result.travel_date = None
                        result.return_date = None 
                except Exception as e:
                    print(e)
                    result.travel_date = None
                    result.return_date = None 
              

                # Budget
                budget_entities = recognizer_result.entities.get("$instance", {}).get("budget", [])

                print('budget_entities :', budget_entities, "\n")
                

                if len(budget_entities) > 0:

                    if recognizer_result.entities.get("budget", [{"$instance": {}}])[0]:
                        print("Budget entities :", recognizer_result.entities.get("budget", [{"$instance": {}}])[0], "\n")
                        result.budget = budget_entities[0]["text"].capitalize()
                elif recognizer_result.entities.get("number", []):
                    budget_entities = recognizer_result.entities.get("number", [])
                    print("Budget entities :", budget_entities, "\n")
                    if max(budget_entities) > 31:
                        result.budget = max(budget_entities)
                    else:
                        result.budget = None
                else:
                    result.budget = None


        except Exception as exception:
            print(exception)

        return intent, result
