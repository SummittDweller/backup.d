""" backup.d/vars.py

This Python script defines variables for use by backup.py and restore.py.
Define some critical vars.  These need to be modified for each project!  Use 'drush status' to determine some values.

"""

backup = "wieting.tar.gz"                                         # name the backup file
stick = "/Volumes/WIETING"                                        # name of a mounted drive to accept a copy of the backup
server = "wieting.summittdweller.com"                             # the remote server name
user = "mark"                                                     # admin user on the remote server
drush_alias = "@wieting"                                          # drush alias for the remote site
web_path = "/var/www/drupalvm/drupal/web/"                        # path to the Drupal web on the remote server
site_path = web_path + "sites/default"                            # path to the Drupal site on the remote server
drush = "/var/www/drupalvm/drupal/vendor/drush/drush/drush.php"   # remote server path to drush
