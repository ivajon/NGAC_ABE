import re
from typing import List
from json import dumps

# # Use NGAC to read the policy from the server
# from NGAC import NGAC


def parse(text: List[str]):
    """
    Gets all the attributes assigned to a user or object
    """
    policy = {
        "user": {},
        "object": {},
        "user_attribute": {},
        "object_attribute": {},
        "connector": [],
        "associate": {},
    }

    def user(args):
        policy["user"][args[1]] = []

    def object(args):
        policy["object"][args[1]] = []

    def assign(args):
        name, attribute = args[1].split(",")
        # We can assign attribute to user or object
        if name in policy["user"].keys():
            policy["user"][name].append(attribute)
        elif name in policy["object"].keys():
            policy["object"][name].append(attribute)
        elif name in policy["user_attribute"].keys():
            policy["user_attribute"][name].append(attribute)
        elif name in policy["object_attribute"].keys():
            policy["object_attribute"][name].append(attribute)

    def user_attribute(args):
        attribute = args[1]
        policy["user_attribute"][attribute] = []

    def object_attribute(args):
        attribute = args[1]
        policy["object_attribute"][attribute] = []

    def associate(args):
        args: str = args[1]
        associate_list = args.split(",")
        rights = associate_list[1:-1]

        for i in range(0, len(rights)):
            rights[i] = rights[i].replace("[", "")
            rights[i] = rights[i].replace("]", "")

        # print(associate_list)
        # print(dumps(policy["associate"]))
        associations = policy["associate"]
        if associate_list[0] in associations.keys():
            attribute_association = associations[associate_list[0]]
            attribute_association[associate_list[-1]] = rights
        else:
            associations[associate_list[0]] = {associate_list[-1]: rights}

    policy_builder = {
        "user": user,
        "object": object,
        "assign": assign,
        "user_attribute": user_attribute,
        "object_attribute": object_attribute,
        "associate": associate,
    }

    for line in text:
        # All NGAC policy elements are function calls
        # The syntax is as follows:
        # <Policy Element>(<Policy Element Arguments>)
        # Policy Element Arguments are comma separated

        element = re.findall(r"([a-z|_]*)\((.*?)\)", line)

        # Now we want to find all attribute assignments
        if len(element) > 0:
            element = [x.replace("'", "") for x in element[0]]
            if element[0] in policy_builder.keys():
                policy_builder[element[0]](element)
    return policy


def get_all_user_attributes(policy):
    attributes = {}
    pol = parse(policy)
    users = list(pol["user"].keys())
    # print(users)

    for user in users:
        attributes[user] = get_user_attributes(user, pol, True)
    return attributes


def get_all_object_attributes(policy):
    attributes = {}
    pol = parse(policy)
    objects = list(pol["object"].keys())
    # print(object)

    for object in objects:
        attributes[object] = get_objects_attributes(object, pol, True)
    return attributes


def get_user_attributes(user, policy, preparsed=False) -> List[str]:
    """
    Gets all of the attributes assigned to an user
    """
    # # Create admin NGAC instance, the static admin key is bad.
    # # Replace with a dynamic key when in production
    # ngac = NGAC(key="admin_key")
    # # Read the current policy
    # pol = parse(ngac.read())
    if preparsed == True:
        pol = policy
    else:
        pol = parse(policy)
    if user not in pol["user"].keys():
        return []
    attributes = pol["user"][user]
    no_new_attributes = False

    # Insert all the attributes that are assigned to the attributes
    while not no_new_attributes:

        # Go over all attributes
        for attribute in attributes:

            # If the attribute is assigned to another attribute
            # Add the assigned attribute to the list of attributes
            if attribute in pol["user_attribute"].keys():

                attributes.extend(pol["user_attribute"][attribute])
                # We now have a new attribute, so we need to check again
                no_new_attributes = True

    return attributes


def get_objects_attributes(object, policy, preparsed=False) -> List[str]:
    """
    Gets all of the attributes assigned to an object
    """

    if preparsed == True:
        pol = policy
    else:
        pol = parse(policy)
    # print(dumps(pol, indent=4))
    # print(pol["associate"]["GroupA"])
    if object not in pol["object"].keys():
        return []
    attributes = pol["object"][object]
    no_new_attributes = False

    # Insert all the attributes that are assigned to the attributes
    while not no_new_attributes:

        # Go over all attributes
        for attribute in attributes:

            # If the attribute is assigned to another attribute
            # Add the assigned attribute to the list of attributes
            if attribute in pol["object_attribute"].keys():

                attributes.extend(pol["object_attribute"][attribute])
                # We now have a new attribute, so we need to check again
                no_new_attributes = True

    return attributes


def get_assocs(parsed):
    associations = parsed["associate"]
    print(associations)
    return associations


def get_connection(user_id, object_id, access_mode, policy):  # access_mode r or w
    parsed = parse(policy)  # parse policy
    # Write a small function to get the attributes parsed["user_attributes"]["u1"]
    user_attr = get_user_attributes(user_id, parsed, preparsed=True)
    # Write a small function to get the attributes parsed["object_attributes"]["o1"]
    object_attr = get_objects_attributes(object_id, parsed, preparsed=True)
    # Write a small function to get the associations parsed["associations"]
    assoc = get_assocs(parsed)

    for ua in user_attr:
        if ua in assoc.keys():
            for oa in object_attr:
                if oa in assoc[ua].keys():
                    if access_mode in assoc[ua][oa]:
                        return ua, oa

    return None


if __name__ == "__main__":
    text = ""

    with open("./src/NGAC/executables/EXAMPLES/policy1.pl", "r") as f:
        text = f.read()

    lines = text.split("\n")
    # print(dumps(parse(lines), indent=4))
    # print(get_user_attributes("u1", lines))
    # print(get_objects_attributes("o1", lines))
    # print(get_connection("u1", "o1", "w", lines))
    print(get_all_user_attributes(lines))
    print(get_all_object_attributes(lines))
