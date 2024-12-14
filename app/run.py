# coding:utf-8
import os
import sys

from PyQt5.QtCore import Qt, QTranslator
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication
from qfluentwidgets import FluentTranslator

from .common.config import cfg
from .view.main_window import MainWindow


def run_program():
    # enable dpi scale
    if cfg.get(cfg.dpiScale) == "Auto":
        QApplication.setHighDpiScaleFactorRoundingPolicy(
            Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
        QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    else:
        os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "0"
        os.environ["QT_SCALE_FACTOR"] = str(cfg.get(cfg.dpiScale))

    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

    # create application
    app = QApplication(sys.argv)
    app.setAttribute(Qt.AA_DontCreateNativeWidgetSiblings)

    # internationalization
    locale = cfg.get(cfg.language).value
    translator = FluentTranslator(locale)
    rmTranslator = QTranslator()
    rmTranslator.load(locale, "rm", ".", ":/rm/i18n")

    app.installTranslator(translator)
    app.installTranslator(rmTranslator)

    # create main window
    w = MainWindow()
    w.basicInterface.run_thread.rez.set_ckpt_dir('./model')
    w.show()

    app.exec_()

