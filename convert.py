from ctypes import Array, sizeof
import json
import os.path
import shutil
from tkinter import DoubleVar
import config
import custom_logging as log
from PIL import Image as ImageProc
import time
import re
import add_to_JSON


# Currently this function just accepts the manually input filetype and prints and returns it to confirm.
def identify(string):
    log.logprint("\nIdentifying file as: " + str(string))
    filetype = string
    return filetype


def convert(file, filetype):
    log.logprint(os.path.abspath("\nConverting: " + str(file)))
    if filetype == "ROS Gridmap":
        start = time.time()  # start time
        extract_ROS(file)
        create_json(config.output_name)
        add_to_JSON.Rosgrid(config.properties, config.output_name)
        end = time.time()
        print("Conversion Done!")
        log.logprint("Elapsed time is  {}s".format(end-start))
    elif filetype == "2D Standard":
        convert_2DStandard(file)
    elif filetype == "Pointcloud":
        convert_pointcloud(file)


def extract_ROS(file):
    
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
    config.output_name = os.path.realpath(config.filename[0] + "_Converted.json")
    # Create JSOn file and original required Headers.



def reset_config():  # will be needed to run after each convert probably.
    return 0


def convert_2DStandard(file):
    log.logprint("\nConverting from 2D Standard")
    json.dumps("2D standard test output")


def convert_pointcloud(file):
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





# Sets up the very most basic JSON 3D MDR document which can be edited with real data.
def create_json(output_name):
    template_path = os.path.realpath(
        str(config.program_path) + "/JSON_Templates/Convert_Template.json")
    ## Check if output file already exists, if so, remove
    if os.path.exists(output_name):
            os.remove(output_name)
    shutil.copyfile(template_path, output_name)
    log.logprint("\nJSON file created \nHeader taken from: " +
                 str(template_path))
