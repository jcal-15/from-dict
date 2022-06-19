from typing import Optional, Union

import sys

from from_dict import from_dict, FromDictTypeError

if sys.version_info[:2] >= (3, 7):
    from dataclasses import dataclass
else:
    from attr import dataclass


@dataclass(frozen=True)
class SimpleNode:
    name: str
    value: str


@dataclass(frozen=True)
class SimpleNode2:
    name: str
    reference: str

@dataclass(frozen=True)
class NodeWithOptional:
    node1: SimpleNode
    node2: Optional[SimpleNode]
    node3: Optional[SimpleNode] = None


@dataclass(frozen=True)
class NodeWithUnion:
    node: Union[SimpleNode, SimpleNode2]

@dataclass(frozen=True)
class NodeWithUnionWithBuiltInType:
    node: Union[SimpleNode, str]

def test_optional():
    data = {
        "node1": {"name": "n1", "value": "v1"},
        "node2": {"name": "n2", "value": "v2"},
        "node3": {"name": "n3", "value": "v3"},
     }
    node = from_dict(NodeWithOptional, data, fd_check_types=True)
    assert node.node1.name == "n1"
    assert node.node1.value == "v1"
    assert node.node2.name == "n2"
    assert node.node2.value == "v2"
    assert node.node3.name == "n3"
    assert node.node3.value == "v3"
    
    data = {
        "node1": {"name": "n1", "value": "v1"},
        "node2": {"name": "n2", "value": "v2"}
     }
    node = from_dict(NodeWithOptional, data, fd_check_types=True)
    assert node.node1.name == "n1"
    assert node.node1.value == "v1"
    assert node.node2.name == "n2"
    assert node.node2.value == "v2"
    assert node.node3 == None
    
    data = {
        "node1": {"name": "n1", "value": "v1"},
        "node2": None
     }
    node = from_dict(NodeWithOptional, data, fd_check_types=True)
    assert node.node1.name == "n1"
    assert node.node1.value == "v1"
    assert node.node2 == None
    assert node.node3 == None
    data = {
        "node1": {"name": "n1", "value": "v1"},
        "node2": None,
        "node3": None
     }
    node = from_dict(NodeWithOptional, data, fd_check_types=True)
    assert node.node1.name == "n1"
    assert node.node1.value == "v1"
    assert node.node2 == None
    assert node.node3 == None
    
    data = {"node1": {"name": "n1", "value": "v1"}}
    try:
        node = from_dict(NodeWithOptional, data, fd_check_types=True)
        raise AssertionError("Expected to raise an exception")
    except TypeError as ex:
        assert "missing 1 required positional argument: 'node2'" in str(ex)


def test_union():
    data = {  "node": {"name": "n1", "value": "v1"} }
    node = from_dict(NodeWithUnion, data, fd_check_types=True)
    assert isinstance(node.node, SimpleNode)
    assert node.node.name == "n1"
    assert node.node.value == "v1"

    data = {  "node": {"name": "n1", "reference": "node-X"} }
    node = from_dict(NodeWithUnion, data, fd_check_types=True)
    assert isinstance(node.node, SimpleNode2)
    assert node.node.name == "n1"
    assert node.node.reference == "node-X"

    data = {  "node": {"name": "n1", "no_match": "node-X"} }
    node = from_dict(NodeWithUnion, data)
    assert isinstance(node.node, dict)
    assert node.node["name"] == "n1"
    assert node.node["no_match"] == "node-X"
    
    data = {  "node": {"name": "n1", "no_match": "node-X"} }
    try:
        node = from_dict(NodeWithUnion, data, fd_check_types=True)
        raise AssertionError("Expected to raise an exception")
    except TypeError:
        pass


def test_union_with_builtin_type():
    data = {  "node": {"name": "n1", "value": "v1"} }
    node = from_dict(NodeWithUnionWithBuiltInType, data, fd_check_types=True)
    assert isinstance(node.node, SimpleNode)
    assert node.node.name == "n1"
    assert node.node.value == "v1"

    data = {  "node": "Hello" }
    node = from_dict(NodeWithUnionWithBuiltInType, data, fd_check_types=True)
    assert isinstance(node.node, str)
    assert node.node == "Hello"

    data = {  "node": {"name": "n1", "no_match": "node-X"} }
    node = from_dict(NodeWithUnionWithBuiltInType, data)
    assert isinstance(node.node, dict)
    assert node.node["name"] == "n1"
    assert node.node["no_match"] == "node-X"
    
    data = {  "node": {"name": "n1", "no_match": "node-X"} }
    try:
        node = from_dict(NodeWithUnion, data, fd_check_types=True)
        raise AssertionError("Expected to raise an exception")
    except FromDictTypeError:
        pass
    
    data = {  "node": 123 }
    try:
        node = from_dict(NodeWithUnion, data, fd_check_types=True)
        raise AssertionError("Expected to raise an exception")
    except FromDictTypeError:
        pass