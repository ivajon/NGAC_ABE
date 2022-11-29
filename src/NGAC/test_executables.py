import subprocess

# Here we want to test the ngac executables




def start_process(path, args):
    process = subprocess.Popen([path, args])
    return process


def stop_process(process):
    process.terminate()
    process.wait()
    assert process.poll() is not None


def simple_get_sequence():
    import os

    import requests
    import time

    time.sleep(2)

    base_url = "http://127.0.0.1:8001/paapi/setpol"
    data = {"policy": "Policy (a)", "token": "admin_token"}

    r = requests.get(base_url, params=data)
    print(r.text)
    if r.status_code != 200:
        print(r.text)
        assert False
    print("Success")

def test_simple_get_sequence():
    import os
    os.chdir("executables")
    cme = start_process("python3", "cme.py")
    pep = start_process("python3", "pep.py")
    ngac = start_process("python3", "ngac_server.py")
    
    import time
    time.sleep(2)

    simple_get_sequence()

    stop_process(cme)
    stop_process(pep)
    stop_process(ngac)
    os.chdir("..")

if __name__ == "__main__":
    test_simple_get_sequence()

