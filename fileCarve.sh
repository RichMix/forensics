# Forensics File Carving (Medium) - Fall NCL Gymnasium

#The security team has found a rather strange file exiting the network, we're not sure if it's 
# containing any sensitive information. Help us identify what's in it.
# This file initially looks like something green, what's the file format of this green file?

# Q2: How many files can be extracted from the binary blob?

# Q3 What is the hidden flag in the file?

# ChatGPT said: To approach this file carving and forensic analysis task, follow these steps to determine 
# the file format, extract embedded files, and identify any hidden flags.  
# You’ll need tools commonly used for file analysis, such as file, xxd, binwalk, foremost, or photorec, which are available in most forensic and Linux environments.

# Step 1: Identify the File Type

# Use the file Command: The file command identifies the format of a file based on its magic numbers or header.
file < suspicious_file >
# This should output the type of file, such as PNG, JPEG, or another common format.

# Examine File Headers with xxd:
# If the file type is ambiguous, you can manually inspect the header with xxd, which outputs a hex and ASCII dump of the file:
xxd < suspicious_file > | head

# Common headers to look for:
# PNG: Starts with 89 50 4E 47 (PNG).
# JPEG: Starts with FF D8 FF.
# GIF: Starts with 47 49 46 (GIF89a or GIF87a).
# BMP: Starts with 42 4D.

# This step should answer Q1, giving you the file format.

# Step 2: Extract Embedded Files from the Binary Blob (Q2)
# Use binwalk for File Extraction:

# Install binwalk 
brew install binwalk
# binwalk is a powerful tool that can scan for and extract multiple embedded files in binary blobs. Run:

# Binwalk the sus files
binwalk -e suspicious_file
binwalk -e extracts files into a folder (likely named _suspicious_file.extracted). Check the extracted files to see how many files were pulled out.

# Use foremost if Additional Carving is Needed:

# If binwalk doesn’t extract all files, use foremost, which performs advanced file carving by searching for file signatures:


# Install foremost
brew install foremost

bash
Copy code
foremost -i suspicious_file -o output_folder
In the output_folder, you’ll see directories with extracted files, sorted by type.
This step should answer Q2, giving you the number of extracted files.

Step 3: Find the Hidden Flag (Q3)
Search Extracted Files for Flags:

After extraction, check each file for hidden text, flags, or other content using strings, which prints readable text:
bash
Copy code
strings extracted_file | grep -i "flag"
Look for common flag formats (like FLAG{}, CTF{}, or other specific formats).
Check Metadata:

Some file formats like images and documents may hide flags in metadata. Use exiftool to inspect:
bash
Copy code
exiftool extracted_file
Inspect Suspicious Files Manually:

If no flag is found with strings or exiftool, open the extracted files (if they are images, documents, etc.) in their respective viewers or editors.


Share


You said:
Version Control (Easy)(60 points)
Cyber Command
One of our employee's computer was compromised and we saw this backup file leave the network, but we couldn't find anything other than a simple README.md file in it. Help us found out what information the hackers got.

8:29:15 pm
Cyber Command
What is the email address of the employee who was compromised? (10 pts)
8:29:15 pm
Richard Habib
gpeterson@mpd.hacknet.cityinthe.cloud
8:29:40 pm
Cyber Command
Correct! Good job so far.
8:29:40 pm
Cyber Command
Each employee is assigned a flag. What is the flag that was compromised? (20 pts)
8:42:57 pm
Richard Habib
-SKY-LRHX-4910
8:42:57 pm
Cyber Command
Correct! Good job so far.
8:42:57 pm
Cyber Command
Greg thinks that he may have had additional account credentials that were compromised. What's the name of the service provider for that other compromised account? (15 pts)
8:53:49 pm
Richard Habib
+Facebook: waffles85
8:53:49 pm
Cyber Command
Correct! Good job so far.
8:53:49 pm
Cyber Command
What was the password on that compromised account? (15 pts)
8:29:15 pm
Please provide step by step instructions on how to complete the task, read hidden files and capture flag from mac/linux terminal with codes and clear concise instructions
ChatGPT said:

To complete the task, we'll need to go through several steps in the terminal to examine any hidden files, read file contents, and check if there are embedded flags or sensitive information in the backup file. Here’s a step-by-step guide to get the necessary information:

Step 1: Set Up and Access the Backup File
Extract the Backup File (if compressed):

If the backup file is a compressed archive (e.g., .zip, .tar, .gz), use the appropriate command to extract it:
bash
Copy code
# For a .zip file
unzip backup_file.zip

# For a .tar.gz file
tar -xzf backup_file.tar.gz
Navigate to the Extracted Directory:

Change to the directory where the backup file was extracted.
bash
Copy code
cd backup_directory
Step 2: Locate Hidden Files and Directories
List All Files, Including Hidden Ones:

Use the ls -la command to see all files in the directory, including hidden ones (files starting with a dot .).
bash
Copy code
ls -la
This will display files like .config, .git, .env, or any other hidden files that might contain sensitive information.
Check for README.md:

If there’s a README.md file, open it to look for any clues or information.
bash
Copy code
cat README.md
Step 3: Search for Sensitive Information in Files
Search for Email, Flag, and Password:

Use grep to look for specific keywords like "email," "flag," or "password" in all files, including hidden ones.
bash
Copy code
grep -ri "email" .
grep -ri "flag" .
grep -ri "password" .
The -r option makes grep search recursively through all directories, and -i makes the search case-insensitive.
Examine .git Directory (if present):

Sometimes, sensitive information is hidden in Git repositories. If there’s a .git directory:
List commits and examine the commit messages and content:
bash
Copy code
git log
git show <commit_id>  # Replace <commit_id> with specific commit hash if found
Step 4: Check for Environment and Configuration Files
Look for .env or Configuration Files:
Environment files (.env) or configuration files (e.g., .config) may contain sensitive information like email, flags, or passwords.
If an .env file is found, read it using:
bash
Copy code
cat .env
Step 5: Capture and Document Flag and Other Credentials
Document Information as You Find It:
For each piece of information (email, flag, account provider, password), record it carefully.
If you find additional flags or credentials, use the format provided by Cyber Command to report them.
Example Commands in Sequence
bash
Copy code
# Extract backup if compressed
unzip backup_file.zip  # or tar -xzf backup_file.tar.gz

# Move into the backup directory
cd backup_directory

# List all files, including hidden
ls -la

# Check README.md for clues
cat README.md

# Search for email, flags, or passwords
grep -ri "email" .
grep -ri "flag" .
grep -ri "password" .

# If there's a .git folder, inspect the commits
git log
git show <commit_id>  # Replace <commit_id> with the actual commit ID if needed

# If an .env file is found, view its content
cat .env

# This approach will help you uncover any hidden or embedded information, such as 
# email addresses, flags, and passwords in the compromised backup file.
