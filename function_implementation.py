import os
import random
from face_recognition import GetFacesFromImage
from face_recognition import GetImageSize


def InvokeImageProcessor(input_name, output_name, argument):
	command = "./image_processor " + input_name + " " + output_name + " " + argument
	os.system(command)
	return


def ConvertToFit(input_name, output_name):
	command = "convert " + input_name + " -define bmp:format=bmp3 -compress none " + output_name
	os.system(command)
	return


def PrepareToSend(input_name, output_name):
	command = "convert " + input_name + " -compress none " + output_name
	os.system(command)
	return


def DeleteTemp(name):
	os.system("rm " + name)
	return


def ClearAfterPhotoSend(name):
	os.system("rm files/outputs/" + name)
	os.system("rm files/inputs/" + name)
	return


def HandleImage(input_name, output_name, argument):	#THIS FUNCTION IS FOR DEBUGGING ONLY! USING IT IN BOT WILL CAUSE HORRIBLE ERRORS!
	ConvertToFit(input_name, "_temp.bmp")
	InvokeImageProcessor("_temp.bmp", "_out.bmp", argument)
	DeleteTemp("_temp.bmp")
	PrepareToSend("_out.bmp", output_name)
	DeleteTemp("_out.bmp")
	return


def ZhmihImage(input_name, output_name, id = 0):
	id = str(id)
	faces = GetFacesFromImage(input_name)
	ConvertToFit(input_name, id + "_temp.bmp")
	image_height = GetImageSize(input_name)[0]
	image_processor_prompt = ""
	for (begin_x, begin_y, width, height) in faces:
		x_center = begin_x + width / 2
		y_center = begin_y + height / 2
		y_center = image_height - y_center
		radius = max(width, height) * 1.25
		intensity = random.uniform(0.6, 0.9)
		image_processor_prompt += (" -zhmih " + str(int(x_center)) + " " + str(int(y_center)) + " " + str(int(radius)) + " " + str(intensity))
	image_processor_prompt += " -ultzhmih 10 0.55"
	InvokeImageProcessor(id + "_temp.bmp", id + "_out.bmp", image_processor_prompt)
	DeleteTemp(id + "_temp.bmp")
	PrepareToSend(id + "_out.bmp", output_name)
	DeleteTemp(id + "_out.bmp")
	return


def AddUpperCaption(input_name, output_name, caption):
	prompt = "convert " + input_name + " -stroke black -strokewidth 4 -font Ubuntu-Mono-Bold -pointsize 96 -fill white -gravity north -annotate +0+0" + " '" + caption + "' " + output_name
	os.system(prompt)
	return

def AddLowerCaption(input_name, output_name, caption):
	prompt = "convert " + input_name + " -stroke black -strokewidth 4 -font Ubuntu-Mono-Bold -pointsize 96 -fill white -gravity south -annotate +0+0" + " '" + caption + "' " + output_name
	os.system(prompt)
	return

