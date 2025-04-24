# FLARE-VM // Arsenal of Tools
In this task, we'll introduce you to tools inside the FlareVM. It has many specialized forensics, incident response, and malware investigation tools.

Below are the tools grouped by their category. 

## Reverse Engineering & Debugging
Reverse engineering is like solving a puzzle backward: you take a finished product apart to understand how it works. Debugging is identifying errors, understanding why they happen, and correcting the code to prevent them.

- Ghidra - NSA-developed open-source reverse engineering suite.
- x64dbg - Open-source debugger for binaries in x64 and x32 formats.
- OllyDbg - Debugger for reverse engineering at the assembly level.
- Radare2 - A sophisticated open-source platform for reverse engineering.
- Binary Ninja - A tool for disassembling and decompiling binaries.
- PEiD - Packer, cryptor, and compiler detection tool.

## Disassemblers & Decompilers
Disassemblers and Decompilers are crucial tools in malware analysis. 
They help analysts understand malicious software’s behaviour, logic, and control flow by breaking it into a more understandable format. 
The tools mentioned below are commonly used in this category.

- CFF Explorer - A PE editor designed to analyze and edit Portable Executable (PE) files.
- Hopper Disassembler - A Debugger, disassembler, and decompiler.
- RetDec - Open-source decompiler for machine code.

## Static & Dynamic Analysis
Static and dynamic analysis are two crucial methods in cyber security for examining malware. 
Static analysis involves inspecting the code without executing it, while dynamic analysis involves observing its behaviour as it runs. 
The tools mentioned below are commonly used in this category.

- Process Hacker - Sophisticated memory editor and process watcher.
- PEview - A portable executable (PE) file viewer for analysis.
- Dependency Walker - A tool for displaying an executable’s DLL dependencies.
- DIE (Detect It Easy) - A packer, compiler, and cryptor detection tool.

## Forensics & Incident Response
Digital Forensics involves the collection, analysis, and preservation of digital evidence from various sources like computers, networks, and storage devices. 
At the same time, Incident Response focuses on the detection, containment, eradication, and recovery from cyberattacks.
The tools mentioned below are commonly used in this category.

- Volatility - RAM dump analysis framework for memory forensics.
- Rekall - Framework for memory forensics in incident response.
- FTK Imager - Disc image acquisition and analysis tools for forensic use.

## Network Analysis
Network Analysis includes different methods and techniques for studying and analysing networks to uncover patterns, optimize performance, 
and understand the underlying structure and behaviour of the network.

- Wireshark - Network protocol analyzer for traffic recording and examination.
- Nmap - A vulnerability detection and network mapping tool.
- Netcat - Read and write data across network connections with this helpful tool.

## File Analysis
File Analysis is a technique used to examine files for potential security threats and ensure proper file permissions.

- FileInsight - A program for looking through and editing binary files.
- Hex Fiend - Hex editor that is light and quick.
- HxD - Binary file viewing and editing with a hex editor.

## Scripting & Automation
Scripting and Automation involve using scripts such as PowerShell and Python to automate repetitive tasks and processes,
making them more efficient and less prone to human error.

- Python - Mainly automation-focused on Python modules and tools.
- PowerShell Empire - Framework for PowerShell post-exploitation.

## Sysinternals Suite
The Sysinternals Suite is a collection of advanced system utilities designed to help IT professionals and developers manage, 
troubleshoot, and diagnose Windows systems.

- Autoruns - Shows what executables are configured to run during system boot-up.
- Process Explorer - Provides information about running processes.
- Process Monitor -Monitors and logs real-time process/thread activity.

------------------------------------------------------------------------------------------------------------------------------------------

## Commonly Used Tools for Investigation: Overview
Let's examine the tools we will focus on in this room. These tools are the basic ones used for initial investigations. See the list below.

### Tool	Investigative Value
Procmon	A helpful tool for tracking system activity, especially regarding malware research, troubleshooting, and forensic investigations.
Process Explorer	Allows you to see the Process of the Parent-child relationship, DLLs loaded, and its path.
HxD	Malicious files can be examined or altered via hex editing.
Wireshark	Observing and investigating network traffic to look for unusual activity.
CFF Explorer	Can generate file hashes for integrity verification, authenticate the source of system files, and validate their validity.
PEStudio	Static analysis or studying executable file properties without running the files.
FLOSS	Extracts and de-obfuscates all strings from malware programs using advanced static analysis techniques. 

You can follow along and open the tools and files on the FlareVM while we discuss the overview of some of these tools.


### Process Monitor (Procmon)
A powerful Windows tool designed to help you record issues with your system's apps. It lets you see, record, and keep track of system and Windows file activity in real-time. Process Monitor is helpful for tracking system activity, especially regarding malware research, troubleshooting, and forensic investigations. It keeps real-time tabs on the file system, registry, and thread/process activity.

Here's how to utilize it effectively for investigation.

the image shows how to leverage the tool. Here, we filtered for the process lsass.exe to see information about it.

According to this log entry, the Local Security Authority Subsystem Service (LSASS)- related process lsass.exe has successfully read a file. LSASS handles authentication and frequently communicates with crucial system files such as lsasrv.dll (Local Security Authority Server Service).

Although this is a standard system process, LSASS may be the target of credential dumping attacks if you are examining logs for indications of malicious activity. Mimikatz and other tools frequently try to access LSASS memory. In these situations, you should watch for any additional suspicious activity related to LSASS, such as odd access patterns or processes reading or writing to lsass.exe.

Don’t worry—the sample above does not show any malware signs!


### Process Explorer (Procexp)
Process Explorer offers in-depth insights into the active processes running on your computer. It allows you to delve into the inner workings of your system, providing a comprehensive list of currently running processes and their linked user accounts. If you've ever been curious about which program is accessing a specific file or folder, Process Explorer can provide us with that information.

The image shows the process and it's parent. We can validate the process ID and other information of the process here

As you can see from the image above, the CFF Explorer app is open. Using Process Explorer(procexp), located on the desktop, we identified the process and its parent process. This is usually pretty useful when we want to monitor what other processes are being spawned, such as from a Word document, an LNK file, or even an ISO file, as threat actors typically abuse these.


### HxD
HxD is a quick and flexible hex editor for editing files, memory, and drives of any capacity. It can be applied to forensic investigation, data recovery, debugging, and exact manipulation of binary data. Important features include viewing file and memory contents, editing, searching, and comparing hex data. Let's look at how the tool works.

The image shows the hex value of a file

This HxD hex editor snapshot shows the binary file possible_medusa.txt. The hex data on the left indicates the file's contents in hexadecimal, and the ASCII interpretation appears on the right. Interestingly, the file starts with 4D 5A (Little Endian), indicating it is executable.
The Data Inspector on the right allows you to examine individual bytes by displaying their values in many data types (e.g., integer, float), facilitating a more straightforward data evaluation.

By permitting in-depth examination of a file's unprocessed hexadecimal data, HxD facilitates inquiry by identifying file kinds, structures, and possible corruption. Its Data Inspector feature helps by offering insights into particular byte values.


### CFF Explorer
With the help of CFF Explorer's comprehensive file information, investigators can generate file hashes for integrity verification, authenticate the source of system files, and validate their validity (e.g., by looking for unusual alterations). This is important to know when analyzing malware since dangerous code may be hidden in altered system files.the image shows the information of the file when opened using the CFF explorer tool.

The cryptominer.bin file's details are displayed in the sample. On September 23, 2024, a 64-bit Portable Executable file was generated. The file's information can be verified by its hashes (SHA-1 and MD5). During investigations, this tool aids in confirming file information lookup and locating possible problems.


### Wireshark
Regarding network traffic analysis, Wireshark is a powerful tool that investigators may use to hunt down dubious connections, examine protocols, and spot possible assaults or data exfiltration. In this case, TLSv1.2 suggests a secure, encrypted connection that can mask harmful activity or safeguard legitimate traffic.

the image shows the capabilities of wireshark such as capturing the network traffic. We can see here the source and destination IP and also the port and protocol used.

This Shows captured packets with details about the protocol, source, destination, and other information. Most packets show that TLSv1.2 and TCP are being used for encrypted transmission. The raw packet data is shown in ASCII and hexadecimal forms, with a significant chunk encrypted using TLSv1.2.


### PEStudio
Static analysis, or studying executable file properties without running the files, is done with PEstudio. This feature is beneficial in several situations. PEstudio offers a variety of information about a file without putting users in danger of execution, which aids in identifying executables that seem suspect or harmful.

So, how does it work? Let's look at the image below.

this image shows information about the certain file that you wish to examine.

This example shows the examination of an executable file, PSexec.exe ( not in the VM; this is a pure example only), using PEstudio 9.22, a static malware analysis tool. The file has a dual purpose—legitimate for system administrators but potentially exploited by hackers for remote access.

The file's entropy value of 6.596 indicates a remote chance of packing or encryption, which is typical of dangerous software. Version 2.34 of this 32-bit console-based application allows it to run programs remotely, a feature frequently used to migrate laterally during attacks. The file is assembled using Visual C++ 8.

The dual-use nature of PsExec, typically legitimate but suspicious in compromised environments, combined with low to medium indicators and moderately high entropy, makes its presence on a system concerning, especially if remote code execution is not expected. Its use in post-exploitation phases warrants further investigation to determine if it’s being misused maliciously.


### FLOSS
Using advanced static analysis techniques, the FLARE Obfuscated String Solver (FLOSS, formerly FireEye Labs Obfuscated String Solver) automatically extracts and de-obfuscates all strings from malware programs. Like strings.exe, it can enhance the basic static analysis of unknown binaries. FLOSS also includes more Python scripts in the script's directory, which can be used to load the script's output into other programs like IDA Pro or Binary Ninja.

Terminal
PS C:\Users\Administrator\Desktop\Sample > floss .\cobaltstrike.exe
INFO: floss: extracting static strings
finding decoding function features: 100%|█████████████████████████████████████████████| 74/74 [00:00<00:00, 2370.15 functions/s, skipped 0 library functions]
INFO: floss.stackstrings: extracting stackstrings from 50 functions
extracting stackstrings: 100%|██████████████████████████████████████████████████████████████████████████████████████| 50/50 [00:00<00:00, 128.00 functions/s]
INFO: floss.tightstrings: extracting tightstrings from 4 functions...
extracting tightstrings from function 0x402e80: 100%|██████████████████████████████████████████████████████████████████| 4/4 [00:00<00:00, 31.99 functions/s]
INFO: floss.string_decoder: decoding strings
emulating function 0x402e80 (call 1/1): 100%|████████████████████████████████████████████████████████████████████████| 21/21 [00:09<00:00,  2.21 functions/s]
INFO: floss: finished execution after 265.61 seconds
INFO: floss: rendering results 

View Results
In the example above, FLOSS extracted 189 static strings from the binary, which may contain hardcoded information such as file paths, URLs (likely for command-and-control servers), IP addresses, API calls, error messages, registry, encryption keys, and configuration data. However, no decoded strings were identified, suggesting that FLOSS did not detect or decode dynamically generated or obfuscated strings during this analysis. Malware frequently uses obfuscated strings to conceal its malicious behavior.

NOTE** Defanged format means replacing . with [.] to prevent accidental clicking or execution.

