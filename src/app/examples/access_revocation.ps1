function wait(){
    # Plucked from stack overflow https://stackoverflow.com/questions/20845058/powershell-wait-for-keypress
    do{ Write-Output "Press Enter";$x = [System.Console]::ReadKey() } while( $x.Key -ne "Enter" )
}


Write-Output "Load ipolicy.pl so we know where we are starting"
python src admin -t admin_token loadi -i ipolicy.pl

Write-Output ""
Write-Output ""
Write-Output "Read the currently loaded policy"
python src admin -t admin_token readpol
wait

Write-Output ""
Write-Output ""
Write-Output "Create a new file"
python src -u u1 create --file o3 -oa oa1

Write-Output ""
Write-Output ""
Write-Output "Read the currently loaded policy, to ensure that the file has been added"
python src admin -t admin_token readpol
wait

Write-Output ""
Write-Output ""
Write-Output "Write some data to that file"
python src -u u1 write --file o3 -i pyproject.toml

Write-Output ""
Write-Output ""
Write-Output "Read the file"
python src -u u1 read --file o3

Write-Output ""
Write-Output ""
Write-Output "Now the admin revokes access to that file for user u1"
Write-Output "Get all the attributes we can remove"
python src admin -t admin_token info -u u1
wait

Write-Output ""
Write-Output ""
Write-Output "Remove ua1 since that will remove read access to o1"
python src admin -t admin_token remove_assign -u u1 -a ua1

Write-Output ""
Write-Output ""
Write-Output "Now we want to read the file"
python src -u u1 read --file o3 # This should report an error
