# Backup


#### Description:

Makes day-to-day backups easier.


##### Example:


###### _create a shortcut for later use:_
        python3 backup.py create documents ~/Documents/ ~/cloud_1/docs/ ~/cloud_2/docs/

###### _backup the content of ~/Documents/ to both ~/cloud_1/docs/ and ~/cloud_2/docs/:_
        python3 backup.py documents


#### Commands:
Command                                  | Description
-----------------------------------------|------------------------------------
*Shortcut*                               | backup
create *Shortcut* *From_path* *To_paths* | add *Shortcut* to the database
delete *Shortcuts*                       | delete *Shortcuts* from the database
update *Shortcuts*                       | change *Shortcuts*' info in the database
show *Shortcuts*                         | fetch *Shortcuts*' information
showall                                  | fetch *Shortcuts* from the databases
