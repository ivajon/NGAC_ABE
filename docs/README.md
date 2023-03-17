# Setting up the system

Firstly clone this repo:

```bash
git clone https://github.com/ivario123/NGAC_ABE.git
```

## Python version

This project requires python 3.9 but should work with any python 3 version higher than 3.7

## Building the NGAC servers

Firstly you need to install `swi-prolog` on your system. After which the following commands clone and build the servers.

```bash
# Remove NGAC folder if it already exists
rm -rf tog-ngac-crosscpp
echo "Cloning the TOG-NGAC repo"
git clone https://github.com/tog-rtd/tog-ngac-crosscpp
echo "Building the NGAC server"
cd tog-ngac-crosscpp
cat server.pl
swipl -v -o ngac -g ngac -c ngac.pl
swipl -v -o ngac_server -g ngac_server -c ngac.pl
echo "Building the CME server"
swipl -v -o cme -g cme -c cme_sim.pl
echo "Building the PEP server"
cd PEP-RAP
swipl -v -o pep_server -g pep_server -c pep.pl
```

## (optional) run the setup tool

The setup tool installs all of the required dependencies and sets up the config files for you!

(on windows)

```ps1
.\setup.ps1
```

(on linux or mac)

```bash
chmod +x setup.bash
./setup.bash
```

and fill in the required information

## Install dependencies

(not needed if using setup tool)

```bash
pip install -r dependencies.txt
```


## Start all of the servers

### Starting the NGAC servers

```bash
echo "-------------"
echo "Starting cme"
echo "------------"
sleep 1
./cme &
sleep 2
echo "------------"
echo "Starting pep"
echo "------------"
sleep 1
cd PEP-RAP
./pep_server &
sleep 2
cd ..
echo "-------------"
echo "Starting ngac"
echo "-------------"
sleep 1
./ngac_server --import EXAMPLES/policy1.pl --port 8001 --epp --jsonresp &
```

### Starting the cryptography server

Refer to [The CryptographyServer](https://github.com/Leohemmingsson/CryptographyServer/blob/main/README.md) documentation

### Starting the interface layer

1. Run the setup tool `setup.py`
2. Ensure that the Crypto server and NGAC are running
3. Start the server `python src` from the interface_layer folder

## Using the app

1. Set the correct url to the interface layer in the `__main__.py` file
2. Use the app
To get all available commands, do

```bash
python src -h
```

from the app folder.

## Using dynamic attributes

Refer to the [ngac-daemon](https://github.com/ivario123/ngac-context-daemon) documentation
