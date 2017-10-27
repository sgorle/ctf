'''
Created on Aug 4, 2017

@author: sgorle
@summary: Software environment setup.
'''
import os

def install_python():
    """
    Installs the Python if not installed.
    
    @return: None
    """
    if _python_installed() is False:
        print "Installing Python: TBD"
        if _python_installed() is False:
            print "Python is not installed. Please install manually."
            exit()
        
       
def _python_installed():
    """
    Check whether Python installed
    
    @return: [bool] true if installed otherwise false.
    """
    flag = False
    print "Check if python is installed or not ..."
    ret_value = os.system("python --version")
    if ret_value is 0:
        print "Python is already installed"
        flag = True
    else:
        print "Python is not installed or not added the python to the path variable"
        flag = False
    return flag
    

def install_studio_link():
    """
    Installs the studio link
    
    @return: None
    """
    if _check_scs_installed() is False:
        print "Installing SCS 1.2 : TBD"
        print "Install SCS 1.2 manually."
        exit()
    if _check_studiolink_installed() is False:
        print "installing studio link..."
        os.system("python -m pip install -U pip setuptools")    
        os.system(r"%ALLUSERSPROFILE%\CirrusLogic\SCS_{0}\installers".format("1.2"))
        os.system("python -m pip install -U linkclient-1.2.0-py2-none-any.whl")
        if _check_python_package_installed("grpcio") is False:
            os.system("python -m pip install -U grpcio")
    exit()
    
    
def _check_studiolink_installed():
    """
    Check whether Studio link is installed
    
    @return: [bool] true if installed otherwise false.
    """
    flag = False
    print "Checking Studiolink installed or not..."
    try:
        from studiolink.StudioLink import StudioLink  # @UnusedImport
        print "Studio link installed already"
        flag =  True
    except Exception:
        print "Studio link is not installed"
        flag = False
    return flag
    
def _check_python_package_installed(pkg_name):
    """
    Check whether the given package installed.
    
    @param pkg_name: 
            [string] scs package name to isntall.
    @return: [bool] true if installed otherwise false.
    """
    import pip
    
    flag = False
    installed_packages = pip.get_installed_distributions()
    flat_installed_packages = [package.project_name for package in installed_packages]
    if pkg_name in flat_installed_packages:
        flag =  True
    return flag
    
def _check_scs_installed():
    """
    Check whether SCS is installed.
    
    @return: [bool] true if installed otherwise false.
    """
    flag = False
    print "Checking SCS installed or not..."
    if os.path.exists(r"C:\Program Files\Cirrus Logic\SoundClearStudio_1.2\link\bin\scs_link.exe") is True:
        print "SCS 1.2 is installed already"
        flag =  True
    else:
        print "SCS 1.2 is not installed."
        flag = False
    return flag
        