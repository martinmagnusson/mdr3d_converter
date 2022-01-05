from ctypes import Array, sizeof
import json
import os.path
from tkinter import DoubleVar
import config
import custom_logging as log
from PIL import Image as ImageProc
import re
import numpy

def ROS(file):
    properties = {}
    with open(file, "r") as f:  # Extract data as dict.
        config.properties = dict(i.strip().split(":", 1) for i in f)
        log.logprint("\ntest dict:" + str(config.properties))
        log.logprint("Opened file: " + str(os.path.realpath(f.name)))
    # Not sure why a .strip has to be applied here again. since its done earlier
    pgm_file_path = os.path.abspath(str(
        config.Selected_file_path_dir) + "/" + str(config.properties["image"].strip()))
    with ImageProc.open(pgm_file_path, mode="r") as pgmf:
        log.logprint("Loading PGM data.")
        pixels = list(pgmf.getdata())
        width, height = pgmf.size
        config.properties.update(dict({"width": width}))
        config.properties.update(dict({"height": height}))
        config.properties.update(dict({"pixels": pixels}))
    log.logprint("\tWidth:" + str(width) + "\n\theight:" +
                 str(height) + "\n\tAmount: \n")
    log.logprint(properties)
    # remove extension from file to make name for convert.

def PCD(file):
    log.logprint("\nConverting from pointcloud")
    with open(file, "r") as f:  # Extract data as dict.
        file_data = f.read()
        config.properties["version"] = re.search(
            "VERSION\s(.*)", file_data).group(1)
        config.properties["fields"] = re.search(
            "FIELDS\s(.*)", file_data).group(1)
        config.properties["type"] = re.search("TYPE\s(.*)", file_data).group(1)
        config.properties["count"] = re.search(
            "COUNT\s(.*)", file_data).group(1)
        config.properties["size"] = re.search("SIZE\s(.*)", file_data).group(1)
        config.properties["width"] = re.search(
            "WIDTH\s(.*)", file_data).group(1)
        config.properties["height"] = re.search(
            "HEIGHT\s(.*)", file_data).group(1)
        config.properties["viewpoint"] = re.search(
            "VIEWPOINT\s(.*)", file_data).group(1)
        config.properties["total_points"] = re.search(
            "POINTS\s(.*)", file_data).group(1)
        config.properties["data_encoding"] = re.search(
            "DATA\s(.*)", file_data).group(1)
        last_line = re.search("(DATA\s.*)", file_data).group(1)
        # config.properties["points"] = re.search(last_line + "\s((.*\n*)*)", file_data).group(1)
        # log.logprint("\ntest points:"+ str(config.properties["points"]))
        log.logprint("Opened file: " + str(os.path.realpath(f.name)))
    with open(file, "r") as f:  # Extract data
        file_matrix = f.readlines()
        matrix = []
        record = False
        for lines in file_matrix:  # find last line, record rows after that in matrix.
            if record == True:
                ##print(lines.rstrip())
                data = lines.split(" ",2)
                #matrix = numpy.append(matrix,data,0)
                matrix.append([float(data[0]),float(data[1]),float(data[2])])
            if str(lines).rstrip() == str(last_line).rstrip() and record == False:
                print("last line found")
                record = True
    log.logprint("Size of matrix is:" + str(len(matrix))) 
    config.properties["list_of_points"] = matrix
    config.matrix_out = matrix
    
def XLM(file):
    log.logprint("\nConverting from 2D Standard")
    json.dumps("2D standard test output")
