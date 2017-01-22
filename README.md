Use these Python scripts from the command line (terminal) to backup and restore a Drupal 8 project/site as a _project_.tar.gz containing an SQL dump and a tar of vars.site_path files.

**This script must exist in a ./backup.d directory inside your project directory!**
  
A vars.py script must also exist in this same directory and it must be modified to define your site and user parameters BEFORE performing any backup/restore operations.

Backups will be stored in and restored from a .data directory off the parent directory where the project lives.

The typical project tree structure looks like this...
```
project/
  file1
  file2
  file3
  backup.d/     
    backup.py
    restore.py
    vars.py
    README.md   <<< This file.
  .data/
    project.tar.gz_timestamp
    other_data1
    other_data2
   
```
You should invoke backup and subsequent restore using commands of the form...
```
cd project_directory
python backup.d/backup.py

```
...and...
```
cd project_directory
python backup.d/restore.py

```
## Dependencies
The SSH feature (see below) reqiures installation of ssh-copy-id.
  On your Mac use... `brew install ssh-copy-id`
The scripts also reqiure the Python _colorama_ library.  
  On your Mac use... `pip install colorama`

##A Note About SSH
If the user of this script has a valid private|public **id_rsa** key pair in **~/.ssh** these scripts will attempt to push the public key (**id_rsa.pub**) out to the remote server so that passwordless **_sudo_** access is automatic. 
