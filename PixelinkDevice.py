""" Written by Fabio Mensi and Andrea Spinosa (Polimi).
    Code for creating the device class of ScopeFoundry for the PixeLINK Camera PL-B771U
    03/19
"""
import PixelinkHardware
from pixelink import PixeLINK
binningModeValue={"Decimate": 0, "Average": 1, "Bin": 2}

class PixelinkDev(object):
    
    def __init__(self, camera_id, acquisition_mode, number_frames, exposure_time, gain, binningpx,binning_mode,frame_rate, offset_x, offset_y, img_width, img_height):
        
        self.cam = PixeLINK()
        
        self.cam.streaming = False
        
        self.acquisition_mode = acquisition_mode
        self.number_frames = number_frames
        self.cam.shutter = exposure_time
        self.cam.gain = gain
        self.cam.binning = [binningpx,binningModeValue[binning_mode],binningpx,binningpx]
        self.cam.frame_rate = frame_rate
        self.cam.roi = [offset_x,offset_y,img_width,img_height]
        
    
    def readExposure(self):
        return self.cam.shutter
        
    def readBinning(self):
        return self.cam.binning[0] 
        
    def readBinningMode(self):
        binMode=['Decimate','Average', 'Bin']
        return binMode[int(self.cam.binning[1])]
             
    def readGain(self):
        return self.cam.gain
        
    def readFrameRate(self):    
        return self.cam.frame_rate 
        
    def readOffsetX(self):
        return self.cam.roi[0] 
        
    def readOffsetY(self):
        return self.cam.roi[1] 
       
    def readWidth(self):
        return self.cam.roi[2]
        
    def readHeight(self):
        return self.cam.roi[3] 
    
    def readSerialNumber(self):
        return self.cam._api.GetNumberCameras()[0]
    
    def readTemp(self):
        return self.cam.sensor_temperature

    #ReadAcquisition and ReadNumberFrames update the parameters that will be used in PixelinkMeasurement
    def readAcquisition(self):
        return self.acquisition_mode
        
    def readNumberFrames(self):   
        return self.number_frames
    
    
    
    def setExposure(self, exposure_time):
        self.cam.frame_rate = min(1/exposure_time, self.cam.frame_rate)
        self.cam.shutter = exposure_time
            
    def setBinning(self, binningpx):
        self.cam.binning = [binningpx,self.cam.binning[1],binningpx,binningpx]
     
    def setBinningMode(self, binning_mode ):
        self.cam.binning=[self.cam.binning[0],binningModeValue[binning_mode],self.cam.binning[2],self.cam.binning[3]]
    
    def setGain(self, gain):
        self.cam.gain = gain
        
    def setFrameRate(self, frame_rate):
        #self.cam.streaming = False
        if frame_rate < 1/self.cam.shutter:
            self.cam.frame_rate = frame_rate
        else:
            print("Framerate incompatible with exposure time")
      
        
    ## To select a different Region of Interest (ROI)  you can choose only values that are multiple of 8, the pixel matrix is divided into blocks of 8 units 
    def setOffsetX(self, offset_x):
        if (offset_x+self.cam.roi[2] > 1280):
            self.cam.roi = [offset_x, self.cam.roi[1], 1280 - offset_x, self.cam.roi[3]]
        else:
            self.cam.roi = [offset_x, self.cam.roi[1], self.cam.roi[2], self.cam.roi[3]]
        
    def setOffsetY(self, offset_y):
        if(offset_y+self.cam.roi[3] > 1024):
            self.cam.roi = [self.cam.roi[0], offset_y, self.cam.roi[2], 1024 - offset_y]
        else:
            self.cam.roi = [self.cam.roi[0], offset_y, self.cam.roi[2], self.cam.roi[3]]
      
    def setWidth(self, img_width):
        if (img_width+self.cam.roi[0] > 1280):
            self.cam.roi = [1280 - img_width, self.cam.roi[1], img_width, self.cam.roi[3]]
        else:
            self.cam.roi = [self.cam.roi[0], self.cam.roi[1], img_width, self.cam.roi[3]]
        
    def setHeight(self, img_height):
        if (img_height+self.cam.roi[1] > 1024):
            self.cam.roi = [self.cam.roi[0], 1024 - img_height, self.cam.roi[2], img_height]
        else:
            self.cam.roi = [self.cam.roi[0], self.cam.roi[1], self.cam.roi[2], img_height]
        
    #SetAcquisition and SetNumberFrames set the parameters that will be used in PixelinkMeasurement
    def setAcquisition(self, acquisition_mode):
        self.acquisition_mode = acquisition_mode
        
    def setNumberFrames(self, number_frames):   
        self.number_frames = number_frames
        
        
    def close_camera(self):
        self.cam.close()
        
        
        
    
        
if __name__ == '__main__':
    import sys
    
    pippo = PixelinkDev(0,'a',1,0.01,0,1,20,0,0,1280,1024)
    print(pippo.cam.grab())
    
        
