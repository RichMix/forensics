Pika Backup
[Pika](https://apps.gnome.org/PikaBackup/)
Pika Backup is a user-friendly backup solution with a GUI which allows us to create backups locally and remotely. 
A big advantage is that it doesn’t copy files it already copied. It copies only new files or files that have been modified since the last backup. 
Additionally it supports encryption which adds another layer of security and its easy to set up.

  Backups and Recovery
# Update
cry0l1t3@hbt[/htb]$ sudo apt update -y 

# Install Pika Backup
cry0l1t3@hbt[/htb]$ sudo apt install flatpak -y
cry0l1t3@hbt[/htb]$ flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo
cry0l1t3@hbt[/htb]$ flatpak install flathub org.gnome.World.PikaBackup

# Run Pika Backup
cry0l1t3@hbt[/htb]$ flatpak run org.gnome.World.PikaBackup
Once we have started Pika Backup we can setup the backup process and configure it the way we need.

Pika Backup screen showing 'No Backup Configured' with a button to 'Setup Backup'.

Pika Backup uses BorgBackup repositories, which are directories containing (encrypted and) deduplicated archives. 
Deduplicated archives is a type of data archive where redundant copies can be identified and removed to reduce storage space and improve efficiency. 
Each data in an archive is split into a smaller chunk and based on its content it is assigned to a unique hash. If a chunk’s hash matches an existing one it will be discarded. 
In production environments where the host can be access through the internet (e.g. web server) it is recommended to follow the 3-2-1 rule:

3 copies of your data
2 on different devices
1 offsite
Pika Backup setup screen with options to create or use existing repository, showing 'Location on Disk' and 'Remote Location' for both.

We can specify the location where the local repository can be created. In this example, we will use a connected HDD with a directory called backup.

Pika Backup location selection screen showing 'Repository Base Folder' set to 'backup' and 'Repository Name' as 'backup-ubuntu-cry0l1t3' with a 'Continue' button.

Once the directory for the repository is specified, we can setup the encryption phrase that Pika Backup uses in order to encrypt all our archives. T
he same way as BorgBackup, Pika Backup employs AES-256-CTR encryption which provides high security.

Pika Backup encryption setup screen with 'Use Encryption' toggled to 'Encrypted', showing password fields for new and repeated password, and a 'Create' button.

After the encryption has been set, we can move on and initiate the first backup or dive deeper into the configuration—exploring things such as the schedule, included, and excluded files and directories.

In this example, we’re going to backup just the home directory as you can see in the Files to Back up section and exclude all Caches.

Pika Backup screen showing 'Backup Never Ran' with options to back up 'Home' folder and exclude 'Caches', and a 'Back Up Now' button.

For the archives we can specify an archive index of our choice. We also can run the Data Integrity Check manually which checks the latest backup archives with the current status and makes updates if any files has been modified since the last backup.

Pika Backup archives screen showing 'home' directory with 20.4 GB available of 52.5 GB total, options for 'Archive Prefix' and 'Cleanup Archives', and 'No Integrity Check' performed. No archives available.

In the Schedule tab we can specify how often a backup needs to be created. The recommended schedule is to do a backup daily for 2 weeks period.

Pika Backup schedule screen showing 'Waiting for Backup to Start', with options to regularly create backups daily at 21:00, and to regularly clean up archives. 'Save Configuration' button is present.

Once everything is set up, we can launch the backup process and wait until its finished.

Pika Backup screen showing 'Backup Running' at 4.0% for 'home' directory, with options to abort, and lists of files to back up and exclude.

