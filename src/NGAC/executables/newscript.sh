# Starts the NGAC servers
# Check what os we are running on, there are 3 options: Debian, Arch, Mac
platform='unknown'
unamestr=$(uname)
echo $unamestr
if [[ "$unamestr" == 'Linux' ]]; then
   platform='linux'
elif [[ "$unamestr" == 'Darwin' ]]; then
    platform='mac'
fi

if [[ "$platform" == 'linux' ]]; then
    # We are running on Debian
    echo "Starting NGAC server on Debian"
    ./linux/ngac_server &
    ./linux/cme &
    ./linux/pep_server &
elif [[ "$platform" == 'mac' ]]; then
    # We are running on Mac
    echo "Starting NGAC server on Mac"
    ./mac/ngac_server &
    ./mac/cme &
    ./mac/pep_server &
else
    echo "Unknown OS"
fi