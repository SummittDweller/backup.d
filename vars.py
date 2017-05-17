""" backup.d/vars.py

This Python script defines variables for use by backup.py, restore.py and migrate.py.
Define some critical vars.  These need to be modified for each project!  Use 'drush status' to determine some values.

"""

backup = "wieting.tar.gz"                                         # name the backup file
stick = "/Volumes/WIETING"                                        # name of a mounted drive to accept a copy of the backup
server = "wieting.tamatoledo.com"                                 # the remote server name
migrate_server = "wieting.dev"                                    # used by migrate.py to identify the destination server
user = "admin"                                                    # admin user on the remote server
migrate_user = "vagrant"                                          # used by migrate.py to identify the destination's user
drush_alias = "@wieting"                                          # drush alias for the remote site
migrate_alias = "@wieting.wieting.dev"                            # used by migrate.py to identify the desitnation's site drush alias
web_path = "/var/www/drupalvm/drupal/web/"                        # path to the Drupal web on the remote server
site_path = web_path + "sites/wieting"                            # path to the Drupal site on the remote server
migrate_path = web_path + "sites/default"                         # used by migrate.py to identify the destination site directory
drush = "/var/www/drupalvm/drupal/vendor/drush/drush/drush.php"   # remote server path to drush
