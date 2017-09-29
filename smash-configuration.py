from sys import platform
import os


print("--------------------------------------------------------\n")
print("------------ Smashbox\n")
print("------------ This is a framework for end-to-end testing the core storage functionality of owncloud-based services.\n")
print("--------------------------------------------------------\n")

client_choice = raw_input('\033[1m' + "Please, choose the client to be tested: \n 0:OwnCloud Native Client \n 1:CERNbox Client \n \n "  + '\033[0m')

oc_account_name = raw_input('\033[1m' + "Test account name:\n" + '\033[0m')
oc_account_password = raw_input('\033[1m' + "Test account password:\n" + '\033[0m')
oc_server = raw_input('\033[1m' + "OwnCloud test server:\n" + '\033[0m')
ssl_enable = raw_input('\033[1m' + "Do you want to enable ssl (Y/N)?:\n" + '\033[0m')

#
# ##--------------## python configuration ##-------------------##
#

try:
    import pip
except ImportError:
    print("Pip not present. Installing pip...")
    os.system("wget https://bootstrap.pypa.io/get-pip.py")
    os.system("python get-pip.py")
    os.system("pip install wget")

import wget

#
# ##--------------## owncloud client installation and configuration ##-------------------##
#

if not os.path.exists("./tmp"):
     os.makedirs("./tmp")

def change_cfg(path):
    cfg_file = open(home + path + "/new-cernbox.cfg", "w")
    for line in open(home + path + "/old-cernbox.cfg"):
        if line[0:len("0\http_user")] == "0\http_user":
            cfg_file.write("0\http_user=" + oc_account_name)
        elif line[0:len("0\url")] == "0\url":
            cfg_file.write("0\url=https://" + oc_server)
        elif line[0:len("0\user")] == "0\user":
            cfg_file.write("0\user=" + oc_account_name)
        else:
            cfg_file.write(line)

if client_choice == "1": # cernbox
     if platform == "linux" or platform == "linux2": # linux
         print '\033[94m' + "(1) Installing cernbox client for linux" + '\033[0m'
         wget.download("http://cernbox.cern.ch/cernbox/doc/Linux/centos7-cernbox.repo")
         os.rename("./centos7-cernbox.repo", "./tmp/centos7-cernbox.repo")
         os.system("cp ./tmp/centos7-cernbox.repo /etc/yum.repos.d/cernbox.repo")
         os.system("yum update")
         os.system("yum install cernbox-client")

         home = os.environ['HOME']
         os.rename(home + "/.local/share/data/CERNbox/cernbox.cfg", home + "/.local/share/data/CERNbox/old-cernbox.cfg")
         change_cfg("/.local/share/data/CERNbox")


     elif platform == "darwin": # MAC OS X
        print '\033[94m' + "(1) Installing cernbox client for MAC OSX" + '\033[0m'
        wget.download("https://cernbox.cern.ch/cernbox/doc/MacOSX/cernbox-2.2.4.1495-signed.pkg")
        os.system("cp ./cernbox-2.2.4.1495-signed.pkg ./tmp/cernbox-2.2.4.1495-signed.pkg")
        os.system("installer -pkg ./tmp/cernbox-2.2.4.1495-signed.pkg -target /")


        home = os.environ['HOME']
        if os.path.exists("/Library/Application Support/CERNbox/cernbox.cfg"):
            os.rename(home + "/Library/Application Support/CERNbox/cernbox.cfg", home + "/Library/Application Support/CERNbox/old-cernbox.cfg")
            change_cfg("/Library/Application Support/CERNbox")


     elif platform == "Windows" : # Windows
        print '\033[94m' + "(1) Installing cernbox client for Windows" + '\033[0m'
        wget.download("https://cernbox.cern.ch/cernbox/doc/Windows/cernbox-2.2.4.830-setup.exe")
        os.rename("./cernbox-2.2.4.830-setup.exe", "./tmp/cernbox-2.2.4.830-setup.exe")
        os.system("./tmp/cernbox-2.2.4.830-setup.exe")

        home = os.environ['LOCALAPPDATA']

elif client_choice == "0": # Owncloud Native Client
        print '\033[94m' + "(1) Installing OwnCloud client" + '\033[0m'

        home = os.environ['HOME']
        os.rename(home + "/.local/share/data/ownCloud/owncloud.cfg", home + "/.local/share/data/ownCloud/old-owncloud.cfg")

        cfg_file = open(home + "/.local/share/data/ownCloud/new-owncloud.cfg", "w")

        for line in open(home + "/.local/share/data/ownCloud/old-owncloud.cfg"):
            if line[0:len("0\http_user")] == "0\http_user":
                cfg_file.write("0\http_user=" + oc_account_name)
            elif line[0:len("0\url")] == "0\url":
                cfg_file.write("0\url=https://" + oc_server)
            elif line[0:len("0\user")] == "0\user":
                cfg_file.write("0\user=" + oc_account_name)
            else:
                cfg_file.write(line)
#
##--------------## smashbox installation ##-------------------##
#

print "\n" + '\033[94m' + "(2) Installing Smashbox" + '\033[0m'

if not os.path.exists("./smashbox"):
    os.system("git clone https://github.com/yolanda93/smashbox.git")

os.system("cp ./auto-smashbox.conf ./smashbox/etc/auto-smashbox.conf")

f = open('./smashbox/etc/auto-smashbox.conf', 'a')

f.write('oc_account_name =' + oc_account_name + '\n')
f.write('oc_account_password =' + oc_account_password + '\n')
f.write('oc_server =' + oc_server + '\n')


if ((ssl_enable =="Y") | (ssl_enable =="y")):
    f.write('oc_ssl_enabled =' + "True" + '\n')
else:
    f.write('oc_ssl_enabled =' + "False" + '\n')

if platform == "linux" or platform == "linux2":  # linux
    if client_choice == "1": # cernbox
        location = os.popen("whereis cernboxcmd").read()
        path = "/" + location.split("cernboxcmd")[1].split(": /")[1] + "cernboxcmd"
elif platform == "darwin":
        path = "/Applications/cernbox.app/Contents/MacOS/cernboxcmd"
elif platform == "Windows":
    if client_choice == "1": # cernbox
        location = os.popen("where cernboxcmd").read()
        path = "/" + location.split("cernboxcmd")[1].split(": /")[1] + "cernboxcmd" # to be changed

f.write("oc_sync_cmd =" + path)

f.close()

os.system("pip install -r ./smashbox/requirements.txt")

#
##--------------## Running Smashbox ##-------------------##
#
print '\033[94m' + "(3) Running smashbox" + '\033[0m'

monit_choice= raw_input('\033[1m' + "Do you want to set up this machine for regression testing with monitoring (Y/N)?:\n" + '\033[0m')

if ((monit_choice == "Y") or (monit_choice == "y")):

    try:
        from crontab import CronTab
    except ImportError:
        print("CronTab not present. Installing crontab...")
        os.system("pip install python-crontab")
        from crontab import CronTab

    user = os.popen("echo $USER").read().split("\n")[0]
    my_cron = CronTab(user)
    current_path = os.path.dirname(os.path.abspath(__file__))
    job = my_cron.new(command="python " + current_path + "/smash-run.py")
    job.day.every(1)
    job.setall('00 18 * * *')
    my_cron.write()

    print("Tests results will be written in: ./smashbox/etc/smashdir \n")
    print("Results are also sent to the smashbox dashboard in monit kibana service: https://monit-kibana.cern.ch")

else:
    print("Tests results will be written in: ./smashbox/etc/smashdir")

