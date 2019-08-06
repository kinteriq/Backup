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
**shortcut**                             | backup
create **shortcut from_path to_paths**   | add **shortcut** to the database
delete **shortcuts**                     | delete **shortcuts** from the database
update **shortcuts**                     | change **shortcuts**' info in the database
show **shortcuts**                       | fetch **shortcuts**' information
showall                                  | fetch **shortcuts** from the database
