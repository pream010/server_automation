#!/usr/bin/powershell
#Developed for patch management project
#Check and install the PSWindowsUpdate module in the system
#Get the no. of available updates with details information
#Install the patches required to the system
#Created by - Preamkumar Umapathi on 02/17/2020
#Updated V0.1 - Preamkumar Umapathi on 02/18/2020 - Updated "-IgnoreReboot" in Install and check update command

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
    #Check if any updates available
    $searchresult=Get-WindowsUpdate -IgnoreReboot
    $pendingupdate=$searchresult.KB.Count
    if(!$pendingupdate)
    {
        Write-Host "No Updates Available"
    }
    else
    {
        #Install all patches
        Install-WindowsUpdate -AcceptAll -IgnoreReboot
    }
}

#END_OF_SCRIPT
