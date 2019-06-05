""" Written by Fabio Mensi and Andrea Spinosa (Polimi).
    Code for creating the measurement class of ScopeFoundry for the PixeLINK Camera PL-B771U
    03/19
"""

from ScopeFoundry import Measurement
from ScopeFoundry.helper_funcs import sibling_path, load_qt_ui_file
from ScopeFoundry import h5_io
import pyqtgraph as pg
import numpy as np


class PixelinkMeas(Measurement):
    name = "pixelink_image"

    def setup(self):

        self.ui_filename = sibling_path(__file__, "form.ui")

        self.ui = load_qt_ui_file(self.ui_filename)
        self.settings.New('save_h5', dtype=bool, initial=False, hardware_set_func=self.setSaveH5,
                          hardware_read_func=self.getSaveH5, reread_from_hardware_after_write=True)
        self.settings.New('refresh_period', dtype=float, unit='s', spinbox_decimals=4, initial=0.02,
                          hardware_set_func=self.setRefresh, vmin=0)
        self.settings.New('autoRange', dtype=bool, initial=True, hardware_set_func=self.setautoRange)
        self.settings.New('autoLevels', dtype=bool, initial=True, hardware_set_func=self.setautoLevels)
        self.settings.New('level_min', dtype=int, initial=0, hardware_set_func=self.setminLevel,
                          hardware_read_func=self.getminLevel)
        self.settings.New('level_max', dtype=int, initial=255, hardware_set_func=self.setmaxLevel,
                          hardware_read_func=self.getmaxLevel)
        self.camera = self.app.hardware['PixelinkHard']

        self.autoRange = self.settings.autoRange.val
        self.display_update_period = self.settings.refresh_period.val
        self.autoLevels = self.settings.autoLevels.val
        self.level_min = self.settings.level_min.val
        self.level_max = self.settings.level_max.val

    def setup_figure(self):
        """
        Runs once during App initialization, after setup()
        This is the place to make all graphical interface initializations,
        build plots, etc.
        """

        # connect ui widgets to measurement/hardware settings or functions
        self.ui.start_pushButton.clicked.connect(self.start)
        self.ui.interrupt_pushButton.clicked.connect(self.interrupt)
        self.settings.save_h5.connect_to_widget(self.ui.save_h5_checkBox)

        # connect ui widgets of live settings
        self.settings.autoLevels.connect_to_widget(self.ui.autoLevels_checkBox)
        self.settings.autoRange.connect_to_widget(self.ui.autoRange_checkBox)
        self.settings.level_min.connect_to_widget(
            self.ui.min_doubleSpinBox)  
        self.settings.level_max.connect_to_widget(
            self.ui.max_doubleSpinBox) 

        # Set up pyqtgraph graph_layout in the UI
        self.imv = pg.ImageView()
        self.ui.plot_groupBox.layout().addWidget(self.imv)

        # Image initialization
        self.image = np.zeros((int(self.camera.img_width.val), int(self.camera.img_height.val)), dtype=np.uint8)

        # Create PlotItem object (a set of axes)

    def update_display(self):
        """
        Displays the numpy array called self.image.
        This function runs repeatedly and automatically during the measurement run,
        its update frequency is defined by self.display_update_period.
        """

        if self.autoLevels == False:
            self.imv.setImage((self.image).T, autoLevels=self.settings.autoLevels.val,
                              autoRange=self.settings.autoRange.val, levels=(self.level_min, self.level_max))
        else:
            self.imv.setImage((self.image).T, autoLevels=self.settings.autoLevels.val,
                              autoRange=self.settings.autoRange.val)
            self.settings.level_min.read_from_hardware()
            self.settings.level_max.read_from_hardware()

    def run(self):

        self.eff_img_height = int(self.camera.img_height.val / self.camera.binningpx.val)
        self.eff_img_width = int(self.camera.img_width.val / self.camera.binningpx.val)

        self.image = np.zeros((self.eff_img_width, self.eff_img_height), dtype=np.uint8)
        self.image[0, 0] = 1  # Otherwise we get the "all zero pixels" error (we should modify pyqtgraph...)
        try:

            self.camera.read_from_hardware()

            self.camera.pixelink.cam.streaming = True
            
            n_frames = self.camera.pixelink.number_frames

            index = 0

            if self.camera.acquisition_mode.val == "fixed_length":
                
                buffer = np.zeros(( n_frames, self.eff_img_height, self.eff_img_width))
                buffer_ticks = np.zeros(n_frames)

                if self.settings['save_h5']:
                    self.initH5()
                    print("\n \n ******* \n \n Saving :D !\n \n *******")

                while index < n_frames:

                    self.image = self.camera.pixelink.cam.grab()
                    buffer[index,:,:] =self.image
                    buffer_ticks[index] = time.time()
                     
                    if self.interrupt_measurement_called:
                        break
                    index += 1
                    
                    self.settings['progress'] = index * 100. / n_frames
                    
                index_save = 0
                
                if self.settings['save_h5']:
                    while index_save < index:
                       
                        self.image_h5[index_save, :, :] = buffer[index_save,:,:]  # saving to the h5 dataset
                        self.h5file.flush()
                        index_save += 1
                      
            elif self.camera.acquisition_mode.val == "run_till_abort":
                
                save = True
                
                while not self.interrupt_measurement_called:
                    
                    self.image = self.camera.pixelink.cam.grab()
                    

        finally:

            self.camera.pixelink.cam.streaming = False
            
            if (self.camera.acquisition_mode.val == "fixed_length") and (self.settings['save_h5']):
                self.h5file.close()  # close h5 file
                
                

    def setRefresh(self, refresh_period):
        self.display_update_period = refresh_period

    def setautoRange(self, autoRange):
        self.autoRange = autoRange

    def setautoLevels(self, autoLevels):
        self.autoLevels = autoLevels

    def setminLevel(self, level_min):
        self.level_min = level_min

    def setmaxLevel(self, level_max):
        self.level_max = level_max

    def getminLevel(self):
        return self.imv.levelMin

    def getmaxLevel(self):
        return self.imv.levelMax

    def setSaveH5(self, save_h5):
        self.settings.save_h5 = save_h5
        
    def getSaveH5(self):
        return self.settings.save_h5


    def initH5(self):
        """
        Initialization operations for the h5 file.
        """

        self.h5file = h5_io.h5_base_file(app=self.app, measurement=self)
        self.h5_group = h5_io.h5_create_measurement_group(measurement=self, h5group=self.h5file)
        img_size = self.image.shape
        length = self.camera.pixelink.number_frames
        self.image_h5 = self.h5_group.create_dataset(name='t0/c0/image',
                                                     shape=(self.camera.pixelink.number_frames, self.eff_img_height, self.eff_img_width),
                                                     dtype=self.image.dtype)
       
        self.image_h5.dims[0].label = "z"
        self.image_h5.dims[1].label = "y"
        self.image_h5.dims[2].label = "x"

        self.image_h5.attrs['element_size_um'] = [1, 1, 1]

    
