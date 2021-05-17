Blob[] blobs = new Blob[6];
float radius = 120.0; 
void setup() {
  size(640, 360);
  colorMode(HSB);
  //for (int i = 0; i < blobs.length; i++) {
    blobs[0] = new Blob(250,150,radius);
    blobs[1] = new Blob(250,220,radius);
    blobs[2] = new Blob(320,150,radius);
    blobs[3] = new Blob(320,220,radius);
    blobs[4] = new Blob(390,150,radius);
    blobs[5] = new Blob(390,220,radius);
 // }
}

void draw() {
  background(51);

  loadPixels();
  for (int x = 0; x < width; x++) {
    for (int y = 0; y < height; y++) {
      int index = x + y * width;
      float sum = 0;
      for (Blob b : blobs) {
        float d = dist(x, y, b.pos.x, b.pos.y);
        sum += 10 * b.r / d;
      }
      if(sum>255)println(sum);
      pixels[index] = color(sum, 255, 255);
    }
  }

  updatePixels();

  for (Blob b : blobs) {
    b.update();
    b.show();
  }
}