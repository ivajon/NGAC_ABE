function wait(){
    # Plucked from stackoverflow https://stackoverflow.com/questions/20845058/powershell-wait-for-keypress
    do{ Write-Output "Press Enter";$x = [System.Console]::ReadKey() } while( $x.Key -ne "Enter" )
}

Write-Output "`n `nReseting the database"
python src reset

Write-Output "`n `nCreate a new file"
python src -u u1 create --file o1 -oa oa1

Write-Output "`n `nWrite some data to that file"
python src -u u1 write --file o1 -i pyproject.toml

Write-Output "`n `nRead the file"
python src -u u1 read --file o1
