import subprocess

# Here we want to test the ngac executables


def cd():
    import os

    if os.path.exists("executables"):
        os.chdir("executables")


def start_process(path, args):
    cd()
    process = subprocess.Popen([path, args])
    return process


def stop_process(process):
    process.terminate()
    process.wait()
    assert process.poll() is not None


def test_simple_get_sequence():
    import os
    # Start the server, if os is ubuntu we need to use python3
    process = start_process("python3", ".")
    assert process.poll() is None
    import requests
    import time

    time.sleep(1)

    base_url = "http://127.0.0.1:8001/paapi/setpol"
    data = {"policy": "Policy (a)", "token": "admin_token"}
    r = requests.post(base_url, data=data)
    print(r.text)
    if r.status_code != 200:
        print(r.text)
        stop_process(process)
        assert False

    stop_process(process)
    assert process.poll() is not None
    print("Success")

    subprocess.call(["killall", "swipl"])
    subprocess.call(["killall", "tee"])


def test_start():
    cd()

    # Start the server
    process = subprocess.Popen(["python", "."])
    assert process.poll() is None
    process.terminate()
    process.wait()
    assert process.poll() is not None

    subprocess.call(["killall", "swipl"])
    subprocess.call(["killall", "tee"])


if __name__ == "__main__":
    test_simple_get_sequence()
