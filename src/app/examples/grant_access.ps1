function wait(){
    # Plucked from stack overflow https://stackoverflow.com/questions/20845058/powershell-wait-for-keypress
    do{ Write-Output "Press Enter";$x = [System.Console]::ReadKey() } while( $x.Key -ne "Enter" )
}

Write-Output ""
Write-Output ""
Write-Output "Load ipolicy.pl so we know where we are starting"
python src admin -t admin_token loadi -i ipolicy.pl
Start-Sleep -Seconds 4

python src admin -t admin_token readpol
wait


Write-Output ""
Write-Output ""
Write-Output "u1 wants to make a file o1 with attributes oa1,oa2"
python src -u u1 create --file o1 -oa oa1,oa2

Write-Output ""
Write-Output ""
Write-Output "Write to that file"
python src -u u1 write --file o1 -i pyproject.toml
Start-Sleep -Seconds 4

Write-Output ""
Write-Output ""
Write-Output "Read the file"
python src -u u1 read --file o1
Start-Sleep -Seconds 4

Write-Output ""
Write-Output ""
Write-Output "User 2 wants to read the same file"
python src -u u2 read --file oa1
wait
# Check for possible removals
python src admin -t admin_token readpol
wait



Write-Output ""
Write-Output ""
Write-Output "User 2 tells admin to grant access"
python src admin -t admin_token assign -u u2 -a ua1

Write-Output ""
Write-Output ""
Write-Output "Now u2 wants to read the file"
python src -u u2 read --file o1
wait

Write-Output ""
Write-Output ""
Write-Output "Delete the file"
python src -u u1 delete --file o1

Write-Output ""
Write-Output ""
Write-Output "Try to read it now that it is removed"
python src -u u1 read --file o1
