import os
import PySimpleGUI as sg
import requests

def rename(path, isEro, outFolder):
    image_folder = path + ('/ero' if isEro else '/nonero')
    outputFolder = path + '/' + outFolder
    if not os.path.exists(outputFolder):
        os.makedirs(outputFolder)
    for filename in os.listdir(image_folder):
        if '-' in filename:
            parts = filename.split('-', 1)
            author = parts[0].strip()
            title_extension = parts[1].strip()

            if '.' in title_extension:
                title, image_extension = title_extension.rsplit('.', 1)
            else:
                title = title_extension
                image_extension = ""

            new_filename = f'{title}.{image_extension}'
            new_image_path = os.path.join(outputFolder, new_filename)

            os.rename(os.path.join(image_folder, filename), new_image_path)
            author_md_path = os.path.join(image_folder, f'{author}.md')

            if os.path.exists(author_md_path):
                with open(author_md_path, 'r') as md_file:
                    md_content = md_file.read()
                    md_content += f"\n![[{new_filename}]]"
            else:
                md_content = f"[[Art]]\n[[Erotic]]\n![[{new_filename}]]" if isEro else f"[[Art]]\n![[{new_filename}]]"

            with open(author_md_path, 'a') as md_file:
                md_file.write(md_content + '\n\n')
        else:
            print(f'Skipped {filename}, no "-" found')
            sg.popup_auto_close(f'Skipped {filename}, no "-" found')

def main():
    # All the stuff inside your window.
    layout = [[sg.Text('Input folder:'), sg.InputText(key='-INPUT_PATH-', default_text='img', size=(30, 20)), sg.FolderBrowse(key='-INPUT_PATH-')],
              [sg.Text('Output folder:'), sg.InputText(key='-OUTPUT_PATH-', default_text='fin', size=(30, 20))],
              [sg.Button('Generate Source'), sg.Button('Build Script'),
               sg.Checkbox(text='ero', key='-EROBOX-', default=True),
               sg.Checkbox(text='nonero', key='-NONEROBOX-', default=True), sg.Button('Ok')]]

    # Create the Window
    window = sg.Window('img splitter', layout,
                       element_justification='c', finalize=True)

    # Event Loop to process "events" and get the "values" of the inputs
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:  # if user closes window
            break
        elif event == 'Ok':
            if values['-NONEROBOX-']:
                rename(values['-INPUT_PATH-'], False, values['-OUTPUT_PATH-'])
            if values['-EROBOX-']:
                rename(values['-INPUT_PATH-'], True, values['-OUTPUT_PATH-'])
            break
        elif event == 'Generate Source':
            response = requests.get("https://raw.githubusercontent.com/Scavix/image-splitter-4-obsidian/main/image_code.py")
            if response.status_code == 200:
                f = open("image_code.py", "w")
                f.write(response.text)
                f.close()
                sg.popup("Done")
            else:
                sg.popup("Web site does not exist or is not reachable")
        elif event == 'Build Script':
            response = requests.get("https://raw.githubusercontent.com/Scavix/image-splitter-4-obsidian/main/image_build_script.bat")
            if response.status_code == 200:
                f = open("image_build_script.bat", "w")
                f.write(response.text)
                f.close()
                sg.popup("Done")
            else:
                sg.popup("Web site does not exist or is not reachable")
        else:
            break
    window.close()

if __name__ == "__main__":
    main()
