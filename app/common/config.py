# coding:utf-8
import sys
from enum import Enum

from PyQt5.QtCore import QLocale
from qfluentwidgets import (qconfig, QConfig, ConfigItem, OptionsConfigItem, BoolValidator,
                            OptionsValidator, RangeConfigItem, RangeValidator,
                            FolderListValidator, Theme, FolderValidator, ConfigSerializer)


class Language(Enum):
    """ Language enumeration """

    CHINESE_SIMPLIFIED = QLocale(QLocale.Chinese, QLocale.China)
    ENGLISH = QLocale(QLocale.English)
    AUTO = QLocale()


class LanguageSerializer(ConfigSerializer):
    """ Language serializer """

    def serialize(self, language):
        return language.value.name() if language != Language.AUTO else "Auto"

    def deserialize(self, value: str):
        return Language(QLocale(value)) if value != "Auto" else Language.AUTO


def isWin11():
    return sys.platform == 'win32' and sys.getwindowsversion().build >= 22000


class Config(QConfig):
    """ Config of application """

    device = OptionsConfigItem("Devices", "Device", "cpu", OptionsValidator(["cpu", "cuda:0"]), restart=False)
    outputFolder = ConfigItem(
        "Folders", "Output", "./", FolderValidator())

    # main window
    micaEnabled = ConfigItem("MainWindow", "MicaEnabled", isWin11(), BoolValidator())
    dpiScale = OptionsConfigItem(
        "MainWindow", "DpiScale", "Auto", OptionsValidator([1, 1.25, 1.5, 1.75, 2, "Auto"]), restart=True)
    language = OptionsConfigItem(
        "MainWindow", "Language", Language.AUTO, OptionsValidator(Language), LanguageSerializer(), restart=True)


YEAR = 2024
AUTHOR = "IVG@SZ"
VERSION = "1.0"
HELP_URL = "https://github.com/ChrisDong-THU/RezMaster"
REPO_URL = "https://github.com/ChrisDong-THU/RezMaster"
FEEDBACK_URL = "https://github.com/ChrisDong-THU/RezMaster/issues"
RELEASE_URL = "https://github.com/ChrisDong-THU/RezMaster/releases"

cfg = Config()
cfg.themeMode.value = Theme.AUTO
qconfig.load('config/config.json', cfg)