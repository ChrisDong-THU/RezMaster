# coding:utf-8
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QAction, QWidget, QVBoxLayout, QButtonGroup
from qfluentwidgets import (Action, DropDownPushButton, DropDownToolButton, PushButton, ToolButton, PrimaryPushButton,
                            HyperlinkButton, ComboBox, RadioButton, CheckBox, Slider, SwitchButton, EditableComboBox,
                            ToggleButton, RoundMenu, FluentIcon, SplitPushButton, SplitToolButton, PrimarySplitToolButton,
                            PrimarySplitPushButton, PrimaryDropDownPushButton, PrimaryToolButton, PrimaryDropDownToolButton,
                            ToggleToolButton, TransparentDropDownPushButton, TransparentPushButton, TransparentToggleToolButton,
                            TransparentTogglePushButton, TransparentDropDownToolButton, TransparentToolButton,
                            PillPushButton, PillToolButton)

from .gallery_interface import GalleryInterface
from .utils import createBoundWidgets

from ..common.translator import Translator


class ExtraInterface(GalleryInterface):
    """ Basic input interface """

    def __init__(self, parent=None):
        translator = Translator()
        super().__init__(parent=parent)
        self.setObjectName('extraInterface')

        # simple push button
        self.button1 = PushButton(self.tr('Analysis'), self, icon=FluentIcon.SEARCH)
        
        self.addExampleCard(
            self.tr('Explore more'),
            self.button1,
            stretch=1
        )
        
    