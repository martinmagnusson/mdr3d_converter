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

def Rosgrid():
    # Currently everything is added as its own "Values" key, not sure if correct.
    with open(config.output_name, 'r+') as file:
        log.logprint("\n\nPreparing to write data to JSON:")
        log.logprint("\nOpened JSON file:" + str(config.output_name))
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
            {"time": config.time_now})
        file_data["properties"].update(
            {"map_description": "converted from old maptype"})
        file_data["properties"].update(
            {"coordinate_system": "relative"})  # temp
        if config.properties["resolution"] != "":         ##Assumption! z resolution is same as x and y, Maybe better set z as 1?
            res_array = [float(config.properties["resolution"]),float(config.properties["resolution"]),float(config.properties["resolution"])]
            log.logprint("\nResolution taken from x,y as " + str(float(config.properties["resolution"])) + "and assumed same for z.")
            file_data["properties"].update(
                {"resolution": res_array})
        file_data["properties"].update(
            {"size": [int(config.properties["width"]), int(config.properties["height"]), int(1)]})
        file_data["properties"].update(
            {"localmap_id": config.filename})
        file_data["properties"].update(
            {"list_of_characteristics": {"C_name": "occupation"}})
        file_data["properties"].update(
            {"list_of_characteristics": {"C_description": "Simple occupancy: 0 means free and 1 means occupied"}})

        file_data["properties"].update( 
            {"list_of_voxels": config.properties["pixels"]})
        #negate: 0 ## Where do these extracted values go?
        #occupied_thresh: 0.65
        #free_thresh: 0.196

        file.seek(0)  # Sets file's current position at offset.
        json.dump(file_data, file, indent=4)  # convert back to json.


def Pointcloud():
    # Currently everything is added as its own "Values" key, not sure if correct.
    with open(config.output_name, 'r+') as file:
        log.logprint("\n\nPreparing to write data to JSON:")
        log.logprint("\nOpened file:" + str(config.output_name))
        # log.logprint(properties)
        file_data = json.load(file)
        # file_data = json.load(file)  # First we load existing data into a dict.
        # Join new_data with file_data inside emp_details
        file_data.update(
            {"title": "Converted Pointcloud"})
        file_data.update(
            {"description": "Implementation of pointcloud file into new 3D standard"})
        file_data["properties"].update(
            {"localmap_id": str(config.filename)})
        file_data["properties"].update(
            {"time": config.time_now})  # Temp
        file_data["properties"].update(
            {"map_description": "converted from old maptype"})
        file_data["properties"].update(
            {"coordinate_system": "relative"})  # temp
        file_data["properties"].update(
            #{"list_of_points": config.properties["list_of_points"]})
            {"list_of_points": config.matrix_out})
        # <-- get real name not path..
        file_data["properties"].update({"localmap_id": config.output_name})
        file.seek(0)  # Sets file's current position at offset.
        json.dump(file_data, file, indent=4)  # convert back to json.

def TWODstandard():
    # Currently everything is added as its own "Values" key, not sure if correct.
    with open(config.output_name, 'r+') as file:
        log.logprint("\n\nPreparing to write data to JSON:")
        log.logprint("\nOpened file:" + str(config.output_name))
        # log.logprint(properties)
        file_data = json.load(file)
        # file_data = json.load(file)  # First we load existing data into a dict.
        # Join new_data with file_data inside emp_details
        file_data.update(
            {"title": "Converted 2D Standard Gridmap"})
        file_data.update(
            {"description": "Implementation of 2D Standard Gridmap into 3D Standard"})
        file_data["properties"].update(
            {"localmap_id": str(config.filename)})
        file_data["properties"].update(
            {"time": config.time_now})  # Temp
        file_data["properties"].update(
            {"map_description": "converted from old maptype"})
        file_data["properties"].update(
            {"coordinate_system": "relative"})  # temp
        file_data["properties"].update(
            #{"list_of_points": config.properties["list_of_points"]})
            {"list_of_points": config.matrix_out})
        # <-- get real name not path..
        file_data["properties"].update({"localmap_id": config.output_name})
        file.seek(0)  # Sets file's current position at offset.
        json.dump(file_data, file, indent=4)  # convert back to json.
