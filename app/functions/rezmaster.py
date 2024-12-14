import os
from .SR.sr_api import SR, load_image


class RezMaster:
    def __init__(self, device='cpu'):
        self.sr_api = SR(None)
        self.sr_api.switch_device(device)
        self.ckpt_dir = None
        self.raw_image = None
    
    def set_image(self, img_path):
        self.raw_image = load_image(img_path)
        
    def process(self, scale):
        if self.sr_api.model is None:
            return
        return self.sr_api.pred(self.raw_image, scale)
    
    def set_ckpt_dir(self, ckpt_dir):
        self.ckpt_dir = ckpt_dir
    
    def load_model(self, model_type, data_type):
        ckpt_path = os.path.join(self.ckpt_dir, f'{model_type.value}_{data_type.value}.pth')
        return self.sr_api.load_model(ckpt_path)