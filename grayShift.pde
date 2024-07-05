PImage img;

//keyword argument variables
String filepath = null; 
Integer w = null;
Integer h = null;

//tonal separation variables
int low;
int mid;
int high;

//color channel separation variabls for low tones
float rl;
float gl;
float bl;

//color channel separation variabls for mid tones
float rm;
float gm;
float bm;

//color channel separation variabls for high tones
float rh;
float gh;
float bh;

FloatList redlow;
FloatList greenlow;
FloatList bluelow;

float redlowSum;
float greenlowSum;
float bluelowSum;

float redlowOffset;
float greenlowOffset;
float bluelowOffset;

FloatList redmid;
FloatList greenmid;
FloatList bluemid;

float redmidSum;
float greenmidSum;
float bluemidSum;

float redmidOffset;
float greenmidOffset;
float bluemidOffset;

FloatList redhigh;
FloatList greenhigh;
FloatList bluehigh;

float redhighSum;
float greenhighSum;
float bluehighSum;

float redhighOffset;
float greenhighOffset;
float bluehighOffset;

//low
int r1;
int r2;
//mid
int r3;
int r4;
//high
int r5;
int r6;

public void settings() {
    // Parse command-line arguments
  if (args != null) {
    for (int i = 0; i < args.length; i++) {
      String[] parts = args[i].split("=");
      if (parts.length == 2) {
        String key = parts[0];
        String value = parts[1];
        if (key.equals("filepath")) {
          filepath = value;
        } else if (key.equals("w")) {
          w = int(value);
        } else if (key.equals("h")) {
          h = int(value);
        } 
      }
    }
  }
  
  //validate keyword arguments
  if (filepath == null) {
    throw new Error("Filepath {filepath} must be defined within the sketch or passed as a keyword argument when running from command line");
  }
   if (w == null) {
    throw new Error("Width {w} must be defined within the sketch or passed as a keyword argument when running from command line");
  }
   if (h == null) {
    throw new Error("Height {h} must be defined within the sketch or passed as a keyword argument when running from command line");
  }

  size(w,h);
}

void setup() {

  img = loadImage(filepath);

  img.loadPixels();

  redlow = new FloatList();
  greenlow = new FloatList();
  bluelow = new FloatList();

  redmid = new FloatList();
  greenmid = new FloatList();
  bluemid = new FloatList();

  redhigh = new FloatList();
  greenhigh = new FloatList();
  bluehigh = new FloatList();

  redlowSum = 0;
  greenlowSum = 0;
  bluelowSum = 0;

  redmidSum = 0;
  greenmidSum = 0;
  bluemidSum = 0;

  redhighSum = 0;
  greenhighSum = 0;
  bluehighSum = 0;

  //low = 25% B
  r1 = 54;
  r2 = 74;
  //mid = 50% B
  r3 = 119;
  r4 = 139;
  //high = 75% B
  r5 = 183;
  r6 = 203;

  // -------------------------------------------------------------------------------- mid
  for (int ii = 0; ii < img.width * img.height; ii++) {      // storing expected neutral pixels

    rm = red(img.pixels[ii]);
    gm = green(img.pixels[ii]);
    bm = blue(img.pixels[ii]);

    if ((rm >= r3 && rm <= r4) && (gm >= r3 && gm <= r4) && (bm >= r3 && bm <= r4)) {

      mid++;

      redmid.append(rm);
      greenmid.append(gm);
      bluemid.append(bm);
    }
  }

  for (int pp = 0; pp < mid; pp++ ) {       //distance from gray and average offset to apply change to gray

    redmidSum = redmidSum + redmid.get(pp);
    greenmidSum = greenmidSum + greenmid.get(pp);
    bluemidSum = bluemidSum + bluemid.get(pp);
  }
  
    redmidOffset = redmidSum / mid - 129;
    greenmidOffset = greenmidSum / mid - 129;
    bluemidOffset = bluemidSum / mid - 129;

  //---------------------------------------------------------------------low

  for (int i = 0; i < img.width * img.height; i++) {

    rl = red(img.pixels[i]);
    gl = green(img.pixels[i]);
    bl = blue(img.pixels[i]);

    if ((rl >= r1 && rl <= r2) && (gl >= r1 && gl <= r2) && (bl >= r1 && bl <= r2)) {

      low++;

      redlow.append(rl);
      greenlow.append(gl);
      bluelow.append(bl);
      
    }
  }

  for (int p = 0; p < low; p++ ) {

    redlowSum = redlowSum + redlow.get(p);
    greenlowSum = greenlowSum + greenlow.get(p);
    bluelowSum = bluelowSum + bluelow.get(p);
  }

  redlowOffset = redlowSum / low - 64;
  greenlowOffset = greenlowSum / low - 64;
  bluelowOffset = bluelowSum / low - 64;

  //----------------------------------------------------------------high
  for (int iii = 0; iii < img.width * img.height; iii++) {

    rh = red(img.pixels[iii]);
    gh = green(img.pixels[iii]);
    bh = blue(img.pixels[iii]);

    if ((rh >= r5 && rh <= r6) && (gh >= r5 && gh <= r6) && (bh >= r5 && bh <= r6)) {

      high++;

      redhigh.append(rh);
      greenhigh.append(gh);
      bluehigh.append(bh);
    }
  }

  for (int ppp = 0; ppp < high; ppp++ ) {

    redhighSum = redhighSum + redhigh.get(ppp);
    greenhighSum = greenhighSum + greenhigh.get(ppp);
    bluehighSum = bluehighSum + bluehigh.get(ppp);
  }

  redhighOffset = redhighSum / high - 193;
  greenhighOffset = greenhighSum / high - 193;
  bluehighOffset = bluehighSum / high - 193;

  float redAvgOffset = (redlowOffset + redmidOffset + redhighOffset) / 3;
  float greenAvgOffset = (greenlowOffset + greenmidOffset + greenhighOffset) / 3;
  float blueAvgOffset = (bluelowOffset + bluemidOffset + bluehighOffset) / 3;


  for (int iii = 0; iii < img.width * img.height; iii++) {

    rh = red(img.pixels[iii]);
    gh = green(img.pixels[iii]);
    bh = blue(img.pixels[iii]);

    img.pixels[iii] = color(round(rh - redAvgOffset), round(gh - greenAvgOffset), round(bh - blueAvgOffset));
  }

  updatePixels();
  println(redlowOffset, greenlowOffset, bluelowOffset);
  println(redmidOffset, greenmidOffset, bluemidOffset);
  println(redhighOffset, greenhighOffset, bluehighOffset);

  img.save(split(filepath, ".")[0] + "_shifted" + "." + split(filepath, ".")[1]);
  exit();
}


void draw () {

}
