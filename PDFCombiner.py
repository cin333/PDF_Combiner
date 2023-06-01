import pandas as pd  # useful parsing module
import os
import fitz
import PySimpleGUI as sg

# Reference 1: https://stackoverflow.com/questions/63725995/how-to-display-files-in-folder-when-using-pysimplegui-filebrowse-function
# Reference 2: https://stackoverflow.com/questions/68929799/pysimplegui-right-justify-a-button-in-a-frame

def PDF_combiner(foldername_1, filename, foldername_2):
    # Change both for your own computer directory
    directory = foldername_1
    result = fitz.open()

    for pdf in directory:
        with fitz.open(pdf) as mfile:
            result.insert_pdf(mfile)

    result.save(foldername_2 + "\\" + filename + ".pdf")

    return 

sg.theme("NeutralBlue")
font = ("Times New Roman", 9)

layout_1 = [
    [sg.Input(key="Folder_Directory", font=font, size=(40,10)), sg.Button('Browse Folders', key="FolderBrowse", font=font), sg.Button("Refresh", key="-REFRESH-", font=font)],

    [sg.Frame(
        layout = [
            [sg.Multiline(key='files', size=(60,20), autoscroll=True, font=font)]
                ], 
        title="Files (Can Directly Edit and Order PDFs of TextBox)",
        font = font
    )
    ],
   
    [sg.Text("Combine These Folders?", font=font), sg.Button("Yes", font=font), sg.Push(),sg.Exit(font=font)],    
]

layout_2 = [
    [sg.Text("Save in Folder: ", font=font), sg.Input(key="Folder_Directory_2", font=font), sg.Button('Browse Folders',font=font, key="FolderBrowse_2")],
    [sg.Text("Enter Combined PDF Filename: ", font=font), sg.Input("Folder Name", do_not_clear=True, font=font), sg.Button("Save", key="-SAVE-", font=font)],
    [sg.Button("Back", key="-BACK-", font=font), sg.Push()]
]

layout_3 = [

]


layout = [
    [sg.Column(layout_1, key = '-COL1-'), sg.Column(layout_2, visible = False, key = '-COL2-')], 
          ]

window = sg.Window('PDF Combiner', layout)


layout = 1 # the currently visible layout
while True:
    event, values = window.read()
    print(event, values)
     
    if event is None or event == 'Exit' or event == 'Exit0':
        window.close()
        break

    elif event == 'FolderBrowse':
        foldername_1 = sg.PopupGetFolder('Select Folder', no_window=True)
        print(foldername_1)
        if foldername_1: # `None` when clicked `Cancel` - so I skip it
            filenames = sorted(os.listdir(foldername_1))
            # it use `key='files'` to `Multiline` widget
            window['files'].update("\n".join(filenames))
        window["Folder_Directory"].update(foldername_1)
    
    elif event == "FolderBrowse_2":
        foldername_2 = sg.PopupGetFolder('Select Folder', no_window=True)
        print(foldername_2)
        window["Folder_Directory_2"].update(foldername_2)
    
    elif event == 'Yes' and values['files'] != "":
        window[f'-COL{layout}-'].update(visible=False)
        layout = int(2)
        window[f'-COL{layout}-'].update(visible=True)
    
    elif event == "-SAVE-":
        final_list = []
        pdf_list = values['files'].split("\n")
        for i in pdf_list:
            i = values['Folder_Directory'] + "/" + i
            final_list.append(i)
        PDF_combiner(final_list, values[0], foldername_2)
        window[f'-COL{layout}-'].update(visible=False)
        layout = int(1)
        window[f'-COL{layout}-'].update(visible=True)
        values[0] = 0

        window["files"].update("")
        window["Folder_Directory"].update("")
    
    elif event == "-BACK-":
        window[f'-COL{layout}-'].update(visible=False)
        layout = int(1)
        window[f'-COL{layout}-'].update(visible=True)
    
    elif event == "-REFRESH-":
        window["files"].update("")
        window["Folder_Directory"].update("")
    
