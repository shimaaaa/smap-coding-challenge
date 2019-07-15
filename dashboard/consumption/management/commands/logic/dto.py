import datetime


class UserData:
    def __init__(self,
                 user_id: int,
                 area: str,
                 tariff: str):
        self._user_id = user_id
        self._area = area
        self._tariff = tariff

    @property
    def user_id(self):
        return self._user_id

    @property
    def area(self):
        return self._area

    @property
    def tariff(self):
        return self._tariff


class ConsumptionData:

    def __init__(self,
                 user_id: int,
                 consumption_datetime: datetime.datetime,
                 consumption: float):
        self._user_id = user_id
        self._consumption_datetime = consumption_datetime
        self._consumption = consumption

    @property
    def user_id(self):
        return self._user_id

    @property
    def consumption_datetime(self):
        return self._consumption_datetime

    @property
    def consumption(self):
        return self._consumption
