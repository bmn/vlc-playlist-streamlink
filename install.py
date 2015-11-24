#!/usr/bin/python

from __future__ import print_function
import os
import sys
import time
import imp
import subprocess
import ctypes
import shutil
import getpass

def error_out(err):
    print('Error: %s' % err)
    exit(1)

class Installer:
    def __init__(self, platform):
        self.steps = Step()
        if callable([self, platform]):
            error_out('"%s" is not a valid platform.' % platform)
        getattr(self, platform)()
    
    def nt(self): # Windows
        self.admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
        self.steps.python_packages()
        self.steps.service_nt()
        dirs = ['C:\Program Files\VideoLAN\VLC', 'C:\Program Files (x86)\VideoLAN\VLC']
        if self.admin:
            self.steps.vlc_plugin(dirs)
        else:
            vlcdir = self.steps.vlc_plugin(dirs, True)
            self.steps.install_vlc_plugin_nt(vlcdir)
    
    def cygwin(self):
        self.admin = 544 in os.getgroups() or 0 in os.getgroups()
        self.steps.python_packages()
        self.steps.service_cygwin(self.admin)
        # Using Windows-style paths because some Cygwin systems (e.g. MobaXterm) don't use /cygdrive
        dirs = ['C:\Program Files\VideoLAN\VLC', 'C:\Program Files (x86)\VideoLAN\VLC']
        if self.admin:
            self.steps.vlc_plugin(dirs)
        else:
            vlcdir = self.steps.vlc_plugin(dirs, True)
            self.steps.install_vlc_plugin_cygwin(vlcdir)
    
    def mac(self):
        self.admin = os.getuid() == 0
        self.steps.python_packages()
        self.steps.service_mac()
        self.steps.vlc_plugin(['/Applications/VLC.app/Contents/MacOS/share'])
    
    def linux(self):
        self.admin = os.getuid() == 0
        self.steps.python_packages()
        self.steps.service_linux()
        self.steps.vlc_plugin(['~/.local/share/vlc'])
    
class Step:
    def python_packages(self, exit_on_error = False):
        package_required = False
        print('Checking for Python packages...')
        for package in ['livestreamer', 'six']:
            try:
                imp.find_module(package)
                print('  %s [FOUND]' % package)
            except ImportError:
                print ('  %s [MISSING]' % package)
                package_required = True
                if exit_on_error or (self.install_python_package(package) != 0):
                    error_out('Some packages could not be installed. Please make sure that pip or easy_install is installed.')
                
        if package_required:
            self.python_packages(True)
            
    def install_python_package(self, package):
        if getattr(self, 'pip', None) is None:
            try:
                import pip
                self.pip = True
            except ImportError:
                self.pip = False
        if self.pip:
            return pip.main(['install', package])
        else:
            return os.system('easy_install %s' % package)
            
    def service_nt(self):
        print('''[!] We can't install livestreamersrv as a service on native Windows yet, sorry :(''')
        print('''[!] Please run the following command manually''')
        print('''[!]   (replacing "PASSWORD" with your Windows password)''')
        print('''[!]     to install it as a scheduled task:''')
        print('''schtasks /Create /RU %s /RP PASSWORD /SC ONSTART /TN "Livestreamer Service" /TR "%s\livestreamersrv\livestreamersrv.bat"''' % (getpass.getuser(), sys.path[0]))
        print('')
        
    def service_cygwin(self, admin = False):
        if subprocess.call(['cygrunsrv', '-Q', 'Livestreamer Service'], stdout = open(os.devnull), stderr = open(os.devnull)) == 0:
            print('Windows livestreamersrv service already exists, skipping installation.')
            return True
        if admin:
            # We can run commands directly :)
            if subprocess.call(['cygrunsrv', '-I', 'Livestreamer Service', '-p', '%s/livestreamersrv/livestreamersrv' % sys.path[0]], stdout = open(os.devnull), stderr = open(os.devnull)) == 1:
                print('Installing livestreamersrv as a Windows service: [FAIL]')
                print('Service install appears to have failed. To start the service manually, use the command:')
                print('./livestreamersrv/livestreamersrv start')
            else:
                print('Installing livestreamersrv as a Windows service: [OK]')
                time.sleep(1)
                if subprocess.call(['cygrunsrv', '-S', 'Livestreamer Service'], stdout = open(os.devnull), stderr = open(os.devnull)) == 1:
                    print('Starting livestreamersrv: [FAIL]')
                    print('Please start "Livestreamer Service" manually from the Services menu.')
                else:
                    print('Starting livestreamersrv: [OK]')
        else:
            # Have to go through cygstart and ask for privs :(
            print('Installing livestreamersrv as a Windows service (requires Administrator privileges)')
            raw_input('Press Enter to continue...')
            os.system('cygstart --action=runas cmd.exe /k "$(cygpath -wa $(which cygrunsrv)) -I \'Livestreamer Service\' -p %s/livestreamersrv/livestreamersrv & exit"' % sys.path[0])
            time.sleep(1) # Give poor old Windows a chance to catch up...
            if subprocess.call(['cygrunsrv', '-Q', 'Livestreamer Service'], stdout = open(os.devnull), stderr = open(os.devnull)) == 1:
                print('Service install appears to have failed. To start the service manually, use the command:')
                print('./livestreamersrv/livestreamersrv start')
            else:
                print('Checking livestreamersrv service: [OK]')
                print("Starting livestreamersrv (requires Administrator privileges)")
                raw_input('Press ENTER to continue...')
                os.system('cygstart --action=runas cmd.exe /k "$(cygpath -wa $(which cygrunsrv)) -S \'Livestreamer Service\' & exit"')
            
    def service_mac(self):
        return False
        
    def service_linux(self):
        return False
        
    def vlc_plugin(self, dirs, rtn = False):
        for dir in dirs:
            if os.path.isdir(dir):
                print('Looking for VLC Lua directory: %s' % dir)
                if rtn:
                    return dir
                else:
                    return self.install_vlc_plugin(dir)
        error_out('VLC directory not found. Please copy vlc/livestreamer.lua to the directory lua/playlist in your VLC installation.')
        
    def install_vlc_plugin(self, destination):
        path = destination+'/lua/playlist/livestreamer.lua'
        print('Installing VLC plugin')
        shutil.copy(sys.path[0]+'/vlc/livestreamer.lua', path)
        return self.check_vlc_plugin(path)
        
    def install_vlc_plugin_nt(self, destination):
        path = destination + r'\lua\playlist\livestreamer.lua'
        print('''[!] We can't install the VLC plugin automatically without admin privileges, sorry :(''')
        print('''[!] Please run the installer as Administrator...''')
        print('''[!] ...or manually copy vlc\livestreamer.lua to %s''' % path)
        
    def install_vlc_plugin_cygwin(self, destination):
        path = destination + r'\lua\playlist\livestreamer.lua'
        print('Installing VLC plugin (requires Administrator privileges)')
        raw_input('Press ENTER to continue...')
        os.system('cygstart --action=runas cmd.exe /k "copy \\"$(cygpath -wa $(pwd)/vlc/livestreamer.lua)\\" \\"%s\\" & exit"' % path)
        return self.check_vlc_plugin(path)
    
    def check_vlc_plugin(self, path):
        if os.path.exists(path):
            print('Checking VLC plugin: [OK]')
            return True
        else:
            error_out('Plugin install appears to have failed. Please copy vlc/livestreamer.lua to the directory lua/playlist in your VLC installation.')


Installer(sys.argv[1])
print('Installation complete!')
exit(0)