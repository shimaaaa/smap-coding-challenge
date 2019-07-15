import csv
import abc
import datetime
from logging import getLogger
from pathlib import Path
from typing import Generator

import pytz

from consumption.management.commands.logic.dto import UserData, ConsumptionData

logger = getLogger(__name__)


class DataReader(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def read_user(self) -> Generator[UserData, None, None]:
        pass

    @abc.abstractmethod
    def read_consumption(self) -> Generator[ConsumptionData, None, None]:
        pass


class DataFileReader(DataReader):
    USER_DATA_FILE = 'user_data.csv'
    CONSUMPTION_DATA_DIRECTORY = 'consumption'

    def __init__(self, target_dir: Path):
        self._target_dir = target_dir

    def _get_user_data_file_path(self):
        return self._target_dir / Path(self.USER_DATA_FILE)

    def _get_consumption_data_directory_path(self):
        return self._target_dir / Path(self.CONSUMPTION_DATA_DIRECTORY)

    def read_user(self) -> Generator[UserData, None, None]:
        with self._get_user_data_file_path().open(mode='r') as f:
            reader = csv.DictReader(f, skipinitialspace=True)
            row_count = 1
            for row in reader:
                row_count += 1
                try:
                    user_id = int(row['id'])
                    yield UserData(
                        user_id=user_id,
                        area=row['area'],
                        tariff=row['tariff']
                    )
                except Exception as e:
                    logger.warning(f'fail to import user data (line: {row_count}, cause: {e})')

    @classmethod
    def _convert_to_datetime(cls, value: str) -> datetime:
        dt = datetime.datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
        return pytz.utc.localize(dt)

    def read_consumption(self) -> Generator[ConsumptionData, None, None]:

        for data_file in self._get_consumption_data_directory_path().glob('**/*.csv'):

            with data_file.open(mode='r') as f:
                reader = csv.DictReader(f, skipinitialspace=True)
                row_count = 1
                file_name = data_file.name
                user_id = file_name.replace('.csv', '')
                for row in reader:
                    row_count += 1
                    try:
                        user_id = int(user_id)
                        consumption_datetime = self._convert_to_datetime(row['datetime'])
                        yield ConsumptionData(
                            user_id=user_id,
                            consumption_datetime=consumption_datetime,
                            consumption=row['consumption']
                        )
                    except Exception as e:
                        logger.warning(f'fail to import consumption data (file: {file_name}, line: {row_count}, cause: {e})')
