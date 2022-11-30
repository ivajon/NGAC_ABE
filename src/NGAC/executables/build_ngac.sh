echo "Cloning the TOG-NGAC repo"
git clone https://github.com/tog-rtd/tog-ngac-crosscpp

echo "Building the NGAC server"
cd tog-ngac-crosscpp
swipl -v -o ngac -g ngac -c ngac.pl
swipl -v -o ngac_server -g ngac_server -c ngac-server.pl

echo "Building the CME server"
swipl -v -o cme_sim -g cme_server -c cme_server.pl

echo "Building the PEP server"
cd PEP-RAP
swipl -v -o pep_server -g pep_server -c pep.pl

echo "SUCCESS: NGAC server built"

