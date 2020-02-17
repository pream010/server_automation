#!/usr/bin/powershell
#Developed for patch management project
#Check and install the PSWindowsUpdate module in the system
#Get the no. of available updates with details information
#Created by - Preamkumar Umapathi on 02/17/2020

#SCRIPT_START

#Check if the PSWindowsUpdate module is available
if (Get-Module -Listavailable -Name PSWindowsUpdate -EA Ignore)
{
    #PSWindowsUpdate module is installed
}
else
{
    #Install PSWindowsUpdate module
    Install-Module -Name PSWindowsUpdate -Force
}

#Import PSWindowsUpdate module
if (Import-Module -Name PSWindowsUpdate -EA Ignore)
{
    Write-Host "Issue with Import PSWindowsUpdate module, please check with your administrator"
}
else
{
    #list the no. of updates available
    Get-WindowsUpdate
}

#END_OF_SCRIPT
