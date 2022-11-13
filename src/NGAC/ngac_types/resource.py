"""
Resource abstraction

A resource can be a file or something else
"""
from typing import List


def relative_import(package, module):
    """
    Solves pythons relative import problem
    """
    import os

    exec(
        f"""from {"" if os.getcwd().endswith("ngac_types") else "ngac_types." if os.getcwd().endswith("NGAC") else "NGAC.ngac_types."}{package} import {module}"""
    )
    return locals()[module]


NgacObject = relative_import("ngac_object", "NgacObject")
ObjectAttribute = relative_import("ngac_attribute", "ObjectAttribute")


class Resource(NgacObject):
    """
    Resource abstraction

    it's possible to iterate over a resource's attributes

    Example:
    ```python
    for attr in resource:
        print(attr)
    ```

    A resource is much more static than a `user`
    """

    def __init__(self, attributes: List[ObjectAttribute], id: str = ""):
        self.id = id
        self.attributes = attributes
        # super.__init__("Resource")

    def get_resource(self) -> str:
        """
        Returns the resource id
        """
        return self.id

    def append(self, attr: ObjectAttribute):
        """
        Appends an attribute to the resource
        """
        self.attributes.append(attr)

    def remove(self, attr: ObjectAttribute):
        """
        Removes an attribute from the resource
        """
        self.attributes.remove(attr)

    def pop(self, index: int) -> ObjectAttribute:
        """
        Pops an attribute from the resource
        """
        return self.attributes.pop(index)

    def append(self, attr: ObjectAttribute):
        """
        Appends an attribute to the resource
        """
        self.attributes.append(attr)

    def __iter__(self):
        return iter(self.attributes)

    def __getitem__(self, index: int) -> ObjectAttribute:
        return self.attributes[index]

    def __len__(self) -> int:
        return len(self.attributes)

    def __str__(self) -> str:
        return f"Resource({self.id}), attributes: {self.attributes}"

    def __repr__(self) -> str:
        return self.__str__()


def test_create_resource():
    """
    Tests the creation of a resource
    """
    ObjectAttribute = relative_import("ngac_attribute", "ObjectAttribute")
    attributes = [ObjectAttribute("attr1"), ObjectAttribute("attr2")]
    resource = Resource(attributes, id="resource1")
    assert resource.id == "resource1"
    assert resource.attributes == attributes


def test_iterate_over_resource():
    """
    Tests the iteration over a resource
    """
    ObjectAttribute = relative_import("ngac_attribute", "ObjectAttribute")
    attributes = [ObjectAttribute("attr1"), ObjectAttribute("attr2")]
    resource = Resource(attributes, id="resource1")
    for attr in resource:
        assert attr in attributes


def test_append_resource():
    """
    Tests the appending of a resource
    """
    ObjectAttribute = relative_import("ngac_attribute", "ObjectAttribute")
    attributes = [ObjectAttribute("attr1"), ObjectAttribute("attr2")]
    resource = Resource(attributes, id="resource1")
    resource.append(ObjectAttribute("attr3"))
    assert len(resource.attributes) == 3


def test_remove_resource():
    """
    Tests the removal of a resource
    """
    ObjectAttribute = relative_import("ngac_attribute", "ObjectAttribute")
    attributes = [ObjectAttribute("attr1"), ObjectAttribute("attr2")]
    resource = Resource(attributes, id="resource1")
    resource.remove(ObjectAttribute("attr2"))
    assert len(resource.attributes) == 1
