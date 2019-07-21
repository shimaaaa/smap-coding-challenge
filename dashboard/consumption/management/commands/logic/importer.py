import abc
import datetime
from logging import getLogger
from typing import List, Dict, Optional

from django.db import transaction
from django.db.utils import IntegrityError
from django.db.models import Avg, Sum
from django.db.models.functions import Trunc

from consumption.management.commands.logic.dto import UserData as UserDataDto
from consumption.management.commands.logic.dto import ConsumptionData as ConsumptionDataDto
from consumption.models import User, UserConsumption, ConsumptionDailySummary

logger = getLogger(__name__)


class DataImporter(metaclass=abc.ABCMeta):
    """
    Data import abstract class
    """

    @abc.abstractmethod
    def user_bulk_import(self, users: List[UserDataDto]) -> None:
        """
        Bulk import user data
            If data with the same user ID already exists, no user data will be registered.
        :param users:
        :return: None
        """
        pass

    @abc.abstractmethod
    def consumption_bulk_import(self, consumptions: List[ConsumptionDataDto]) -> None:
        """
        Bulk import consumption data
            If data with the same user ID and datetime already exists, no consumption data will be registered.
        :param consumptions:
        :return: None
        """
        pass

    @abc.abstractmethod
    def summary_import(self, target_datetime_from) -> None:
        """
        Create aggregation daily consumption data
        :param target_datetime_from: data aggregation start datetime
        :return: None
        """
        pass


class DatabaseImporter(DataImporter):

    @classmethod
    def _convert_user_to_model(cls, user: UserDataDto) -> User:
        return User(
            id=user.user_id,
            area=user.area,
            tariff=user.tariff
        )

    @classmethod
    def _convert_consumption_to_model(cls, user: User, consumption: ConsumptionDataDto) -> UserConsumption:
        return UserConsumption(
            user=user,
            target_datetime=consumption.target_datetime,
            value=consumption.value
        )

    @classmethod
    def _user_import(cls, user: User):
        if User.objects.filter(id=user.id).exists():
            logger.warning('user data is already exits. (user_id: %s)', user.id)
            return
        user.save()

    @classmethod
    def _consumption_import(cls, consumption: UserConsumption):
        if UserConsumption.objects.filter(user=consumption.user, target_datetime=consumption.target_datetime).exists():
            logger.warning('consumption data is already exits. (user_id: %s, datetime: %s)',
                           consumption.user.id, consumption.target_datetime)
            return
        consumption.save()

    @classmethod
    def _get_users_by_id(cls, user_id_list) -> Dict[int, User]:
        users_dict = dict()
        users = User.objects.filter(id__in=user_id_list)

        for user in users:
            users_dict[user.id] = user

        return users_dict

    def user_bulk_import(self, dto_users: List[UserDataDto]) -> None:
        users = [self._convert_user_to_model(u) for u in dto_users]

        try:
            with transaction.atomic():
                User.objects.bulk_create(users)
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
                logger.warning('consumption data user dose not found. (user_id: %s)', dto_consumption.user_id)
                continue
            consumption = self._convert_consumption_to_model(user=user, consumption=dto_consumption)
            consumptions.append(consumption)

        try:
            with transaction.atomic():
                UserConsumption.objects.bulk_create(consumptions)
        except IntegrityError:
            for consumption in consumptions:
                self._consumption_import(consumption)

    def summary_import(self, target_datetime_from: Optional[datetime.datetime] = None):
        daily_data = UserConsumption.objects\
                                    .annotate(target_date=Trunc('target_datetime', 'day')).values('target_date')\
                                    .annotate(total=Sum('value'))\
                                    .annotate(avg=Avg('value'))
        if target_datetime_from is not None:
            # set 00:00:00 to aggregate daily data
            target_datetime_from = target_datetime_from.replace(hour=0, minute=0, second=0)
            daily_data = daily_data.filter(target_datetime__gte=target_datetime_from)

        for d in daily_data:
            summary = ConsumptionDailySummary(
                target_date=d['target_date'],
                total_value=d['total'],
                average_value=d['avg']
            )
            summary.save()
