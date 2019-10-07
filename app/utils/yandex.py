from yadisk import YaDisk

from app.config import Config


class YandexDisc(object):
    """
        Implements access to Yandex.Disk REST API.

        :param token: application token
    """

    def __init__(self, token: str):
        self._ya_disc = YaDisk(
            id=Config.YA_DISK_APP_ID,
            secret=Config.YA_DISK_APP_SECRET,
            token=token
        )
        self.token = token
        self.base_folder = Config.YA_DISC_BASE_FOLDER
        self.meta_folder = f'{self.base_folder}/meta'

    def check_token(self) -> bool:
        return self._ya_disc.check_token(self.token)

    def _is_base_exists(self) -> bool:
        return self._ya_disc.exists(self.base_folder)

    def _is_meta_exists(self) -> bool:
        return self._ya_disc.exists(f'{self.base_folder}/meta')

    def _get_files(self):
        pass

    def get_calls(self):
        if not self._is_meta_exists():
            return {'message': 'meta folder does not exists'}

        files = self._ya_disc.listdir(f'{self.base_folder}/meta')

        return [file for file in files]
