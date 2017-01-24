""" backup.d/vars.py

This Python script defines variables for use by backup.py and restore.py.
Define some critical vars.  These need to be modified for each project!  Use 'drush status' to determine some values.

Customized 17-Jan-2017 for Rootstalk.Grinnell.edu.

"""

backup = "rootstalk.tar.gz"                                       # name the backup file
stick = "/Volumes/RS"                                             # name of a mounted drive to accept a copy of the backup
server = "rootstalk.grinnell.edu"                                 # the remote server name
user = "dguser"                                                   # admin user on the remote server
drush_alias = "@rootstalk.prod"                                   # drush alias for the remote site
site_path = "/var/www/html/drupal/web/sites/default"              # path to the Drupal site on the remote server
drush = "/var/www/html/drupal/vendor/drush/drush/drush.php"       # remote server path to drush
