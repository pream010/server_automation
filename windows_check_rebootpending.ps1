#!/usr/bin/powershell
#Reboot the system if it's pending with reboot

#SCRIPT_START

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
    Write-Host "No Reboot Required"
}
else
{
    Restart-Computer -Force
}

#END_OF_SCRIPT
