import PySimpleGUI as sg
import os.path
import convert as co
import validation as va
import config
import custom_logging as log

# Packages needed.
# pip3 install Pillow
# pip3 install pysimplegui
# pip3 install beautifulsoup4
# pip3 install lxml
# https://csveda.com/python-combo-and-listbox-with-pysimplegui/
from PySimpleGUI.PySimpleGUI import Checkbox, Tab
sg.theme('graygraygray')  # color

# Program
print("\n" + "Starting Program" + "\n")

# sg.theme_previewer()
file_list_column = [
    [
        sg.Text("Folder \t"),
        sg.In(size=(25, 1), enable_events=True, key="-FOLDER-"),
        sg.FolderBrowse(),
    ],
    [
        sg.Listbox(
            values=[], enable_events=True, size=(43, 20), key="-FILE LIST-"
        )
    ],
    [sg.HSeparator()],
    # [
    #    sg.Text("File \t"),
    #    sg.In(size=(25, 1), enable_events=True, key="-FILE-"),
    #    sg.FileBrowse(),
    # ],
    [
        sg.Checkbox("Run on All Files in folder", key="-Checkbox_Batch-",
                    tooltip="Run operation on all files in the folder", enable_events=True)
    ],
    [sg.HSeparator()],
    [
        sg.Button("Exit", font=config.Font,
                  button_color="lightcoral", size=(20, 1))
    ],

]


image_viewer_column = [
    [sg.Text("File Information", font=config.Font)],
    [sg.HSeparator()],
    [sg.Text(size=(70, 1), key="-TOUT-")],
    [sg.Canvas(key="-Info-", size=(350, 350))],
    [sg.HSeparator()],
    [
        sg.Combo(list(config.Filetypes), size=(20, 4), enable_events=True, key='-FILETYPE-',
                 default_value=config.Filetypes[0], tooltip="Select what format to convert from."),
        sg.Button("Convert", font=config.Font,
                  button_color="grey", size=(20, 1), disabled=True),
        sg.Checkbox("Create Logfile", key="-Checkbox_Logging-",
                    tooltip="Enable to create a logfile along with the conversion")
    ]
]

# Full layout
layout = [
    [
        sg.Column(file_list_column, element_justification='left'),
        sg.VSeperator(),
        sg.Column(image_viewer_column, element_justification='left'),
    ]
]

window = sg.Window("3D MDR Converter", layout, element_justification='c')

# Run the Event Loop
while True:
    event, values = window.read()
    if event == "Exit" or event == sg.WIN_CLOSED:
        break
    if event == "-FILETYPE-":  # Extract the Filetype selected.
        config.Filetype = values['-FILETYPE-']
        # print(config.Filetype)
    if event == "-FOLDER-":     # Folder name was filled in, make a list of files in the folder
        folder = values["-FOLDER-"]
        try:
            # Get list of files in folder
            file_list = os.listdir(folder)
        except:
            file_list = []
        fnames = [
            f
            for f in file_list
            if os.path.isfile(os.path.join(folder, f))
            and f.lower().endswith((".pcd", ".pgm", ".yaml", ".json", ".xml"))
        ]
        window["-FILE LIST-"].update(fnames)
    # Enable Conversion button without selecting a file.
    if event == "-Checkbox_Batch-": ## Batch Checkbox
        if config.batch_enabled == False:
            config.batch_enabled = True
            window["Convert"].update(
                disabled=False, button_color="forestgreen")
        else:
            config.batch_enabled = False
            window["Convert"].update(disabled=True, button_color="grey")
        print("Batch mode:" + str(config.batch_enabled))
    if event == "-Checkbox_Logging-": ##Loggin Checkbox
        if config.logging_enabled == False:
            config.logging_enabled = True
        else:
            config.logging_enabled = False
        print("Batch mode:" + str(config.batch_enabled))
    if event == "Convert":
        if values["-Checkbox_Logging-"] == True:
            config.logging_enabled = True
            print("\nLogfile will be created")
        else:
            config.logging_enabled = False
        if config.batch_enabled == True: ##If batch enabled, run batch scripts.
            config.Selected_file_path_dir = values["-FOLDER-"]
            # Only run on ROS Gridmap files, skip others.
            if values['-FILETYPE-'] == "ROS Gridmap":              
                co.batch_ROS()
            elif values['-FILETYPE-'] == "Pointcloud":
                co.batch_PCD()
            elif values['-FILETYPE-'] == "2D Standard":
                co.batch_TwoDG()
            log.batch_log_finalize()    
            print("Batch operation done")
        else: ## Else convert the single picked file.
            co.convert(config.Selected_file_path, config.Filetype)
    elif event == "-FILE LIST-":  # A file was chosen from the listbox
        try:
            config.filename = values["-FILE LIST-"][0]
            config.Selected_file_path_dir = values["-FOLDER-"]
            config.Selected_file_path = os.path.join(
                config.Selected_file_path_dir, config.filename
            )
            print("\nValues Folder:" +
                  str(values["-FOLDER-"]) + "\nFile:" + str(values["-FILE LIST-"][0]))
            window["-TOUT-"].update(config.Selected_file_path)
            window["Convert"].update(
                disabled=False, button_color="forestgreen")
            #config.batch_enabled = False
            #window["-Checkbox_Batch-"].update(values)
        except:
            pass

window.close()
print("\n" + "Ending Program" + "\n")
