# Backup


## Description:

Makes day-to-day backups easier.


#### Example:


###### _create a shortcut for later use:_
        python3 backup.py create documents ~/Documents/ ~/cloud_1/docs/ ~/cloud_2/docs/

###### _backup the content of ~/Documents/ to both ~/cloud_1/docs/ and ~/cloud_2/docs/:_
        python3 backup.py documents

---

## Commands:
Command          | Description
-----------------|------------------------------------
help             | get documentation
create           | create a shortcut
delete           | delete a shortcut
update           | change shortcut's source and/or destination paths
show             | fetch shortcut's source and destination paths
showall          | fetch all shortcuts from the database
*shortcut*\*     | do a backup
clear            | delete all shortcuts from the database

### __create__:
create _shortcut-name source-path destination-path_
- __shortcut-name__: any name you would like
- __source-path__: path to the directory which you need to copy from
- __destination-path__\*\*: path to the directory you need to copy to (can enter several paths separated by space)

        python3 backup.py create documents ~/Documents/ ~/cloud_1/docs/ ~/cloud_2/docs/

\*\* _Add separator at the end if the directory already exists,\
otherwise, there should be no separator at the end of the path._

### __delete__:
delete _shortcut-name_
- __shortcut-name__: name (or names separated by space) that you want to delete

         python3 backup.py delete documents
         python3 backup.py delete photos documents

### __update__\*\*\*:
update _shortcut-name_
- __shortcut-name__: name (or names separated by space) that you want to update

         python3 backup.py update documents
         python3 backup.py update photos documents

\*\*\* _You will be asked to change source and/or destination paths in the interactive mode;\
In order to keep the current information simply press ENTER to skip._

### __show__:
show _shortcut-name_
- __shortcut-name__: name (or names separated by space) that you want to see the saved information about

         python3 backup.py show documents
         python3 backup.py show photos documents

### __showall__:

        python3 backup.py showall

### __*shortcut*\*__:
\* custom name (or names separated by space) saved in the database

        python3 backup.py documents
        python3 backup.py photos documents
