# Starts the NGAC servers

# Check what os we are running on, there are 3 options: Debian, Arch, Mac

if [ -f /etc/debian_version ]; then
    # We are running on Debian
    echo "Starting NGAC server on Debian"
    ./linux/ngac_server &
    ./linux/cme &
    ./linux/pep_server &
    elif [ -f /etc/arch-release ]; then
    # We are running on Arch
    echo "Starting NGAC server on Arch"
    ./arch/ngac_server &
    ./arch/cme &
    ./arch/pep_server &
    elif [ -f /etc/os-release ]; then
    # We are running on Mac
    echo "Starting NGAC server on Mac"
    ./mac/ngac_server &
    ./mac/cme &
    ./mac/pep_server &
else
    # Unknown.
    echo "Unknown OS"
fi