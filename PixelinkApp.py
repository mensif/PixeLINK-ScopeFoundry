from ScopeFoundry import BaseMicroscopeApp

class PixelinkA(BaseMicroscopeApp):

    # this is the name of the microscope that ScopeFoundry uses 
    # when storing data
    name = 'pixelink_app'
    
    # You must define a setup function that adds all the 
    #capablities of the microscope and sets default settings
    def setup(self):
        
        #Add App wide settings
        
        #Add hardware components
        print("Adding Hardware Components")
        from PixelinkHardware import PixelinkHard
        self.add_hardware(PixelinkHard(self))

        #Add measurement components
        print("Create Measurement objects")
        from PixelinkMeasurement import PixelinkMeas
        self.add_measurement(PixelinkMeas(self))

        # Connect to custom gui
        
        # load side panel UI
        
        # show ui
        self.ui.show()
        self.ui.activateWindow()


if __name__ == '__main__':
    import sys
    
    app = PixelinkA(sys.argv)
    sys.exit(app.exec_())
