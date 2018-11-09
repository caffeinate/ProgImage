import shutil
import tempfile

from prog_image.settings.global_config import BaseConfig

class Config(BaseConfig):
    DEBUG = True
    TESTING = True
    FILEBASE = None

    def reset(self):
        if self.FILEBASE:
            shutil.rmtree(self.FILEBASE)

        self.FILEBASE = tempfile.mkdtemp()
