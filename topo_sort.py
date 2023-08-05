from dataclasses import dataclass
from collections import defaultdict
from typing import List, Set

@dataclass
class DependencyEdge:
    id: int
    depends_on: int

@dataclass
class NodeData:
    id: int
    dependents: Set[int]
    dependencies_count: int = 0

class CyclicDependencyFound(Exception):
    pass

class TopologicalSort:
    def __init__(self, items: int):
        self._items: int = items
        self._nodes: List[NodeData] = [NodeData(id=i, dependents=set(), dependencies_count=0) for i in range(items)]

    def addEdge(self, edge: DependencyEdge) -> None:
        assert(self._isValidNode(edge.id))
        assert(self._isValidNode(edge.depends_on))

        if edge.id in self._nodes[edge.depends_on].dependents:
            return

        self._nodes[edge.depends_on].dependents.add(edge.id)
        self._nodes[edge.id].dependencies_count += 1

    def getOrdering(self) -> List[int]:
        order: List[int] = []
        can_visit: List[int] = []
        pending_dependencies: List[int] = [self._nodes[i].dependencies_count for i in range(self._items)]

        for id in range(self._items):
            if pending_dependencies[id] == 0:
                can_visit.append(id)

        while len(can_visit) > 0:
            id = can_visit.pop()
            order.append(id)

            for dependent in self._nodes[id].dependents:
                pending_dependencies[dependent] -= 1
                if pending_dependencies[dependent] == 0:
                    can_visit.append(dependent)

        if len(order) != self._items:
            raise CyclicDependencyFound()
        
        return order

    def _isValidNode(self, node: int) -> bool:
        return node >= 0 and node < self._items