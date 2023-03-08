Write-Output "`n `nLoad cpolicy.pl so we know where we are starting"
python src admin -t admin_token loadi -i cpolicy.pl

Write-Output "`n `nRead the currently loaded policy"
python src admin -t admin_token readpol