echo "Starting the interface layer"
cd interface_layer      # Go to the interface layer
python ./src &          # Start the interface layer
cd ..                   # Go back to the root directory

echo "Interface layer started"
echo "Now you can start the client"