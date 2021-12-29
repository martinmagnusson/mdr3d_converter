from ctypes import Array, sizeof
import json
import os.path
from tkinter import DoubleVar
import config
import custom_logging as log
from PIL import Image as ImageProc
import re


def ROS(file):
    log.logprint("\nConverting from ROS Gridmap")
    config.program_path = os.path.dirname(__file__)
    log.logprint("Program_Path: " + str(config.program_path))
    config.Selected_file_path = os.path.abspath(file)
    log.logprint("Selected_file_Path: " + str(config.Selected_file_path))
    config.Selected_file_path_dir = os.path.dirname(file)
    log.logprint("Selected_file_Path_dir: " +
                 str(config.Selected_file_path_dir))
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
    config.filename = os.path.splitext(str(file))
    log.logprint("\nfilename: ")
    log.logprint(config.filename)
    config.output_name = os.path.realpath(
        config.filename[0] + "_Converted.json")
    # Create JSOn file and original required Headers.


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

    with open(file, "r") as f:  # Extract data as dict.
        file_matrix = f.readlines()
        print("test start")
        record = False
        matrix = []
        n = 1
        for lines in file_matrix:  # find last line, record rows after that in matrix.
            if record == True:
                #print("reading matrix data:" + str(lines))
                # print(i)
                matrix[n] = str(lines)
                n += 1
            if str(lines).rstrip() == str(last_line).rstrip() and record == False:
                print("last line found")
                record = True
            matrix += "\n"
        print("Size of matrix is:" + str(len(matrix)))
        print("test done")
