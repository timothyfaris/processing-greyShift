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


void setup() {
  size(3000, 2000); //canvas size should reflect pixel dimensions of photo
  img = loadImage("IMG_7773.jpg"); //sketch must be saved, and the image must be within a folder named "data" witin the sketch folder.
  img.loadPixels();

  reds = new FloatList();
  greens = new FloatList();
  blues = new FloatList();

  redSum = 0;
  greenSum = 0;
  blueSum = 0;

  r1 = 118;  // (128,128,128) is ~ 50% gray, so this range considers
  r2 = 138;  // more pixels than only those that are exactly (128,128,128)


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

    redOffset = round(redSum / gray - 128);
    greenOffset = round(greenSum / gray - 128);
    blueOffset = round(blueSum / gray - 128);

  for (int i = 0; i < img.width * img.height; i++) {

    r = red(img.pixels[i]);
    g = green(img.pixels[i]);
    b = blue(img.pixels[i]);

    img.pixels[i] = color(r + redOffset, g + greenOffset, b + blueOffset);

    updatePixels();
  }
}

void draw () {
  image(img, 0, 0, 3000, 2000); //reflect same size from above
  if (mousePressed) {
    saveFrame("output/frame###.jpg");
  }
}
