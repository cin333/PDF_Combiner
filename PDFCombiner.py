import pandas as pd  # useful parsing module
import os
import fitz
import PySimpleGUI as sg

# Reference: https://stackoverflow.com/questions/63725995/how-to-display-files-in-folder-when-using-pysimplegui-filebrowse-function

def PDF_combiner(foldername, name):
    # Change both for your own computer directory
    directory = foldername

    result = fitz.open()

    for pdf in os.listdir(directory):
        with fitz.open(directory + "\\" + pdf) as mfile:
            result.insert_pdf(mfile)

    result.save(directory + "\\" + name + ".pdf")

    return 

sg.theme("NeutralBlue")

layout_1 = [
    [sg.Input(key="Folder_Directory"), sg.Button('Browse Folders', key="FolderBrowse")],

    [sg.Text('Files (Can Directly Edit and Adjust TextBox)')],
    [sg.Multiline(key='files', size=(60,20), autoscroll=True)],
    
    [sg.Text("Combine These Folders?"), sg.Button("Yes"), sg.Button("No"), sg.Button("Edit")],

    [sg.Exit()],    
]

layout_2 = [
    [sg.Text("Save in Folder: "), sg.Input(key="Folder_Directory_2"), sg.Button('Browse Folders', key="FolderBrowse_2")],
    [sg.Text("Enter Combined PDF Filename: "), sg.Input("Folder Name", do_not_clear=True)],
    [sg.Button("Save", key="-SAVE-"), sg.Button("Back", key="-BACK-")]
]

layout_3 = [

]


layout = [
    [sg.Column(layout_1, key = '-COL1-'), sg.Column(layout_2, visible = False, key = '-COL2-')], 
          ]

window = sg.Window('Test', layout)


layout = 1 # the currently visible layout
while True:
    event, values = window.read()
    filenames = "" # Empty for now
    print(event, values)
     
    if event is None or event == 'Exit' or event == 'Exit0':
        window.close()
        break

    elif event == 'FolderBrowse':
        foldername = sg.PopupGetFolder('Select Folder', no_window=True)
        print(foldername)
        if foldername: # `None` when clicked `Cancel` - so I skip it
            filenames = sorted(os.listdir(foldername))
            # it use `key='files'` to `Multiline` widget
            window['files'].update("\n".join(filenames))
        window["Folder_Directory"].update(foldername)
    
    elif event == "FolderBrowse_2":
        foldername = sg.PopupGetFolder('Select Folder', no_window=True)
        print(foldername)
        window["Folder_Directory_2"].update(foldername)
    
    elif event == 'Yes' and values['files'] != "":
        window[f'-COL{layout}-'].update(visible=False)
        layout = int(2)
        window[f'-COL{layout}-'].update(visible=True)
    
    elif event == "-SAVE-":
        PDF_combiner(foldername, values[0])
        window[f'-COL{layout}-'].update(visible=False)
        layout = int(1)
        window[f'-COL{layout}-'].update(visible=True)
        values[0] = 0
    
    elif event == "-BACK-":
        window[f'-COL{layout}-'].update(visible=False)
        layout = int(1)
        window[f'-COL{layout}-'].update(visible=True)
    


        
            

