# EC Council Lab Notes

In the PowerShell, type 
## whoami /user 
and press Enter to display the details regarding Security ID (SID) and other additional information of the current user.

Now, type 
## get-aduser -identity administrator -properties * 
and press Enter to display user account information.

After changes in Server manager or to AD/Group Policy type 
## get-adcomputer -filter * | out-file C:\useraccounts.txt 
and press Enter to create a detailed report of all computer objects in the domain.

Administrator: Windows PowerShell, click to type 
## gpresult /H C:\passwords-policy-settings.html 
and press Enter to generate the report of password policy settings to update the configuration documentation.

