Write-Output "Installing all dependencies"
python -m pip install -r dependencies.txt
Write-Output "Running setup tool" 
python setup.py
