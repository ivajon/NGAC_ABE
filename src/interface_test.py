from requests import get, post
from json import dumps, loads


def write(data):
    status = post("http://localhost:5000/write", data=data)
    print(
        f"HTTP code: {status.status_code}, text: {status.text if status.status_code == 200 else status.reason}"
    )
    return status.text


def read(data):
    return post("http://localhost:5000/read", data=data).text


def make_file(data):
    ret = post("http://localhost:5000/make_file", data=data)
    print(
        f"HTTP code: {ret.status_code}, text: {ret.text if ret.status_code == 200 else ret.reason}"
    )
    return ret.text


def delete_file(data):
    ret = post("http://localhost:5000/delete_file", data=data)
    print(
        f"HTTP code: {ret.status_code}, text: {ret.text if ret.status_code == 200 else ret.reason}"
    )
    print(ret.text)
    return ret.text


def write_data_to_file(data, resource_id, file_attributes):
    json = dumps(
        {
            "user_id": "u1",
            "object_id": resource_id,
            "object_attributes": file_attributes,
            "policy": "A & !B",
            "data": data,
        }
    )
    make_file(json)
    write(json)


def write_data_to_file_then_remove(data, resource_id, file_attributes):
    json = dumps(
        {
            "user_id": "u1",
            "object_id": resource_id,
            "object_attributes": file_attributes,
            "policy": "A & !B",
            "data": data,
        }
    )
    make_file(json)
    write(json)
    delete_file(json)


print(read(dumps({"user_id": "u1", "resource_id": "o1"})))

#write_data_to_file("Hello World", "o1", ["oa1"])
write_data_to_file_then_remove("Hello World", "o1", ["oa1"])

# post request to localhost:5000/read
# payload = dumps({"user_id": "u1", "resource_id": "o1"})
# print(post("http://localhost:5000/read", data=payload).text)

# payload = dumps({"user_id": "u1", "resource_id": "o1", "policy": "A & !B"})
# print(post("http://localhost:5000/write", data=payload).text)
