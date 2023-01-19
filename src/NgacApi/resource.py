"""
Resource
---

This file describes a simple resource abstraction. A resource is a set of `attributes` and a resource specific `Id`.

This resource abstraction is fully agnostic to what the resource actually is. That needs to be done by a content manager.
"""
from typing import List


from .ngac_object import *
from .attribute import ObjectAttribute
from .policy_element import PolicyElement


class Resource(NgacObject, PolicyElement):
    """
    Resource abstraction
    ---

    A Resource is a set of `ObjectAttribute`s and a resource specific `id`.
    """

    def __init__(self, attributes: List[ObjectAttribute] = None, id: str = ""):
        """
        Creates a new resource abstraction.
        """
        self.id = id
        self.attributes = attributes

    def pol_el_repr(self) -> str:
        base_str = ""
        for attr in self.attributes:
            base_str += f"assign({self.id},{attr.get_attribute() if isinstance(attr, ObjectAttribute) else attr});"
        return f"""[object({self.id}),{base_str[:-1]}]"""

    def get_resource(self) -> str:
        """
        Returns the resource id.
        """
        return self.id

    def append(self, attribute: ObjectAttribute):
        """
        Appends an attribute to the resource.
        """
        self.attributes.append(attribute)

    def remove(self, attribute: ObjectAttribute):
        """
        Removes an attribute from the resource.
        """
        self.attributes.remove(attribute)

    def pop(self, index: int) -> ObjectAttribute:
        """
        Pops an attribute from the resource.
        """
        return self.attributes.pop(index)

    def __iter__(self):
        """
        Iterates over the resource's attributes.
        """
        return iter(self.attributes)

    def __getitem__(self, index: int) -> ObjectAttribute:
        """
        Returns the attribute at the given index.
        """
        return self.attributes[index]

    def __len__(self) -> int:
        """
        Returns the number of the resources.
        """
        return len(self.attributes)

    def __str__(self) -> str:
        """
        returns the string representation of the resource.
        """
        return f"Resource({self.id}), attributes: {self.attributes}"

    def __repr__(self) -> str:
        """
        returns the string representation of the resource.
        """
        return self.__str__()


def test_create_resource():
    """
    Tests the creation of a resource.
    """
    attributes = [ObjectAttribute("attr1"), ObjectAttribute("attr2")]
    resource = Resource(attributes, id="resource1")
    assert resource.id == "resource1"
    assert resource.attributes == attributes


def test_iterate_over_resource():
    """
    Tests the iteration over a resource.
    """
    attributes = [ObjectAttribute("attr1"), ObjectAttribute("attr2")]
    resource = Resource(attributes, id="resource1")
    for attribute in resource:
        assert attribute in attributes


def test_append_resource():
    """
    Tests the appending of a resource.
    """
    attributes = [ObjectAttribute("attr1"), ObjectAttribute("attr2")]
    resource = Resource(attributes, id="resource1")
    resource.append(ObjectAttribute("attr3"))
    assert len(resource.attributes) == 3


def test_remove_resource():
    """
    Tests the removal of a resource.
    """
    attributes = [ObjectAttribute("attr1"), ObjectAttribute("attr2")]
    resource = Resource(attributes, id="resource1")
    resource.remove(ObjectAttribute("attr2"))
    assert len(resource.attributes) == 1


def test_resource_cover_all():
    """
    Tests the coverage of the resource class.
    """
    attributes = [ObjectAttribute("attr1"), ObjectAttribute("attr2")]
    resource = Resource(attributes, id="resource1")
    assert resource.get_resource() == "resource1"
    assert resource.pop(0) == ObjectAttribute("attr1")
    assert resource[0] == ObjectAttribute("attr2")
    assert len(resource) == 1
    assert str(resource) == repr(resource)
