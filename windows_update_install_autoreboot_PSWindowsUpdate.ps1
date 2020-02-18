#!/usr/bin/powershell
#Developed for patch management project
#Check and install the PSWindowsUpdate module in the system
#Get the no. of available updates with details information
#Install the patches required to the system
#Autoreboot the system once the patches installed (check wheather it's required reboot or not)
#Created by - Preamkumar Umapathi on 02/18/2020

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
        Write-Host "Updates=No Updates Available"
        
        #Check for pending reboot
        if (Get-ChildItem "HKLM:\Software\Microsoft\Windows\CurrentVersion\Component Based Servicing\RebootPending" -EA Ignore)
        {
          $rebootpending="yes"
        }
        elseif (Get-Item "HKLM:\Software\Microsoft\Windows\CurrentVersion\WindowsUpdate\Auto Update\RebootRequired" -EA Ignore)
        {
          $rebootpending="yes"
        }
        else
        {
          $rebootpending="no"
        }

        #Reboot the system if its pending with reboot
        if ($rebootpending -eq "no")
        {
            Write-Host "Reboot=No Reboot Required"
        }
        else
        {
            Restart-Computer -Force
        }
    }
    else
    {
        #Install all patches
        Install-WindowsUpdate -AcceptAll -IgnoreReboot
        
        #Check for pending reboot
        if (Get-ChildItem "HKLM:\Software\Microsoft\Windows\CurrentVersion\Component Based Servicing\RebootPending" -EA Ignore)
        {
          $rebootpending="yes"
        }
        elseif (Get-Item "HKLM:\Software\Microsoft\Windows\CurrentVersion\WindowsUpdate\Auto Update\RebootRequired" -EA Ignore)
        {
          $rebootpending="yes"
        }
        else
        {
          $rebootpending="no"
        }

        #Reboot the system if its pending with reboot
        if ($rebootpending -eq "no")
        {
            Write-Host "Reboot=No Reboot Required"
        }
        else
        {
            Restart-Computer -Force
        }
    }
}

#END_OF_SCRIPT
