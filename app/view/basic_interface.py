# coding:utf-8
from PyQt5.QtCore import Qt, QSize, QVariant, QStandardPaths
from PyQt5.QtWidgets import QFileDialog, QWidget, QVBoxLayout, QButtonGroup, QStackedWidget
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import QThread, pyqtSignal
from qfluentwidgets import (IndeterminateProgressBar, PushButton, SplitPushButton, FluentIcon, DoubleSpinBox, InfoBar, InfoBarPosition, RoundMenu, Action)

from .gallery_interface import GalleryInterface
from .utils import ModelType, DataType, RunMode
from .utils import createBoundWidgets, createWidget, get_pix_size, noscroll, min_time

from ._tab import TabInterface
from ..common.signal_bus import signalBus
from ..common.config import cfg

from ..functions import RezMaster


class WorkerThread(QThread):
    fail_signal = pyqtSignal()
    success_signal = pyqtSignal()
    run_signal = pyqtSignal(QVariant, str) # QVariant: Any type
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.rez = RezMaster(cfg.device.value)
        self.scale = 1.0
        self.model_type = None
        self.data_type = None
        self.pending_model_type = None
        self.pending_data_type = None
        
        self.ops = RunMode.LOAD
    
    def set_scale(self, scale):
        self.scale = scale
    
    def run(self):
        if self.ops == RunMode.LOAD:
            self.run_load()
        elif self.ops == RunMode.PROCESS:
            self.run_process()
    
    @min_time(2)
    def process(self):
        result = self.rez.process(self.scale)
        caption = f'M{self.model_type.value}-D{self.data_type.value}-{get_pix_size(result)}'
        return result, caption

    @min_time(2)
    def load_model(self):
        self.model_type = self.pending_model_type
        self.data_type = self.pending_data_type
        return self.rez.load_model(self.model_type, self.data_type)
        
    def run_process(self):
        result, caption = self.process()
        self.run_signal.emit(result, caption)
    
    def run_load(self):
        if self.load_model():
            self.success_signal.emit()
        else:
            self.fail_signal.emit()
        

class BasicInterface(GalleryInterface):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setObjectName('basicInterface')
        
        self.run_thread = WorkerThread()
        
        self.tab = TabInterface(self)
        self.currentTabIndex = None
        card = self.addExampleCard(
            self.tr('Image Gallery'),
            widget=self.tab,
            stretch=1
        )
        card.topLayout.setContentsMargins(0, 0, 0, 0)
        
        self.button1 = PushButton(self.tr('Input'), self, icon=FluentIcon.PHOTO)
        self.button2 = PushButton(self.tr('Start'), self, icon=FluentIcon.PLAY)
        
        self.model_dict = {'DDIR': ModelType.DDIR, 'DDIR PLUS': ModelType.DDIR_PLUS, 'DDIR PRO': ModelType.DDIR_PRO}
        self.data_dict = {'RealArbi': DataType.REAL_ARBI, 'Fundus': DataType.FUNDUS, 'Colonoscopy': DataType.COLONOSCOPY}
        
        self.button3 = SplitPushButton(self.tr('Model Type'), self, FluentIcon.ROBOT)
        self.button3.setFlyout(self.createStandMenu(self.button3, self.model_dict.keys(), 'Model Type'))
        self.button4 = SplitPushButton(self.tr('Data Type'), self, FluentIcon.TAG)
        self.button4.setFlyout(self.createStandMenu(self.button4, self.data_dict.keys(), 'Data Type'))
        self.button5 = PushButton(self.tr('Load'), self, icon=FluentIcon.POWER_BUTTON)
        
        self.spinBox = DoubleSpinBox(self)
        self.spinBox.setRange(1.0, 8.0)
        self.spinBox.setValue(self.run_thread.scale)
        
        bar = IndeterminateProgressBar(self)
        bar.setFixedWidth(360)
        
        self.stackedSetView = QStackedWidget(self)
        self.stackedSetView.addWidget(createBoundWidgets(self, [self.button3, self.button4, self.button5, \
            self.spinBox, self.button1, self.button2], animate=True))
        self.stackedSetView.addWidget(createWidget(self, bar, align=Qt.AlignCenter))
        
        self.addExampleCard(
            self.tr('Control Panel'),
            self.stackedSetView,
            stretch=1
        )

        self.connectSignalToSlot()
    
    def connectSignalToSlot(self):
        self.button1.clicked.connect(self.onOpenButtonClicked)
        self.button2.clicked.connect(self.onStartButtonClicked)
        self.button5.clicked.connect(self.onLoadClicked)

        self.tab.illegal_ops.connect(self.createErrorInfor)
        self.spinBox.valueChanged.connect(self.onScaleChanged)
        
        self.run_thread.run_signal.connect(self.onRunSignal)
        self.run_thread.success_signal.connect(self.onLoadSuccess)
        self.run_thread.fail_signal.connect(self.onLoadFail)
        
        signalBus.switchDevice.connect(self.run_thread.rez.sr_api.switch_device)
    
    def onOpenButtonClicked(self):
        path, _ = QFileDialog.getOpenFileName(self, self.tr('Select Image'), \
            QStandardPaths.writableLocation(QStandardPaths.DesktopLocation),'*.jpg *.png')
        if path=='':
            return
        self.load_image(path)
        
    def onScaleChanged(self, value):
        self.run_thread.scale = value
    
    def setBtnStatus(self, status):
        self.button1.setEnabled(status)
        self.button2.setEnabled(status)
        self.button5.setEnabled(status)
    
    def onStartButtonClicked(self):
        self.setBtnStatus(False)
        if self.run_thread.rez.sr_api.model is None:
            self.createErrorInfor(self.tr('Please load a model first.'))
            self.setBtnStatus(True)
            return
        
        if self.run_thread.rez.raw_image is None:
            self.createErrorInfor(self.tr('Please input a raw image first.'))
            self.setBtnStatus(True)
            return
        
        if self.tab.stackedWidget.currentWidget().objectName() == 'tabRawInterface':
            self.tab.addTabInterface()
        
        self.currentTabIndex = self.tab.stackedWidget.currentIndex()
        self.tab.tabBar.setTabText(self.currentTabIndex, self.tr('Processing...'))
        self.tab.stackedWidget.widget(self.currentTabIndex).set_busy()
        
        self.run_thread.ops = RunMode.PROCESS
        self.run_thread.start()
    
    @noscroll
    def set_busy(self, *args, **kwargs):
        self.stackedSetView.setCurrentIndex(1)
    
    @noscroll
    def set_idle(self, *args, **kwargs):
        self.stackedSetView.setCurrentIndex(0)
    
    def onLoadSuccess(self):
        self.createSuccessInfo(self.tr('Load Model Done.'))
        self.set_idle()
        
    def onLoadFail(self):
        self.createErrorInfor(self.tr('Please ensure the \"./model\" folder is properly configured.'))
        self.set_idle()
    
    def onLoadClicked(self):
        if self.run_thread.pending_model_type is None or self.run_thread.pending_data_type is None:
            self.createErrorInfor(self.tr('Please select model type and data type first.'))
            return
        self.set_busy()
        
        self.run_thread.ops = RunMode.LOAD
        self.run_thread.start()
    
    def onRunSignal(self, result, caption):
        self.createSuccessInfo(caption+self.tr(' Done.'))
        
        pix = self.img2pix(result)
        self.tab.tabBar.setTabText(self.currentTabIndex, caption)
        self.tab.stackedWidget.widget(self.currentTabIndex).set_image(pix)
        self.setBtnStatus(True)
    
    @staticmethod
    def img2pix(img):
        y, x = img.shape[:-1]
        frame = QImage(img, x, y, x*3, QImage.Format_RGB888) # x*3防止倾斜
        pix = QPixmap.fromImage(frame)
        
        return pix
    
    def load_image(self, path):
        self.run_thread.rez.set_image(path)
        pix = self.img2pix(self.run_thread.rez.raw_image)
        self.tab.rawInterface.set_image(pix)
        self.tab.tabBar.setTabText(0, self.tr('Raw Image ')+'-'+get_pix_size(pix))
    
    @noscroll
    def createErrorInfor(self, message, *args, **kwargs):
        InfoBar.error(
            title=self.tr('ERROR'),
            content=message,
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP,
            duration=2000,
            parent=self
        )
    
    @noscroll
    def createSuccessInfo(self, message, *args, **kwargs):
        InfoBar.success(
            title=self.tr('SUCCESS'),
            content=message,
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP,
            duration=2000,
            parent=self
        )
        
    def createStandMenu(self, button, options, cls):
        menu = RoundMenu(parent=self)
        actions = [Action(option, triggered=lambda c, b=button, o=option: [b.setText(o), self.set_type(cls, o)]) for option in options]
        menu.addActions(actions)
        return menu
    
    def set_type(self, cls, option):
        if cls == 'Model Type':
            self.run_thread.pending_model_type = self.model_dict[option]
        elif cls == 'Data Type':
            self.run_thread.pending_data_type = self.data_dict[option]
        

    