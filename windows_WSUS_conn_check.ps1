#!/usr/bin/powershell
#Check WSUS connectivity

#START_OF_SCRIPT

$hostname = $env:computername
Try 
{ 
    #Create Session COM object
    $updatesession =  [activator]::CreateInstance([type]::GetTypeFromProgID("Microsoft.Update.Session",$hostname))
    $updatesearcher=$updatesession.CreateUpdateSearcher()
    $searchresult=$updatesearcher.Search("IsInstalled=0")
    $pendingupdate=$searchresult.Updates.Count
    "Pending KB Count="+$pendingupdate
} 
Catch 
{ 
    Write-Host "WSUS Connectivity Issue" 
    Break 
}

#END_OF_SCRIPT
