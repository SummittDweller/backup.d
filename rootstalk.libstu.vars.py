""" backup.d/vars.py

This Python script defines variables for use by backup.py and restore.py.
Define some critical vars.  These need to be modified for each project!  Use 'drush status' to determine some values.

Customized 17-Jan-2017 to backup Rootstalk.Grinnell.edu.

"""

backup = "rootstalk.tar.gz"                                       # name the backup file
stick = "/Volumes/RS"                                             # name of a mounted drive to accept a copy of the backup
server = "rootstalk.grinnell.edu"                                 # the remote server name
user = "libstu"                                                   # admin user on the remote server
drush_alias = "@rootstalk.prod"                                   # drush alias for the remote site
web_path = "/var/www/html/drupal/web/"                            # path to the Drupal web root on the remote server
site_path = web_path + "sites/default"                            # path to the Drupal site on the remote server
drush = "/var/www/html/drupal/vendor/drush/drush/drush.php"       # remote server path to drush

