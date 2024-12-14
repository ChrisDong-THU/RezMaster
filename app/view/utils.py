from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout
from PyQt5.QtGui import QPixmap
from qfluentwidgets import FlowLayout

import time
import numpy as np
from functools import wraps
from enum import Enum


class RunMode(Enum):
    LOAD = 1
    PROCESS = 2


class ModelType(Enum):
    DDIR = 1
    DDIR_PLUS = 2
    DDIR_PRO = 3
    
    
class DataType(Enum):
    REAL_ARBI = 1
    FUNDUS = 2
    COLONOSCOPY = 3


def noscroll(method):
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        scrollbar = self.verticalScrollBar()
        scrollbar.setEnabled(False)
        
        try:
            return method(self, *args, **kwargs)
        finally:
            scrollbar.setEnabled(True)
    return wrapper

def min_time(min_time=3):
    def decorator(method):
        @wraps(method)
        def wrapper(self, *args, **kwargs):
            start_time = time.time()
            result = method(self, *args, **kwargs)
            time.sleep(max(0, min_time - (time.time() - start_time)))
            return result
        return wrapper
    return decorator

def createBoundWidgets(parent, widgets=[], animate=False):
    widget = QWidget(parent)
    layout = FlowLayout(widget, needAni=animate)

    layout.setContentsMargins(0, 0, 0, 0)
    layout.setSpacing(10)

    for w in widgets:
        layout.addWidget(w)
    
    return widget

def createWidget(parent, component, align=Qt.AlignCenter):
    widget = QWidget(parent)
    
    # nested layout
    outer_layout = QVBoxLayout()
    outer_layout.setAlignment(align)
    outer_layout.setContentsMargins(0, 0, 0, 0)

    flow_layout = FlowLayout()
    flow_layout.addWidget(component)
    flow_layout.setContentsMargins(0, 0, 0, 0)
    flow_layout.setSpacing(10)

    outer_layout.addLayout(flow_layout)
    widget.setLayout(outer_layout)
    
    return widget

def get_pix_size(pix):
    if isinstance(pix, QPixmap):
        h = pix.height()
        w = pix.width()
    elif isinstance(pix, np.ndarray):
        h, w = pix.shape[:2]
    
    return f"{h}x{w}"