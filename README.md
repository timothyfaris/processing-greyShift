greyShift locates pixels within a specified range of 50% gray. These neutral-ish pixels are examined via RGB color channels. The average deviance from 50% gray is calculated and then applied to every pixel in the image, functioning as an image specific tone correction.

If you would like to try this local app using your own images, download both the Processing Development Environment ([processing.org/download](https://processing.org/download)) and this repository. Place this repository into the main Processing folder. 

The app can then be run from a terminal using the prompt <span style="color: #0066ffff;">processing-java --sketch="C:\Users\User\Desktop\Processing\greyShift" --run filepath="C:\Users\User\"path to image file"" w=(number of pixels wide) h=(number of pixels high) scalar=0.2</span>

** 0.2 is a nice place to start with scalar value but this can be modified.
### Examples
![example_01](/assets/fish.gif)

![example_02](/assets/egret.gif)

### Reference List

https://github.com/thomaseleff

https://stackoverflow.com/questions/62376327/using-processing-for-image-visualization-pixel-color-thresholds