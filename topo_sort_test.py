import unittest

from topo_sort import DependencyEdge, TopologicalSort, CyclicDependencyFound

class TestTopologicalSort(unittest.TestCase):
    def test_basic_sort(self):
        # Test a simple case with no cyclic dependencies
        ts = TopologicalSort(4)
        edges = [
            DependencyEdge(id=0, depends_on=1),
            DependencyEdge(id=1, depends_on=2),
            DependencyEdge(id=2, depends_on=3),
        ]
        for edge in edges:
            ts.addEdge(edge)

        self.assertEqual(ts.getOrdering(), [3, 2, 1, 0])

    def test_add_dependencies_after_initial_sort(self):
        ts = TopologicalSort(4)
        edges = [
            DependencyEdge(id=0, depends_on=1),
            DependencyEdge(id=1, depends_on=2),
        ]
        for edge in edges:
            ts.addEdge(edge)

        initial_order = ts.getOrdering()
        self.assertEqual(initial_order, [3, 2, 1, 0])

        # Add more dependencies and get the new order
        additional_edges = [
            DependencyEdge(id=3, depends_on=0),
        ]
        for edge in additional_edges:
            ts.addEdge(edge)

        new_order = ts.getOrdering()
        self.assertEqual(new_order, [2, 1, 0, 3])

        # Ensure the initial order remains unchanged
        self.assertEqual(initial_order, [3, 2, 1, 0])

    def test_cyclic_dependency(self):
        # Test if the code correctly detects cyclic dependencies
        ts = TopologicalSort(3)
        edges = [
            DependencyEdge(id=0, depends_on=1),
            DependencyEdge(id=1, depends_on=2),
            DependencyEdge(id=2, depends_on=0),
        ]
        for edge in edges:
            ts.addEdge(edge)

        with self.assertRaises(CyclicDependencyFound):
            ts.getOrdering()

    def test_repeated_edges(self):
        # Test if repeated edges are handled correctly
        ts = TopologicalSort(5)
        edges = [
            DependencyEdge(id=0, depends_on=1),
            DependencyEdge(id=1, depends_on=2),
            DependencyEdge(id=2, depends_on=3),
            DependencyEdge(id=2, depends_on=4),
        ]
        for edge in edges:
            ts.addEdge(edge)

        self.assertEqual(ts.getOrdering(), [4, 3, 2, 1, 0])

    def test_single_node(self):
        # Test a single node case
        ts = TopologicalSort(1)
        self.assertEqual(ts.getOrdering(), [0])

    def test_empty_graph(self):
        # Test an empty graph
        ts = TopologicalSort(0)
        self.assertEqual(ts.getOrdering(), [])

if __name__ == '__main__':
    unittest.main()
