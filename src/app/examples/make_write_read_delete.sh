# Load ipolicy.pl so we know where we are starting
python src admin -t admin_token loadi -i ipolicy.pl

# Create a new file
python src -u u1  create --file o1 -oa o1,o2
# Write some data to that file
python src -u u1  write --file o1 -i pyproject.toml
# Read the file
python src -u u1 -a ua1 read --file o1
# Delete the file
python src -u u1 -a ua1 delete --file o1
