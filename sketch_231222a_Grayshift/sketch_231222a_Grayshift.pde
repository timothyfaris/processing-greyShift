PImage img;

float r;
float g;
float b;

int gray;

FloatList reds;
FloatList greens;
FloatList blues;

float redSum;
float greenSum;
float blueSum;

float redOffset;
float greenOffset;
float blueOffset;

int r1;
int r2;
int r3;

void setup() {
  size(3000, 2000); //canvas size should reflect pixel dimensions of photo
  img = loadImage("frame705.jpg"); //sketch must be saved, and the image must be within a folder named "data" witin the sketch folder.
  
  //  example_2_unfiltered.jpg   MAME0808.JPG         IMG_E4204.JPG        example_1_unfiltered.jpg
  //  3.0 -5.0 3.0 works         9.0 0.0 -9.0 works   0.0 3.0 -2.0 works   4.0 -2.0 -4.0 does not work
  
  img.loadPixels();

  reds = new FloatList();
  greens = new FloatList();
  blues = new FloatList();

  redSum = 0;
  greenSum = 0;
  blueSum = 0;

  r1 = 118;  // (128,128,128) is ~ 50% gray, so this range considers
  r2 = 138;  // more pixels than only those that are exactly (128,128,128)

  r3 = 128;

  for (int i = 0; i < img.width * img.height; i++) {

    r = red(img.pixels[i]);
    g = green(img.pixels[i]);
    b = blue(img.pixels[i]);

    if ((r >= r1 && r <= r2) && (g >= r1 && g <= r2) && (b >= r1 && b <= r2)) {

      gray++;

     reds.append(r);
     greens.append(g);
     blues.append(b);
    }
  }

  for (int p = 0; p < gray; p++ ) {

    redSum = redSum + reds.get(p);
    greenSum = greenSum + greens.get(p);
    blueSum = blueSum + blues.get(p);
  }

    redOffset = redSum / gray - 128;
    greenOffset = greenSum / gray - 128;
    blueOffset = blueSum / gray - 128;

  for (int i = 0; i < img.width * img.height; i++) {

    r = red(img.pixels[i]);
    g = green(img.pixels[i]);
    b = blue(img.pixels[i]);
    
    
    
    
  // if avg gray value is between 118 - 127, then add offset (needs to be defined per channel)
  // else if avg gray is between 128 - 138, subtract offset
  
  // needs to be more sophisitcated in reference to specific color channels.. if deviation is disproportionately green, subtract green, add red and blue.. or something along those lines.
  
  // would it be beneficial to align more closely with Photoshop's color balance interface? Automating sliders to adjust between [cyan - red] [green - magenta] [yellow - blue]
  // Photoshop also separates this tonal balance between Shadows, Midtones, and Highlights.. how? along with a "Preserve Luminosity" feature. This feature could likely be leveraged via the brightness channel in Processing.
  // not actually a subtraction of RGB but rather an addition of CMY
  
  //Need to separate Shadows, Mids, Highlights - examine each channel
  //how do you define these separations?
  
  
  // Red  = (255,0,0)      Green   = (0,255,0)      Blue   = (0,0,255)
  // Cyan = (0,255,255)    Magenta = (255,0,255)    Yellow = (255,255,0)
  
  //if (redOffset > 1 || greenOffset < 1 || blueOffset < 1) {
  
  //if ((redSum >= r1 && redSum <= r3) && (greenSum >= r1 && greenSum <= r3) && (blueSum >= r1 && blueSum <= r3)) {
    
    img.pixels[i] = color(round(r - redOffset), round(g - greenOffset), round(b - blueOffset));
  //} else {
  //  img.pixels[i] = color(r + redOffset, g + greenOffset, b + blueOffset);
  //}
  
  
  
  
  
    updatePixels();
  }
  println(redOffset,greenOffset,blueOffset); 
}

void draw () {
  image(img, 0, 0, 3000, 2000); //reflect same size from above
  if (mousePressed) {
    saveFrame("output/frame###.jpg");
  }
}
