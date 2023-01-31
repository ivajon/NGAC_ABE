
echo "Starting the NGAC servers"

cd NgacApi/executables  # Go to executables
./better_start_ngac.sh  # Start the NGAC

echo "NGAC servers started"
# Start the interface layer
cd ../..                # Go back to the root directory