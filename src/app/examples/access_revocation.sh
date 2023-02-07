# Load ipolicy.pl so we know where we are starting
python src admin -t admin_token loadi -i ipolicy.pl

python src admin -t admin_token readpol
# Create a new file
python src -u u1  create --file o3 -oa oa1
python src admin -t admin_token readpol
# Write some data to that file
python src -u u1  write --file o3 -i pyproject.toml
# Read the file
python src -u u1 -a ua1 read --file o3

# Now the admin revokes access to that file for user u1
python src admin -t admin_token remove_assign -u u1 -a ua1

# Now we want to read the file
python src -u u1 -a ua1 read --file o3 # This should report an error
