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


# https://www.geeksforgeeks.org/append-to-json-file-using-python/
def Rosgrid(properties, filename):
    # Currently everything is added as its own "Values" key, not sure if correct.
    with open(filename, 'r+') as file:
        log.logprint("Opened file:" + str(filename))
        # log.logprint(properties)
        file_data = json.load(file)
        # file_data = json.load(file)  # First we load existing data into a dict.
        # Join new_data with file_data inside emp_details
        file_data.update(
            {"title": "Converted ROS Gridmap"})
        file_data.update(
            {"description": "Implementation of the local map type densegrid. A densegrid is a parallelepiped divided in equal voxels, which are described by the proper field."})
        file_data["properties"].update(
            {"localmap_id": str(config.filename)})
        file_data["properties"].update(
            {"time": "now"})  # Temp
        file_data["properties"].update(
            {"map_description": "converted from old maptype"})
        file_data["properties"].update(
            {"coordinate_system": "relative"})  # temp
        file_data["properties"].update(
            {"resolution": str(float(properties["resolution"]))})
        file_data["properties"].update(
            {"size": [int(properties["width"]), int(properties["height"]), int(1)]})
        file_data["properties"].update(
            {"list_of_voxels": properties["pixels"]})
        # <-- get real name not path..
        file_data["properties"].update({"localmap_id": filename})
        file.seek(0)  # Sets file's current position at offset.
        json.dump(file_data, file, indent=4)  # convert back to json.