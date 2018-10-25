import cv2
import numpy as np
import sys
from datetime import datetime


def morph_operator(im, op, kx=3, ky=3):
    w, h = im.shape

    out_mat = np.zeros((im.shape[0], im.shape[1]))

    for x in range(w):
        for y in range(h):
            down, left, right, up = get_neighbors(h, kx, ky, w, x, y)

            # neighbors_matrix = im[left:right, up:down]
            neighbors_list = [im[left][y], im[left+1][y],
                              im[right][y], im[right-1][y],
                              im[x][y],
                              im[x][up], im[x][up+1],
                              im[x][down], im[x][down-1]]

            #out_mat[x, y] = max(neighbors_list)
            if found_blob(neighbors_list):
                if op == "DILATION":
                    out_mat[x, y] = 255
                elif len(set(neighbors_list)) == 1:
                    out_mat[x, y] = neighbors_list[0]
                else:
                    out_mat[x, y] = 0
            else:
                out_mat[x, y] = im[x][y]

    # cv2.imshow('asd', out_mat)
    # cv2.waitKey(0)
    return out_mat


def found_blob(items):
    # return len(set(items)) == 1
    for pixel in items:
        if pixel == 255:
            return True


def get_neighbors(h, kx, ky, w, x, y):
    left = max(0, x - kx)
    up = max(0, y - ky)
    right = min(w - 1, x + kx)
    down = min(h - 1, y + ky)
    return down, left, right, up


def main():
    from argparse import ArgumentParser

    parser = ArgumentParser()

    parser.add_argument("-i", "--image", dest="image",
                        help="specify the name of the image", metavar="IMAGE")
    parser.add_argument("-x", "--x_size", dest="x_size",
                        help="specify scale size (x)", metavar="RESAMPLE SIZE")
    parser.add_argument("-y", "--y_size", dest="y_size",
                        help="specify scale size (y)", metavar="RESAMPLE SIZE")
    parser.add_argument("-m", "--morph_method", dest="morph_method",
                        help="specify the morph method (dialation or erosion)",
                        metavar="MORPHOLOGICAL METHOD")

    args = parser.parse_args()

    # Load image
    if args.image is None:
        print("Please specify the name of image")
        print("use the -h option to see usage information")
        sys.exit(2)
    else:
        image_name = args.image.split(".")[0]
        input_image = cv2.imread(args.image, 0)


    # Check interpolate method argument

    if args.morph_method is None:
        print("Interpolation method not specified, using default=EROSION")
        print("use the -h option to see usage information")
        morph_method = "EROSION"

    else:
        if args.morph_method not in ["EROSION", "DILATION"]:
            print("Invalid Morph method, using default=EROSION")
            print("use the -h option to see usage information")
            morph_method = "EROSION"
        else:
            morph_method = args.morph_method

    # Write output file
    outputDir = 'output/'

    resampled_image = morph_operator(input_image, morph_method)
    output_image_name = outputDir + image_name + morph_method + datetime.now().strftime("%m%d-%H%M%S") + ".jpg"
    cv2.imwrite(output_image_name, resampled_image)


if __name__ == "__main__":
    main()
