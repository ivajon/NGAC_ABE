from requests import post
from json import dumps


def write(data):
    status = post("http://localhost:5000/write", data=data)
    print(dumps(status.text))
    return status.text


def read(data):
    return post("http://localhost:5000/read", data=data).text


def make_file(data):
    ret = post("http://localhost:5000/make_file", data=data)
    print(dumps(ret.text))
    return ret.text


def delete_file(data):
    ret = post("http://localhost:5000/delete_file", data=data)
    print(dumps(ret.text))
    return ret.text


def write_data_to_file(data, resource_id, file_attributes):
    json = dumps(
        {
            "user_id": "u1",
            "resource_id": resource_id,
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
            "resource_id": resource_id,
            "object_attributes": file_attributes,
            "policy": "A & !B",
            "data": data,
        }
    )
    make_file(json)
    write(json)
    delete_file(json)


#print(read(dumps({"user_id": "u1", "resource_id": "o1"})))

#write_data_to_file("Hello World", "o1", ["oa1"])
#write_data_to_file_then_remove("Hello World", "o1", ["oa1"])


def unassign(data):
    return post("http://localhost:5000/admin/user/unassign", data=data, headers={
        "token": "admin_token"
    }).text


def read_pol():
    return post("http://localhost:5000/admin/read_policy", headers={
        "token": "admin_token"
    }).text


"""
Read o1 with u1, we know this should work

unassign ua1 from u1

Read o1 with u1, we know this should not work
"""

print(read(dumps({"user_id": "u1", "resource_id": "o1"})))
print(read_pol())
print(unassign(dumps({"user_id": "u1", "attribute": "ua1"})))
print(read_pol())
print(read(dumps({"user_id": "u1", "resource_id": "o1"})))
