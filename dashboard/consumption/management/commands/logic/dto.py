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
                 target_datetime: datetime.datetime,
                 value: float):
        self._user_id = user_id
        self._target_datetime = target_datetime
        self._value = value

    @property
    def user_id(self):
        return self._user_id

    @property
    def target_datetime(self):
        return self._target_datetime

    @property
    def value(self):
        return self._value
