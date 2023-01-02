import re
from ngac_types.user import User
from ngac_types.resource import Resource
from ngac_types.ngac_attribute import UserAttribute, ObjectAttribute

def assign(args):
    print(" ")
    return ""
    pass

lookup_dic = {
    "user": User,
    "user_attribute": UserAttribute,
    "object": Resource,
    "object_attributes": ObjectAttribute,
    "assign": assign,
}

def user_in(text:str):
    if "user(" in text:
        print(text)

def user_attribute_in(text:str):
    if "user_attribute(" in text:
        print(text)

def object_in(text:str):
    if "object(" in text:
        print(text)

def object_attributes_in(text:str):
    if "object_attributes(" in text:
        print(text)

def assign_in(text:str):
    if "assign(" in text:
        print(text)

if __name__ == "__main__":
    text = ""

    with open("./policy1.pl", "r") as f:
        text = f.read()
    
    lines = text.split("\n")
    for line in lines:
        user_in(line)
        user_attribute_in(line)
        object_in(line)
        object_attributes_in(line)
        assign_in(line)     
    exit()

    matches = re.findall(r"([a-z|_]*)\((.*?)\)", text)
    policy = []

    for x in matches:
        if x[0] in lookup_dic.keys():
            policy.append(lookup_dic[x[0]](x[1]))
            print(x[1])
    for p in policy:
        print(p)

    print(policy)
