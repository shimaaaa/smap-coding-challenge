import abc
import datetime
from logging import getLogger
from typing import List, Dict

from django.db.utils import IntegrityError
from django.db.models import Avg, Sum
from django.db.models.functions import Trunc

from consumption.management.commands.logic.dto import UserData as UserDataDto
from consumption.management.commands.logic.dto import ConsumptionData as ConsumptionDataDto
from consumption.models import Users, UserConsumptions, ConsumptionDailySummary

logger = getLogger(__name__)


class DataImporter(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def user_bulk_import(self, users: List[UserDataDto]) -> None:
        pass

    @abc.abstractmethod
    def consumption_bulk_import(self, consumptions: List[ConsumptionDataDto]) -> None:
        pass

    @abc.abstractmethod
    def summary_import(self, target_datetime_from) -> None:
        pass


class DatabaseImporter(DataImporter):

    @classmethod
    def _convert_user_to_model(cls, user: UserDataDto) -> Users:
        return Users(
            id=user.user_id,
            area=user.area,
            tariff=user.tariff
        )

    @classmethod
    def _convert_consumption_to_model(cls, user: Users, consumption: ConsumptionDataDto) -> UserConsumptions:
        return UserConsumptions(
            user=user,
            datetime=consumption.consumption_datetime,
            consumption=consumption.consumption
        )

    @classmethod
    def _user_import(cls, user: Users):
        if Users.objects.filter(id=user.id).exists():
            return
        user.save()

    @classmethod
    def _consumption_import(cls, consumption: UserConsumptions):
        if UserConsumptions.objects.filter(user=consumption.user, datetime=consumption.datetime).exists():
            logger.warning('consumption data is already exits. (user_id: %s, datetime: %s)', consumption.user.id, consumption.datetime)
            return
        consumption.save()

    def _get_users_by_id(self, user_id_list) -> Dict[int, Users]:
        users_dict = dict()
        users = Users.objects.filter(id__in=user_id_list)

        for user in users:
            users_dict[user.id] = user

        return users_dict

    def user_bulk_import(self, dto_users: List[UserDataDto]) -> None:
        users = [self._convert_user_to_model(u) for u in dto_users]

        try:
            Users.objects.bulk_create(users)
        except IntegrityError:
            for user in users:
                self._user_import(user)

    def consumption_bulk_import(self, dto_consumptions: List[ConsumptionDataDto]) -> None:
        user_id_list = [c.user_id for c in dto_consumptions]
        users = self._get_users_by_id(user_id_list=list(set(user_id_list)))

        consumptions = list()

        for dto_consumption in dto_consumptions:
            user = users.get(dto_consumption.user_id)
            if user is None:
                continue
            consumption = self._convert_consumption_to_model(user=user, consumption=dto_consumption)
            consumptions.append(consumption)

        try:
            UserConsumptions.objects.bulk_create(consumptions)
        except IntegrityError:
            for consumption in consumptions:
                self._consumption_import(consumption)

    def summary_import(self, target_datetime_from: datetime.datetime):
        daily_data = UserConsumptions.objects\
                                     .annotate(target_date=Trunc('datetime', 'day')).values('target_date')\
                                     .annotate(total=Sum('consumption'))\
                                     .annotate(avg=Avg('consumption'))
        if target_datetime_from is not None:
            # set 00:00:00 to aggregate daily data
            target_datetime_from = target_datetime_from.replace(hour=0, minute=0, second=0)
            daily_data = daily_data.filter(datetime__gte=target_datetime_from)

        for d in daily_data:
            summary = ConsumptionDailySummary(
                target_date=d['target_date'],
                total_consumption=d['total'],
                average_consumption=d['avg']
            )
            summary.save()
