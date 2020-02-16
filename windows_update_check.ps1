#!/usr/bin/powershell
#Developed for patch management project
#Windows Last Patched Date Script
#Returns the no.of KBs pending to update
#Included pending reboot
#Created by - Preamkumar Umapathi on 01/31/2020

$Now = Get-Date -Format G
$hostname = $env:computername
$ostype = $env:OS
$os = Get-WmiObject win32_operatingsystem
$uptime = ((get-date) - ($os.ConvertToDateTime($os.lastbootuptime))).Days
$version = (Get-WmiObject -class Win32_OperatingSystem).Caption
$lastpatch = Get-WmiObject Win32_Quickfixengineering | select @{Name='InstalledOn';Expression={$_.InstalledOn -as [datetime]}} | sort-Object -Property InstalledOn |select-object -expandproperty installedon -last 1
$lastpatchs = (Get-Date $lastpatch -format "MM/dd/yyyy")
$updatesession=[activator]::CreateInstance([type]::GetTypeFromProgID("Microsoft.Update.Session",$hostname))
$updatesearcher=$updatesession.CreateUpdateSearcher()
$searchresult=$updatesearcher.Search("IsInstalled=0")
$pendingupdate=$searchresult.Updates.Count

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

#Check if any pending KBs needs to install
if ((!$pendingupdate) -and ($rebootpending -eq "no"))
{
  $patchstatus = "Patched"
}
else
{
  $patchstatus = "Not-Patched"
}

#print the output in the screen
"Datastamp="+$Now+"|"+"hostname="+$hostname+"|"+"OS="+$ostype+"|"+"OS_Version="+$version+"|"+"Status="+$patchstatus+"|"+"Pending_KB_Count="+$pendingupdate+"|"+"Pending_Reboot="+$rebootpending+"|"+"Last_KB_PatchDate="+$lastpatchs+"|"+"Uptime="+$uptime"|"

#END_OF_SCRIPT
