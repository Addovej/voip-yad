import csv
from io import BytesIO

from yadisk import YaDisk

from app.config import Config


FIELDS_LIST = [
    'filename',
    'date',
    'status',
    'type',
    'phone_number_operator',
    'phone_number_client',
    'duration_answer'
]


class YandexDisk(object):
    """
        Implements access to Yandex.Disk REST API.

        :param token: application token
    """

    def __init__(self, token: str):
        self._disk = YaDisk(
            id=Config.YA_DISK_APP_ID,
            secret=Config.YA_DISK_APP_SECRET,
            token=token
        )
        self.token = token
        self.base_folder = Config.YA_DISK_BASE_FOLDER
        self.meta_folder = f'{self.base_folder}/meta'

    def check_token(self) -> bool:
        return self._disk.check_token(self.token)

    def _is_base_exists(self) -> bool:
        return self._disk.exists(self.base_folder)

    def _is_meta_exists(self) -> bool:
        return self._disk.exists(self.meta_folder)

    def _csv_files(self):
        for item in self._disk.listdir(self.meta_folder):
            if item.FIELDS.get('media_type', None) == 'spreadsheet':
                yield item.FIELDS.get('path', None)

    def _get_from_csv(self, file) -> list:
        buffer = BytesIO()
        self._disk.download(file, buffer)
        buffer.flush()
        splitted = buffer.getvalue().decode('utf-8-sig').splitlines()
        header, *body = [line for line in csv.reader(splitted, delimiter=';')]
        if header != FIELDS_LIST:
            return [{
                'file': file,
                'message': 'Header is invalid'
            }]

        return [dict(zip(header, item)) for item in body if item]

    def _get_files(self) -> list:
        data = []
        for file in self._csv_files():
            data = data + self._get_from_csv(file)
        return data

    def get_calls(self):
        if not self._is_meta_exists():
            return {'message': 'meta folder does not exists'}

        return self._get_files()
