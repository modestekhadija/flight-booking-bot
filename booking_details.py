# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
import datetime


class BookingDetails:
    def __init__(
        self,
        destination: str = None,
        origin: str = None,
        travel_date: datetime = None,
        return_date: datetime = None,
        budget: int = None,
        unsupported_airports=None,
    ):
        if unsupported_airports is None:
            unsupported_airports = []
        self.destination = destination
        self.origin = origin
        self.travel_date = travel_date
        self.return_date = return_date
        self.budget = budget
        self.unsupported_airports = unsupported_airports
