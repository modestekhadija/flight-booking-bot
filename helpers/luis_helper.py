# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
from enum import Enum
from typing import Dict, Tuple
from botbuilder.ai.luis import LuisRecognizer
from botbuilder.core import IntentScore, TopIntent, TurnContext
import pprint

from booking_details import BookingDetails


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
            print('===============================recognizer_result=============================================')
            print(recognizer_result)

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
                print('===============================to_entities=============================================')
                print(to_entities)

                if len(to_entities) > 0:
                    print('===================recognizer_result.entities.get("dst_city", [{"$instance": {}}])[0]=============================================')
                    print(recognizer_result.entities.get("dst_city", [{"$instance": {}}])[0])
                    print(to_entities[0]["text"].capitalize())
                    if recognizer_result.entities.get("dst_city", [{"$instance": {}}])[0]:
                        result.destination = to_entities[0]["text"].capitalize()

                    else:
                        result.unsupported_airports.append(to_entities[0]["text"].capitalize())



                # Origin
                from_entities = recognizer_result.entities.get("$instance", {}).get("or_city", [])
                print('===============================from_entities=============================================')
                print(from_entities)

                if len(from_entities) > 0:
                    print('===================recognizer_result.entities.get("or_city", [{"$instance": {}}])[0]=============================================')
                    print(recognizer_result.entities.get("or_city", [{"$instance": {}}])[0])
                    if recognizer_result.entities.get("or_city", [{"$instance": {}}])[0]:
                        result.origin = from_entities[0]["text"].capitalize()

                    else:
                        result.unsupported_airports.append(from_entities[0]["text"].capitalize())

                # This value will be a TIMEX. And we are only interested in a Date so grab the first result and drop
                # the Time part. TIMEX is a format that represents DateTime expressions that include some ambiguity.
                # e.g. missing a Year.


                # Start date
                date_entities = recognizer_result.entities.get("datetime", [])
                print('===============================str_date_entities=============================================')
                print(date_entities)

                if date_entities[0]:
                    timex = date_entities[0]["timex"]

                if timex:                
                    datetime = timex[0].split("T")[0]
                    result.travel_date = datetime

                else:
                    result.travel_date = None


                # End date
                end_date_entities = recognizer_result.entities.get("datetime", [])
                print('===============================end_date_entities=============================================')
                print(end_date_entities)

                if len(end_date_entities)>1 and end_date_entities[1]:
                    timex = end_date_entities[1]["timex"]

                if timex:                
                    datetime = timex[0].split("T")[0]
                    result.return_date = datetime

                else:
                    result.return_date = None


                # Budget
                budget_entities = recognizer_result.entities.get("$instance", {}).get("budget", [])
                print('===============================budget_entities=============================================')
                print(budget_entities)

                if len(budget_entities) > 0:

                    if recognizer_result.entities.get("budget", [{"$instance": {}}])[0]:
                        result.budget = budget_entities[0]["text"].capitalize()


        except Exception as exception:
            print(exception)

        return intent, result
