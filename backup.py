""" backup.d/backup.py

Use this Python script from the command line (terminal) in combination with restore.py.  This script will create a
 *.tar.gz containing an SQL dump and a tar of vars.site_path files.

This script must exist in a ./backup.d directory inside your project directory.  Corresponding scripts vars.py and
restore.py must also exist in this same directory and vars.py must be modified to define your site and user
parameters BEFORE performing any backup/restore operations.

Backups will be stored in and restored from a .data directory off the parent directory where the project lives.

The typical project tree structure looks like this...

project/
  file1
  file2
  file3
  backup.d/
    backup.py
    restore.py
    vars.py
  .data/
    project.tar.gz_timestamp
    other_data1
    other_data2

"""

from colorama import init
from colorama import Style, Fore, Back
import vars
import os
import subprocess
import sys
from datetime import datetime

init()  # for Colorama

# Get the current (working) directory and verify that necessary parts are in place.
cwd = os.getcwd()
print Style.BRIGHT + Fore.GREEN + "\nThe current (working) directory is '" + cwd + "'." + Style.RESET_ALL

if (not os.path.isdir("backup.d")):
  print Style.BRIGHT + Fore.RED + "\nPlease change directories.  The required backup.d/ directory does NOT exist.  This process is terminated.\n" + Style.RESET_ALL
  exit(1)

if (not os.path.isdir(".data")):
  print Style.BRIGHT + Fore.RED + "\nThe required .data/ directory does NOT exist.  Let's make one now.\n" + Style.RESET_ALL
  os.mkdir(".data", 0776);

# Get the current time and build a destination file name
timeStamp = datetime.now().strftime('%Y-%m-%d_%H-%M')
file = vars.backup + "_" + str(timeStamp)
destination = "/home/" + vars.user + "/" + file
userAtServer = vars.user + "@" + vars.server
local = cwd + "/.data/" + file

# Cleanup the remote server before beginning
command = "rm -f /home/" + vars.user + "/" + vars.server + ".sql /home/" + vars.user + "/" + vars.backup
args = [ "ssh", userAtServer, command ]
print Style.BRIGHT + "\nLaunching " + Fore.GREEN + " ".join(args) + Fore.RESET + " to clean up... " + Style.RESET_ALL
error = subprocess.check_call(args);

# Try 'drush sql-dump' instead of 'drush ard', it's easier to control
command = "sql-dump --result-file=" + vars.site_path + "/files/" + vars.server + ".sql --skip-tables-key=common"
args = [ "ssh", userAtServer, vars.drush, vars.drush_alias, command ]
print Style.BRIGHT + "\nLaunching " + Fore.GREEN + " ".join(args) + Fore.RESET +" to dump the database... " + Style.RESET_ALL
error = subprocess.check_call(args);

# Follow up with a 'tar' command under better control
skip = [ "config_*", "*/css/*", "*/js/*", "*/php/*", "*services.yml", "*settings.php" ]
exclude = " --exclude=".join(skip)
command = "tar -czvf " + destination + " -C " + vars.site_path + " . /home/" + vars.user + "/*.sql --exclude=" + exclude
command = "tar -czvf " + destination + " -C " + vars.site_path + " . --exclude=" + exclude
args = [ "ssh", userAtServer, command ]
print Style.BRIGHT + "\nLaunching " + Fore.GREEN + " ".join(args) + Fore.RESET + " to create a backup... " + Style.RESET_ALL
error = subprocess.check_call(args);

# No problems thus far?...rsync the file back to the host
args = [ "rsync", "-aruvi", userAtServer + ":" + destination, local ]
print Style.BRIGHT + "\nRunning " + Fore.GREEN + ' '.join(args) + Fore.RESET + " to copy the backup to your host..."  + Style.RESET_ALL
error = subprocess.check_call(args)

# If stick is mounted, copy the backup there too
if os.path.isdir(vars.stick):
    args = ["rsync", "-aruvi", local, vars.stick]
    print Style.BRIGHT + "\nRunning " + Fore.GREEN + ' '.join(args) + Fore.RESET + " to copy the backup to your mounted " + vars.stick + " volume..."  + Style.RESET_ALL
    error = subprocess.check_call(args)
    
    files = filter(os.path.isfile, os.listdir(vars.stick))
    print "\nContents of " + vars.stick + " now includes: "
    for f in files:
        print "  " + f
    print "\n\n"

else:
    print Style.BRIGHT + "\nMount a portable drive at " + vars.stick + " and use "
    print Fore.GREEN + "  'rsync -aruvi " + local + " " + vars.stick + "' " + Fore.RESET + "to copy the backup there.\n\n" + Style.RESET_ALL