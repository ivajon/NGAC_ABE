# Load ipolicy.pl so we know where we are starting
python src admin -t admin_token loadi -i ipolicy.pl

# User 1 wants to make a file
python src -u u1  create --file o1 -oa oa1,oa2
# Write to that file
python src -u u1  write --file o1 -i pyproject.toml
# Read the file
python src -u u1 read --file o1

# User 2 wants to read the same file
python src -u u2 -a ua1 read --file o1
echo "This should have failed"

# User 2 tells admin to grant access
python src admin -t admin_token assign -u u2 -a ua1
python src -u u2 read --file o1




# Delete the file
python src -u u1 delete --file o1

# Try to read it now that it is removed

python src -u u1 read --file o1
