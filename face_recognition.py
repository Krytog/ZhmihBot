import cv2 as cv
import sys


def GetFacesFromImage(image_name):
	original_image = cv.imread(image_name)
	grayscale_image = cv.cvtColor(original_image, cv.COLOR_BGR2GRAY)
	face_cascade = cv.CascadeClassifier("dark_magic.xml")	#DON'T RENAME IT OR EVERYTHING WILL BLOW UP

	return face_cascade.detectMultiScale(grayscale_image)


def GetImageSize(image_name):
	image = cv.imread(image_name)
	return image.shape

