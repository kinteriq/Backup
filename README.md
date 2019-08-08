# Backup


#### Description:

Makes day-to-day backups easier.


##### Example:


###### _create a shortcut for later use:_
        python3 backup.py create documents ~/Documents/ ~/cloud_1/docs/ ~/cloud_2/docs/

###### _backup the content of ~/Documents/ to both ~/cloud_1/docs/ and ~/cloud_2/docs/:_
        python3 backup.py documents


#### Commands:
Command                                     | Description
--------------------------------------------|------------------------------------
*SHORTCUT_NAME*                             | backup
create *SHORTCUT_NAME PATH_FROM PATH_TO*    | add *SHORTCUT* to the database
delete *SHORTCUT_NAMEs*                     | delete *SHORTCUTs* from the database
update *SHORTCUT_NAMEs*                     | change *SHORTCUTs*' paths
show *SHORTCUT_NAMEs*                       | fetch *SHORTCUTs*' information
showall                                     | fetch *SHORTCUT_NAMEs* from the database
