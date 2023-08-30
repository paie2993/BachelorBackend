import functools
from typing import Any
from collections import defaultdict

# documentary purposes
First = Any
Second = Any

Node = str
Property = str
Value = str


# Provides utility functions for manipuling data structures
class Aggregator:
    # shallow-flattening
    def flatten(self, collection: list[list]) -> list:
        return functools.reduce(lambda x, y: x + y, collection, [])

    # aggregates the first value in the tuples by the second value
    def aggregate_by_second_value(
        self, pairs: list[tuple[First, Second]]
    ) -> dict[First, set[Second]]:
        accumulator = defaultdict(set)
        for first, second in pairs:
            accumulator[first].add(second)
        return accumulator

    def intersect(
        self,
        first: dict[Node, dict[Property, Value]],
        second: dict[Node, set[Property]],
    ) -> dict[Node, dict[Property, Value]]:
        accumulator = defaultdict(dict)
        for node, properties in second.items():
            for property in properties:
                if node in first:
                    if property in first[node]:
                        accumulator[node][property] = first[node][property]
        return accumulator
