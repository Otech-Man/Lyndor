import os
import sys
import shutil
import json

real_path = os.path.realpath(__file__)
real_path = real_path[:real_path.find('install.py')]
LYNDOR_PATH = real_path

def check_os():
    '''Check operating system'''
    if sys.platform.lower() == 'darwin':
        return 'macos'
    elif sys.platform.lower() == 'win32':
        return 'windows'
    elif sys.platform.lower() == 'linux2':
        return 'linux'
    else:
        sys.exit('unknown operating system.')

def set_path():
    '''Set path for saving lynda folder'''
    if check_os() == 'macos':
        os.chdir(os.path.expanduser('~/Movies'))
        return os.getcwd()
    elif check_os() == 'windows':
        os.chdir(os.path.expanduser('~/Videos'))
        return os.getcwd()

def folder_path(folder):
    '''Set path for desktop folder'''
    if check_os() == 'macos':
        os.chdir(os.path.expanduser('~/'+folder))
        return os.getcwd()
    elif check_os() == 'windows':
        os.chdir(os.path.expanduser('~/'+folder))
        return os.getcwd()

def create_folder():
    ''' Create lynda folder '''
    path = read_settings_json('preferences', 'location')
    if not os.path.exists(path):
        os.makedirs(path)
        print '-> Lynda folder created at: ' + read_settings_json('preferences', 'location')
    else:
        print '>>> Lynda folder already exists\n'

def create_aliases():
    '''Create aliases file'''
    os.chdir(LYNDOR_PATH)
    if check_os() == 'windows':
        run_path = 'doskey lynda= python "'+os.getcwd()+'/run.py"'
        alias = open('aliases.bat', 'w')
        alias.write(run_path)
        alias.close()
        print '-> aliases.bat file created.\n'

def lynda_folder_files():
    ''' create Run-Lyndor.bat in windows '''
    os.chdir(LYNDOR_PATH)
    bulk_download = open('Bulk Download.txt','w')
    bulk_download.close()
    shutil.move('Bulk Download.txt', read_settings_json('preferences', 'location')+'/Bulk Download.txt')
    print '-> Bulk Download.txt file created successfully.\n'
    if check_os() == 'windows':
        run_path = 'python "'+os.getcwd()+'/run.py"'
        lynda = open('Run-Lyndor.bat', 'a')
        lynda.writelines('@ECHO OFF\n')
        lynda.writelines('REM Batch file to execute run.py\n')
        lynda.writelines('SET PATH=%PATH%;C:\Python27;C:\Python27\Scripts\n')
        lynda.writelines(run_path+'\n')
        lynda.writelines('pause')
        lynda.close()
        try:
            os.rename('Run-Lyndor.bat', read_settings_json('preferences', 'location') + '/Run-Lyndor.bat')
        finally:
            print '-> Run-Lyndor.bat file created.\n'

def create_settings_json():
    ''' Create settings_json file '''
    os.chdir(LYNDOR_PATH)
    files = os.listdir(os.getcwd())
    for f in files:
        if f == 'settings.json':
            #Prevent existing settings.json file from overwriting
            print '>>> settings.json file already exists, will use the same path inside it.\n'
            return
    settings_dict = {
        "credentials":{
            "username" : "",
            "password" : "",
            },
        "preferences":{
            "location" : set_path()+'/Lynda',
            "download_subtitles" : True
        }
    }
    out_file = open(LYNDOR_PATH+'/settings.json', 'w')
    json.dump(settings_dict, out_file, indent=4)
    out_file.close()
    print '-> settings.json file created.\
 (To download videos to a different folder, replace the folder path in settings.json)'
    print '\n>>> Your Lynda videos will be saved at -> '+ read_settings_json('preferences','location') +'\n'

def read_settings_json(section, key):
    ''' Read settings.json '''
    os.chdir(LYNDOR_PATH)

    in_file = open('settings.json', 'r')
    data = json.load(in_file)
    in_file.close()
    return data[section][key]

def install_dependencies():
    '''install required softwares'''
    os.chdir(LYNDOR_PATH)
    requirements = open('requirements.txt')
    line = requirements.readline()
    for module in requirements:
        os.system('pip install '+ module)
    requirements.close()
    print '\n>>> All the required softwares are installed\n'

if __name__ == '__main__':
    try:
        install_dependencies()
        set_path()
        create_settings_json()
        create_folder()
        create_aliases()
        lynda_folder_files()
    except KeyboardInterrupt:
        print "Program execution cancelled through keyboard!"
        sys.exit(0)
            