import PySimpleGUI as sg
import os.path
import convert as co
import validation as va
import config
import custom_logging as log

## Packages needed.
    # pip3 install Pillow
    # pip3 install pysimplegui
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
    [
        sg.Text("File \t"),
        sg.In(size=(25, 1), enable_events=True, key="-FILE-"),
        sg.FileBrowse(),
    ],
    [sg.HSeparator()],
    [
        sg.Button("Exit", font=config.Font, button_color="lightcoral", size=(20, 1))
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
        sg.Checkbox("Create Logfile", key="-Checkbox_Logging-", tooltip="Enable to create a logfile along with the conversion")
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
        #print(config.Filetype)
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
    if event == "Convert":
        print("Start Converting")  # Create popup?
        if values["-Checkbox_Logging-"] == True:
            config.logging_enabled = True
            print("\nLogfile will be created")
        config.Filetype = co.identify(config.Filetype) #Doesnt do much atm. Attempts to verify file.
        if config.Filetype == "2D Standard": # Only check validity on XML files
            if va.validate(config.Selected_file_path, config.Filetype): ##Currently just says if file is valid or not, convert still runs afterwards.
                log.logprint('Valid! :)')
            else:
                log.logprint('Not valid! :(')
        co.convert(config.Selected_file_path, config.Filetype)
    elif event == "-FILE LIST-":  # A file was chosen from the listbox
        try:
            config.Selected_file_path = os.path.join(
                values["-FOLDER-"], values["-FILE LIST-"][0]
            )
            config.filename = values["-FILE LIST-"][0]
            window["-TOUT-"].update(config.Selected_file_path)
            window["Convert"].update(disabled=False, button_color="forestgreen")
        except:
            pass

window.close()
print("\n" + "Ending Program" + "\n")
