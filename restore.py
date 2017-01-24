""" backup.d/restore.py

Use this Python script from the command line (terminal) in combination with backup.py. You should first cd to
  your project directory holding one or more *.tar.gz backups in a .data directory.  This
  script will always select the most recent copy of .data/*.tar.gz OR it will pull the latest from a mounted
  and properly named USB stick (see vars.py) for name details.

This script must exist in a ./backup.d directory.  Corresponding scripts vars.py and backup.py must also
exist in this same directory and vars.py must be modified to define your site and user parameters BEFORE
performing any backup/restore operations.

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
import glob
import subprocess

init()

# Get the current (working) directory and verify that necessary parts are in place.
cwd = os.getcwd()
print Style.BRIGHT + Fore.GREEN + "\nThe current (working) directory is '" + cwd + "'." + Style.RESET_ALL

if (not os.path.isdir(".data")):
  print Style.BRIGHT + Fore.RED + "\nThe required .data/ directory does NOT exist.  This process is terminated.\n" + Style.RESET_ALL
  exit(1)

if (not os.path.isdir("backup.d")):
  print Style.BRIGHT + Fore.RED + "\nPlease change directories.  The required backup.d/ directory does NOT exist.  This process is terminated.\n" + Style.RESET_ALL
  exit(1)

# OK, build some credentials and paths
userAtServer = vars.user + "@" + vars.server
path = "/home/" + vars.user + "/" + vars.backup
local = cwd + "/.data"

# Determine the user's home directory so we can check for a public SSH key.
homeDir = os.path.expanduser("~")
pubKey = homeDir + "/.ssh/id_rsa.pub"

# If the user of this script has an id_rsa|id_rsa.pub (private|public) key pair, append the public key the remote user's ~/.ssh/authorized_keys.
if os.path.isfile(pubKey):
  args = [ "ssh-copy-id", "-i", pubKey, userAtServer ]
  print Style.BRIGHT + "\nLaunching remote " + Fore.GREEN + " ".join(args) + Fore.RESET + " to establish key file authentication..."
  error = subprocess.check_call(args)
else:
  print Style.BRIGHT + Fore.RED + "\nNo ~/.ssh/id_rsa.pub public key found so the " + userAtServer + " password may be required several times. " + Fore.RESET

# If stick is mounted, copy the latest backup from there to the current directory
if os.path.isdir(vars.stick):
  stick_path = max(glob.iglob(vars.stick + "/" + vars.backup + '*'), key=os.path.getctime)
  args = ["rsync", "-aruvi", stick_path, local]
  print Style.BRIGHT + "\nRunning " + Fore.GREEN + ' '.join(args) + Style.RESET_ALL + " to copy the latest backup from your mounted " + vars.stick + " volume..." 
  error = subprocess.check_call(args)
else:
  print Style.BRIGHT + "\nMount a portable drive at " + vars.stick + " to pull backups for restoration." + Style.RESET_ALL

# Find the latest file matching the backup* filename pattern
file_path = max(glob.iglob(local + "/" + vars.backup + '*'), key=os.path.getctime)

# rsync (push) the file to the remote from this host
args = [ "rsync", "-aruvi", file_path, userAtServer + ":" + path ]
print Style.BRIGHT + "\nRunning '" + Fore.GREEN + ' '.join(args) + Fore.RESET + "' to copy the backup to the server..."  + Style.RESET_ALL
error = subprocess.check_call(args)

# Extract everything from the tar file to /tmp/restore
command = "mkdir /tmp/restore; tar -xzvf " + path + " -C /tmp/restore" 
args = [ "ssh", userAtServer, command ]
print Style.BRIGHT + "\nLaunching " + Fore.GREEN + " ".join(args) + Fore.RESET + " to extract files from the backup to /tmp/restore... " + Style.RESET_ALL
error = subprocess.check_call(args);

# Make sure vars.site_path is writeable and rsync /tmp/restore/ to vars.site_path 
command = "chmod 777 " + vars.site_path + "; rsync -ruv /tmp/restore/ " + vars.site_path
args = [ "ssh", userAtServer, command ]
print Style.BRIGHT + "\nLaunching " + Fore.GREEN + " ".join(args) + Fore.RESET + " to copy files from /tmp/restore to the destination... " + Style.RESET_ALL
error = subprocess.check_call(args);

# Define a drush sql-cli command to restore the database
command = "sql-cli < " + vars.site_path + "/files/" + vars.server + ".sql"
args = [ "ssh", userAtServer, vars.drush, vars.drush_alias, command ]
print Style.BRIGHT + "\nLaunching remote " + Fore.GREEN + " ".join(args) + Fore.RESET + " to restore the database from backup..." + Style.RESET_ALL
error = subprocess.check_call(args);

# Use drush to flush the cache
command = "cr all"
args = [ "ssh", userAtServer, vars.drush, vars.drush_alias, command ]
print Style.BRIGHT + "\nLaunching remote " + Fore.GREEN + " ".join(args) + Fore.RESET + " to flush the site cache"
error = subprocess.check_call(args);

# Cleanup the remote sever
args = [ "ssh", userAtServer, "rm -f", path + "* ", vars.site_path + "/files/*.sql" ]
print Style.BRIGHT + "\nLaunching " + Fore.GREEN + " ".join(args) + Fore.RESET + " to cleanup the remote server... " + Style.RESET_ALL
error = subprocess.check_call(args)

print "\n\n"
