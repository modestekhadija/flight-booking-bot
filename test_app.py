import unittest


from botbuilder.dialogs import (
    ComponentDialog,
    WaterfallDialog,
    WaterfallStepContext,
    DialogTurnResult,
)
from botbuilder.dialogs.prompts import TextPrompt, PromptOptions
from botbuilder.core import (
    MessageFactory,
    TurnContext,
    BotTelemetryClient,
    NullTelemetryClient,
)
from botbuilder.schema import InputHints

from booking_details import BookingDetails
from flight_booking_recognizer import FlightBookingRecognizer
from helpers.luis_helper import LuisHelper, Intent
from dialogs.booking_dialog import BookingDialog


class TestApp(unittest.TestCase):
    def test_flight_or_city(self):
        self.assertEqual(BookingDetails(destination = 'Madrid').destination, 'Madrid')

    def test_flight_dst_city(self):
        self.assertEqual(BookingDetails(origin='Lyon').origin, 'Lyon')

    def test_flight_str_date(self):
        self.assertEqual(BookingDetails(travel_date='Today').travel_date, 'Today')

    def test_flight_end_date(self):
        self.assertEqual(BookingDetails(return_date='Tomorrow').return_date, 'Tomorrow')

    def test_flight_budget(self):
        self.assertEqual(BookingDetails(budget=500).budget, 500)
# TOO : add more tests



if __name__ == '__main__':
    unittest.main()