# PixeLINK
The ScopeFoundry platform for the camera Pixelink. Model:PL-B771U





## Requirement to install:
"Anaconda"
Python 3.6

## Testing Environment:
Windows 7 

PixeLINK PL-B771U

PixeLINK Software Development Kit 4.2 - Release 8.7.1 

## Parameters 
### Binning

0: Decimation: the camera makes the acquisition only on one pixel for a block of 2x2 pixels

1: Average: the camera makes the acquisition for all the block of 2x2 pixels and then it makes an average all over the four value

2: Bin: the camera makes the acquisition for all the block of 2x2 pixels and then it sums all the 4 value


With Bin Mode the image is brighter than with Decimation and Average Mode.

### Region of Interest (ROI)
The matrix of pixel is divided into blocks of eight pixel, so when you change the region of interest you must choose a value that is multiple of 8

### Frame Rate
The frame rate is from 4.5 to 30 fps, but in the case of binning value equal to 2 and binning mode equal to Decimate the range of the frame rate is from 6.5 to 30 fps









## Code Implementation


The binning attribute of the object cam is a four value array
The first parameter is called Value and it can be 1 or 2. With value “1” we get a normal acquisition all over the pixels. Using the value “2” we get an acquisition with a number of point for image one quarter of the image with value “2”.
The second parameter is called Mode and it can assume value 0,1 or 2, each value stand for a different method of acquisition.
0: Decimation: the camera makes the acquisition only on one pixel for a block of 2x2 pixels
1: Average: the camera makes the acquisition for all the block of 2x2 pixels and then it makes an average all over the four value
2: Bin: the camera makes the acquisition for all the block of 2x2 pixels and then it sums all the 4 value


Data sheet of the camera:https://pixelink.com/products/industrial-cameras/usb-20/pl-b771/


## Acknowledgements
We would like to thank professor Andrea Bassi (https://github.com/andreabassi78) and Michele Castriotta (https://github.com/mikics), whose code provided us a starting point to develop this project (especially for the measurement part)
