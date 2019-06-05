""" Written by Fabio Mensi and Andrea Spinosa (Polimi).
    Code for creating the hardware class of ScopeFoundry for the PixeLINK Camera PL-B771U
    03/19
"""
from ScopeFoundry import HardwareComponent
import PixelinkDevice
from PixelinkDevice import PixelinkDev

class PixelinkHard(HardwareComponent):
    
    def setup(self):
        
        self.camera = self.add_logged_quantity('camera', dtype=int, si=False, ro=1, initial = 0 )
        self.temperature = self.add_logged_quantity('temperature', dtype=float, si=False, ro=1, unit = 'Celsius')
        self.exposure_time = self.add_logged_quantity('exposure_time', dtype = float, si = False, ro = 0, unit = 'sec', initial = 0.01)
        self.gain = self.add_logged_quantity('gain', dtype = float, si = False, ro = 0, unit = 'dB', initial = 0)
        self.acquisition_mode = self.add_logged_quantity('acquisition_mode', dtype = str, choices = ["fixed_length", "run_till_abort"], initial = "fixed_length")
        self.binningpx = self.add_logged_quantity('binningpx', dtype = int, choices = [1, 2], initial = 1)
        self.binning_mode = self.add_logged_quantity('binning_mode', dtype = str, choices = ["Decimate", "Average","Bin"], initial = "Decimate")
        self.number_frames = self.add_logged_quantity("number_frames", dtype = int, si = False, ro = 0, initial = 1)
        self.frame_rate = self.add_logged_quantity("frame_rate", dtype = float, si = False, ro = 0, initial = 20.0)
        self.offset_x = self.add_logged_quantity("offset_x", dtype=int, si = False, ro= 0, initial = 0)
        self.offset_y = self.add_logged_quantity("offset_y", dtype=int, si = False, ro= 0, initial = 0)
        self.img_width = self.add_logged_quantity("img_width", dtype=int, si = False, ro= 0, initial = 1280)
        self.img_height = self.add_logged_quantity("img_height", dtype=int, si = False, ro= 0, initial = 1024) 
        
        
        
    def connect(self):
        
        self.pixelink = PixelinkDev(camera_id=0, acquisition_mode=self.acquisition_mode.val, number_frames=self.number_frames.val, exposure_time=self.exposure_time.val, gain=self.gain.val, binningpx=self.binningpx.val,binning_mode=self.binning_mode.val, frame_rate=self.frame_rate.val, offset_x=self.offset_x.val, offset_y=self.offset_y.val, img_width=self.img_width.val, img_height=self.img_height.val) #manca il framerate 
        
        self.camera.hardware_read_func = self.pixelink.readSerialNumber
        self.temperature.hardware_read_func = self.pixelink.readTemp
        self.offset_x.hardware_read_func = self.pixelink.readOffsetX
        self.offset_y.hardware_read_func = self.pixelink.readOffsetY
        self.img_width.hardware_read_func = self.pixelink.readWidth
        self.img_height.hardware_read_func = self.pixelink.readHeight
        self.exposure_time.hardware_read_func = self.pixelink.readExposure
        self.gain.hardware_read_func = self.pixelink.readGain
        self.acquisition_mode.hardware_read_func = self.pixelink.readAcquisition
        self.number_frames.hardware_read_func = self.pixelink.readNumberFrames
        self.binningpx.hardware_read_func = self.pixelink.readBinning
        self.frame_rate.hardware_read_func = self.pixelink.readFrameRate
        self.binning_mode.hardware_read_func = self.pixelink.readBinningMode
        
        self.offset_x.hardware_set_func = self.pixelink.setOffsetX
        self.offset_y.hardware_set_func = self.pixelink.setOffsetY
        self.img_width.hardware_set_func = self.pixelink.setWidth
        self.img_height.hardware_set_func = self.pixelink.setHeight
        self.exposure_time.hardware_set_func = self.pixelink.setExposure
        self.gain.hardware_set_func = self.pixelink.setGain
        self.acquisition_mode.hardware_set_func = self.pixelink.setAcquisition
        self.number_frames.hardware_set_func = self.pixelink.setNumberFrames
        self.binningpx.hardware_set_func = self.pixelink.setBinning
        self.frame_rate.hardware_set_func = self.pixelink.setFrameRate
        self.binning_mode.hardware_set_func = self.pixelink.setBinningMode
        
        self.read_from_hardware()    
        
        
    def disconnect(self):
        
        if hasattr(self, 'pixelink'):
            self.pixelink.close_camera()
            del self.pixelink
                
        for lq in self.settings.as_list():
            lq.hardware_read_func = None
            lq.hardware_set_func = None 
