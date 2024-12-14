from PyQt5.QtCore import Qt, pyqtSignal, QPoint, QStandardPaths, QSize, QMargins
from PyQt5.QtWidgets import QWidget, QStackedWidget, QVBoxLayout, QLabel, QHBoxLayout, QFrame, QSizePolicy, QFileDialog
from qfluentwidgets import (qrouter, BodyLabel, CommandBar, CommandBarView, FlyoutView, FlyoutViewBase, Flyout, Action, FlyoutAnimationType, 
                            TabCloseButtonDisplayMode, TabBar, Slider, IndeterminateProgressRing, IconWidget, TransparentToolButton, FluentIcon)
from qfluentwidgets import FluentIcon as FIF

from ..common.config import cfg
from ..common.style_sheet import StyleSheet
from ..components.QtImageViewer import QtImageViewer


class TabInterface(QWidget):
    """ Tab interface """
    illegal_ops = pyqtSignal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.tabCount = 1

        self.stackedTabView = QStackedWidget(self)
        self.tabBar = TabBar(self)
        self.stackedWidget = QStackedWidget(self)

        self.tabBar.setMovable(True)
        self.tabBar.setScrollable(True)
        self.tabBar.setTabShadowEnabled(True)
        self.tabBar.setCloseButtonDisplayMode(TabCloseButtonDisplayMode.ALWAYS)

        self.rawInfo = self.tr('Click input and load the raw image.')
        self.newInfo = self.tr('Set the scale factor and click start.')
        
        self.rawInterface = NewInterface(self, self.rawInfo)
        
        self.tabView = QWidget(self)
        self.settingView = QWidget(self)
        
        self.stackedTabView.addWidget(self.tabView)
        self.stackedTabView.addWidget(self.settingView)
        
        self.vBoxLayout1 = QVBoxLayout(self)
        self.vBoxLayout2 = QVBoxLayout(self.tabView)
        self.vBoxLayout3 = QVBoxLayout(self.settingView)
        
        self.settingWidget = QFrame(self)
        self.slider = Slider(Qt.Horizontal, self)
        self.slider.setRange(40, 200)
        self.slider.setValue(100)
        self.settingVBoxlayout = QVBoxLayout(self.settingWidget)
        
        self.toolWidget = QFrame(self)
        self.toolBar = self.createCommandBar()
        self.toolsHBoxLayout = QHBoxLayout(self.toolWidget)

        # add items to pivot
        self.__initWidget()

    def __initWidget(self):
        self._initLayout()
        
        self.addSubInterface(self.rawInterface,
                             'tabRawInterface', self.tr('Raw Image'), ':/rm/images/controls/Image2.png')

        self.settingWidget.setObjectName('settingWidget')
        self.toolWidget.setObjectName('bottomWidget') # 便于应用qss
        StyleSheet.NAVIGATION_VIEW_INTERFACE.apply(self)

        self.connectSignalToSlot()

        qrouter.setDefaultRouteKey(
            self.stackedWidget, self.rawInterface.objectName())

    def connectSignalToSlot(self):
        self.tabBar.tabAddRequested.connect(self.addTabInterface)
        self.tabBar.tabCloseRequested.connect(self.removeTab)

        self.stackedWidget.currentChanged.connect(self.onCurrentIndexChanged)
        self.slider.valueChanged.connect(self.onAdjustHeight)

    def _initLayout(self):
        self.tabViewDefaultHeight = 500
        self.stackedTabView.setFixedHeight(self.tabViewDefaultHeight)
        self.tabBar.setTabMaximumWidth(200)
        self.toolBar.setMinimumWidth(310)

        self.vBoxLayout1.setSpacing(12)
        self.vBoxLayout1.setContentsMargins(0, 0, 0, 0)

        self.vBoxLayout1.addWidget(self.stackedTabView, 0)
        self.vBoxLayout1.addWidget(self.toolWidget, 0)
        self.vBoxLayout1.setAlignment(Qt.AlignTop)

        self.vBoxLayout2.addWidget(self.tabBar)
        self.vBoxLayout2.addWidget(self.stackedWidget)
        self.vBoxLayout2.setContentsMargins(8, 0, 8, 0)
        
        self.vBoxLayout3.addWidget(self.settingWidget)
        self.vBoxLayout3.setAlignment(Qt.AlignTop)
        self.vBoxLayout3.setContentsMargins(16, 16, 16, 0)
        
        self.settingVBoxlayout.addWidget(self.slider, 0, Qt.AlignTop)
        self.settingVBoxlayout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)

        self.toolsHBoxLayout.addWidget(self.toolBar, 0, Qt.AlignRight)
        self.toolsHBoxLayout.setAlignment(Qt.AlignRight)
        self.toolsHBoxLayout.setContentsMargins(8, 8, 8, 8)

    def createCommandBar(self):
        bar = CommandBar(self)
        bar.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        bar.addActions([
            Action(FIF.INFO, self.tr('Info'), triggered=self.onInfoClicked),
            Action(FIF.DOWNLOAD, self.tr('Save'), triggered=self.onSaveClicked),
            Action(FIF.DELETE, self.tr('Del'), triggered=self.onDeleteClicked),
        ])
        bar.addSeparator()
        bar.addActions([
            Action(FIF.SETTING, self.tr('Zoom'), triggered=self.onZoomClicked),
        ])

        return bar
    
    def onInfoClicked(self):
        pass
    
    def onSaveClicked(self):
        self.stackedWidget.currentWidget().save_image()
        
    def onDeleteClicked(self):
        self.stackedWidget.currentWidget().del_image()
        
    def onZoomClicked(self):
        self.onNextTabView()
    
    def onNextTabView(self):
        currentIndex = self.stackedTabView.currentIndex()
        nextIndex = (currentIndex + 1) % self.stackedTabView.count()
        self.stackedTabView.setCurrentIndex(nextIndex)
    
    def addSubInterface(self, widget, objectName, text, icon):
        widget.setObjectName(objectName)
        self.stackedWidget.addWidget(widget)
        self.tabBar.addTab(
            routeKey=objectName,
            text=text,
            icon=icon,
            onClick=lambda: self.stackedWidget.setCurrentWidget(widget)
        )

    def onAdjustHeight(self, value):
        height = min(value*self.tabViewDefaultHeight/100, self.window().height()-180)
        
        self.stackedTabView.setFixedHeight(height)
        self.slider.setValue(height/self.tabViewDefaultHeight*100)
    
    def onCurrentIndexChanged(self, index):
        widget = self.stackedWidget.widget(index)
        if not widget:
            return

        qrouter.push(self.stackedWidget, widget.objectName())
    
    def addTabInterface(self):
        self.tabCount += 1
        widget = NewInterface(self, self.newInfo)
        self.addSubInterface(widget, f'tab{self.tabCount}', self.tr('New Image'), ':/rm/images/controls/Image.png')
        
        qrouter.push(self.stackedWidget, widget.objectName())
        self.tabBar.setCurrentIndex(self.tabBar.count() - 1)
        self.stackedWidget.setCurrentWidget(widget)

    def removeTab(self, index):
        item = self.tabBar.tabItem(index)
        
        if item.routeKey() == 'tabRawInterface':
            self.illegal_ops.emit(self.tr('Raw image cannot be deleted.'))
            return

        widget = self.findChild(QWidget, item.routeKey())
        if widget.is_busy:
            self.illegal_ops.emit(self.tr('Current tab is in progress.'))
            return
        
        self.tabBar.removeTab(index)
        self.stackedWidget.removeWidget(widget)
        widget.deleteLater()
        
        
class NewInterface(QStackedWidget):
    def __init__(self, parent=None, info=None):
        super().__init__(parent=parent)
        self.is_busy = False
        
        self.infoWidget = QWidget(self)
        self.ringWidget = QWidget(self)
        self.resultWidget = QtImageViewer(self)

        self.infoLabel = QLabel(info, self)
        
        self.ring = IndeterminateProgressRing(self)
        self.ring.setFixedSize(64, 64)
        
        self.vBoxLayout1 = QVBoxLayout(self.infoWidget)
        self.vBoxLayout2 = QVBoxLayout(self.ringWidget)
        self.vBoxLayout3 = QVBoxLayout(self.resultWidget)

        self._init_widget()

    def _init_widget(self):
        self.addWidget(self.infoWidget)
        self.addWidget(self.ringWidget)
        self.addWidget(self.resultWidget)
        
        self.resultWidget.setObjectName('resultWidget')
        StyleSheet.NAVIGATION_VIEW_INTERFACE.apply(self)
        
        self.connectSignalToSlot()
        self._init_layout()
        self.set_info()
    
    def _init_layout(self):
        self.vBoxLayout1.addWidget(self.infoLabel, 0, Qt.AlignCenter)
        self.vBoxLayout1.setAlignment(Qt.AlignCenter)
        
        self.vBoxLayout2.addWidget(self.ring, 0, Qt.AlignCenter)
        self.vBoxLayout2.setAlignment(Qt.AlignCenter)

        self.vBoxLayout3.setAlignment(Qt.AlignCenter)
    
    def connectSignalToSlot(self):
        self.resultWidget.rightMouseButtonPressed.connect(self.createCommandBarFlyout)
    
    def set_info(self, info=None):
        if info:
            self.infoLabel.setText(info)
        self.setCurrentIndex(0)
    
    def set_busy(self):
        self.is_busy = True
        self.setCurrentIndex(1)
    
    def set_image(self, img):
        self.is_busy = False
        self.resultWidget.setImage(img)
        self.setCurrentIndex(2)
    
    def createCommandBarFlyout(self, x, y):
        view = CommandBarView(self)

        view.addAction(Action(FIF.DOWNLOAD, self.tr('Save'), triggered=self.save_image))
        view.addAction(Action(FIF.DELETE, self.tr('Delete'), triggered=self.del_image))

        view.resizeToSuitableWidth()

        Flyout.make(view, self.resultWidget, self, FlyoutAnimationType.FADE_IN)
        
    def save_image(self):
        if not self.resultWidget.hasImage():
            return
        
        path, ok = QFileDialog.getSaveFileName(
            parent=self,
            caption=self.tr('Save image'),
            directory=cfg.get(cfg.outputFolder),
            filter='PNG (*.png)'
        )
        if not ok:
            return

        self.resultWidget.image().save(path, 'PNG')
        
    def del_image(self):
        self.resultWidget.clearImage()
        self.set_info()

