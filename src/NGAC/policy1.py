import re
from ngac_types.user import User
from ngac_types.resource import Resource
from ngac_types.ngac_attribute import UserAttribute, ObjectAttribute


def assign(args):
    print("hej")
    return ""
    pass


lookup_dic = {
    "user": User,
    "user_attribute": UserAttribute,
    "object": Resource,
    "object_attributes": ObjectAttribute,
    "assign": assign,
}

if __name__ == "__main__":
    text = ""

    with open("./policy1.pl", "r") as f:
        text = f.read()
    matches = re.findall(r"([a-z|_]*)\((.*?)\)", text)
    policy = []

    for x in matches:
        if x[0] in lookup_dic.keys():
            policy.append(lookup_dic[x[0]](x[1]))
            print(x[1])
    for p in policy:
        print(p)

    print(policy)
