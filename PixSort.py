from PIL import Image
from sys import argv
from random import randint

def main(img_name, output_img, black, sort_band, vert = False, rev = False, xor = False):
    # test input image
    img = Image.open(img_name)

    # get input pixels
    if vert:
        img = img.rotate(90)
    pixels = list(img.getdata())

    # begin selectively sorting image data
    sort_buffer = []
    sorted_pixels = []

    for p in pixels:
        # pixels that are "darker" than our threshold go into the buffer
        if p[sort_band] < black[sort_band]:
            sort_buffer.append(p)

        # when we see a lighter pixel, we sort or otherwise manipulate the current buffer based on parameters.
        # the sorted buffer is then added to the output pixels and cleared,
        # and the lighter pixel is simply added to output as-is
        else:
            if rev:
                sort_buffer = reversed(sorted(sort_buffer, key = lambda x: x[sort_band]))
            else:
                sort_buffer = sorted(sort_buffer, key = lambda x: x[sort_band])

            if xor:
                sort_buffer = [tuple(x ^ 255 for x in sp) for sp in sort_buffer]

            sorted_pixels += sort_buffer
            sort_buffer = []
            sorted_pixels.append(p)

    # write sorted pixels to image and save
    print(sorted_pixels[:10])
    img.putdata(sorted_pixels)
    if vert:
        img = img.rotate(-90)
    img.save(output_img)

if __name__ == "__main__":
    # todo: Get parameters via GUI/CLI input rather than hard-coding
    red = 100
    green = 100
    blue = 100
    black = tuple([red, green, blue])

    band = 1
    vert = 1
    rev = 0
    xor = 0

    img_name = "images/image0.jpg"
    output_img_name = "images_out/image0_sorted_" + str(band) + str(vert) + str(rev) + str(xor) + ".jpg"

    main(img_name, output_img_name, black, band, vert, rev, xor)
