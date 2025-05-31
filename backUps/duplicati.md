# Duplicati
Duplicati is a cross-platform backup solution also with strong capabilities. 

It also supports AES-256 for encryption, with optional asymmetric encryption using GPG (RSA or similar for key exchange). 

Data is encrypted client-side and it supports strong password-based key derivation. 

A great advantage for many people is the number of remote destinations Duplicati supports:
- Google Drive
- OneDrive
- Amazon S3
- SFTP
- Dropbox

and others.

The installation process is also very simple but instead of using a GUI, Duplicati is uses a webserver for management. 

Let’s download the installation package and install it.

  Backups and Recovery
cry0l1t3@hbt[/htb]$ cd ~/Downloads
cry0l1t3@hbt[/htb]$ sudo apt install ./duplicati-2.1.0.5_stable_2025-03-04-linux-x64-gui.deb
cry0l1t3@hbt[/htb]$ duplicati
Once installed, we can navigate to http://localhost:8200 and will see a webpage similar to this:

Duplicati interface showing 'Add a new backup' with options to configure a new backup or import from a file, and a 'Next' button.

In the Add backup tab we can start to specify our general backup settings, give it a name, set encryption and the passphrase for it.

Duplicati backup settings screen with fields for 'Name', 'Description', 'Encryption', 'Passphrase', and 'Repeat Passphrase', and a 'Next' button.

In this example, we’ll configure Duplicati to make backups and send them to a remote server. One of the most recommended and most secure methods is the file transfer through SSH/SFTP by using SSH keys. 

Therefore, we need to generate a separate SSH key by using the ssh-keygen command.

  Backups and Recovery
cry0l1t3@hbt[/htb]$ ssh-keygen -t ed25519

Generating public/private ed25519 key pair.

Enter file in which to save the key (/home/cry0l1t3/.ssh/id_ed25519): duplicati
Enter passphrase (empty for no passphrase): ******************
Enter same passphrase again: ******************

Your identification has been saved in duplicati
Your public key has been saved in duplicati.pub
The key fingerprint is:
SHA256:2mKNI0ZOfVMuwkFenV4NtUv0hwiHTir0gGYfR/Lhm8Q cry0l1t3@ubuntu
The key's randomart image is:
+--[ED25519 256]--+
|     .o.+..oo+o  |
|    +o+*..=o.o.+ |
|   o oo=E=... + o|
|     oooo=o  . ..|
|    o +.S .   .  |
|   +   B o       |
|    + * o        |
|   . o o         |
|                 |
+----[SHA256]-----+
Once the SSH key has been created we now can specify the storage type, remote IP addres and port, path on the server, username and in Advanced options we can add the authentication method ssh-key.

Duplicati backup destination setup with SFTP, server IP 10.129.12.122, port 50022, path '/home/duplicati', username 'duplicati', and 'Test connection' button.

After that we can select the source data that needs to be backed up. A huge advantage that Duplicati provides is the filter functionality using regular expressions.

Duplicati source data selection screen with folder tree for 'User data' and 'Computer', option to show hidden folders, and filter settings.

As the last step we can configure the schedule for the backups.

Duplicati schedule screen with 'Automatically run backups' checked, next run at 01:00 PM on 04/27/2025, repeating every day, with all days selected.

It is highly recommended that your backups (especially when they are stored on a remote server) are encrypted at rest and in transit. 
This means that your data should be stored in repositories and during the transfer. 

Both Pika Backup and Duplicati support this functionality and therefore help organizations to fullfil compliance regulations like GDPR and HIPPA.

We also recommend to simulate a Disaster Recovery situation where your server all of the sudden doesn’t work properly anymore or data has been lost and you need to recover the last state of it from scratch. 
While going through this process you will learn what kind of things can happen during recovery and if your process works as expected. 
Keep in mind that you should keep notes and document the process step-by-step so you have a continuity plan in place that you can use to restore your data. 
We also recommend to simulate this situation twice a year or once a quarter to ensure that the process you have set up works as expected. 
Because when things brake, your continuity plan is your last to restore everything you have built.

