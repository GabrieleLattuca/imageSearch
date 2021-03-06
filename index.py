# import the necessary packages
from colordescriptor import ColorDescriptor
import argparse
import glob
import cv2
 
# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-d", "--dataset", required = True,
	help = "Path to the directory that contains the images to be indexed")
ap.add_argument("-i", "--index", required = True,
	help = "Path to where the computed index will be stored")
ap.add_argument("-m", "--mask", required = True,
	help = "Path to image mask (same size as images) to break into a grid")
ap.add_argument("-g", "--gridsize", required = True,
	help = "Dimension for a single width/height for the square grid mask")
args = vars(ap.parse_args())
 
# initialize the color descriptor
cd = ColorDescriptor((8, 12, 3),args["mask"],args["gridsize"])

# open the output index file for writing
output = open(args["index"], "w")

# use glob to grab the image paths and loop over them
count=1
imagePaths = glob.glob(args["dataset"] + "/*.png")
for imagePath in imagePaths:
        print "Extracting for %s of %s..." %(count,len(imagePaths))
	# extract the image ID (i.e. the unique filename) from the image
	# path and load the image itself
	imageID = imagePath[imagePath.rfind("/") + 1:]
	image = cv2.imread(imagePath)
 
	# describe the image
	features = cd.describe(image)
 
	# write the features to file
	features = [str(f) for f in features]
	output.write("%s,%s\n" % (imageID, ",".join(features)))
        count+=1
 
# close the index file
output.close()
