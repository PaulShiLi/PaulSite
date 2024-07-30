# Linux Cheat sheet

---

#### Basic Commands

1. Finds all files of a certain pattern in a given directory

   ```bash
   find -iname "<fileName>"
   ```

2. Finds all files of a certain extension in a given directory

   ```bash
   find -iname "*.<fileExtension>"
   ```

3. Copy paste a file to another directory

   ```bash
   cp <file> <destination>
   ```

4. Move a file or rename a file

   ```bash
   mv <file> <destination>
   ```

---

#### Group Management

1. List all groups in the system

   ```bash
   sudo less /etc/group
   ```

2. Check users of a given group

   ```bash
   getent group groupname
   ```

3. Add an existing user to a group

   ```bash
   sudo usermod -a -G <username> <groupname>
   ```

4. Remove user from a group

   ```bash
   sudo deluser <username> <groupname>
   ```

---

#### User management

1. Find user ID of a user

   ```bash
   id -u <username>
   ```

2. Delete a user

   ```bash
   userdel [options] <username>
   ```

   | Options | Description                                                                            |
   |:-------:|:--------------------------------------------------------------------------------------:|
   | -f      | Forcefully delete a user account and also with forceful removal of files               |
   | -r      | Deletes user account along with mail spool and user’s home directory                   |
   | -z      | Deletes SELinux users if they are mapped for the users while deleting user from Linux. |

3. Add user

   ```bash
   useradd [options] <username>
   ```

   | Options             | Description                                                                                                                                                                                                                               |
   |:-------------------:|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------:|
   | -m                  | Creates user home directory under `/home/username`                                                                                                                                                                                        |
   | -u [custom userID]  | Creates user with specified custom user id                                                                                                                                                                                                |
   | -g [loginGroupName] | Assigns user to initial login group.<br>Default login group is the user's username.                                                                                                                                                     |
   | -G [otherGroups]    | Adds user to additional groups.<br>`sudo useradd -G group1,group2 <username>`                                                                                                                                                           |
   | -c [customComment]  | Adds a short description for the new user<br>`sudo useradd -c "Comment" <username>`<br>The comment is saved in `/etc/passwd`<br>`grep <username> /etc/passwd`<br>Output: `<username>:x :1001:1001:Comment:/home/username:/bin/sh` |
   | -e [YYYY-MM-DD]     | Adds account expiry date to user<br>`sudo useradd -e 2019-01-22 <username>`                                                                                                                                                             |

---

#### Miscellaneous Commands

1. Finding Extents of a file

   ```bash
   filefrag -e <filePath>
   ```

   Example:

   `root@hawkins-national-labratory:/home/eleven/Desktop# filefrag -e ST_Linux_1_0.tar.gz`

   `Filesystem type is: ef53
   File size of ST_Linux_1_0.tar.gz is 18707973 (4568 blocks of 4096 bytes)`

   | ext: | logical_offset: | physical_offset:                              | length: | expected: | flags:   |
   | ---- | --------------- | --------------------------------------------- | ------- | --------- | -------- |
   | 0:   | 0..4095:        | <mark>2529280</mark> .. <mark>2533375</mark>: | 4096:   |           |          |
   | 1:   | 4096..4567:     | <mark>2523136 </mark>.. <mark>2523607</mark>: | 472:    | 2533376:  | last,eof |

   `ST_Linux_1_0.tar.gz: 2 extents found`

2. Finding user expiry date

   ```bash
   chage -l <username>
   ```
