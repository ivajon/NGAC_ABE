interpreter="python"
if [ -f "/etc/debian_version" ]; then
    echo "You are running on ubuntu, setting python interpreter to python3"
    interpreter="python3"
fi

echo "Installing dependencies, this might take a while."
$interpreter -m pip install -r dependencies.txt
echo "Running setup tools"
$interpreter setup.py