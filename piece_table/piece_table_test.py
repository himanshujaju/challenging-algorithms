import unittest

from piece_table import PieceTable

class TestPieceTable(unittest.TestCase):

    def setUp(self):
        self.piece_table = PieceTable("Hello, World!")

    def test_initial_text(self):
        self.assertEqual(self.piece_table.getText(), "Hello, World!")

    def test_insert_at_beginning(self):
        self.piece_table.insert(0, "Hi ")
        self.assertEqual(self.piece_table.getText(), "Hi Hello, World!")

    def test_insert_at_end(self):
        self.piece_table.insert(len(self.piece_table.getText()), " How are you?")
        self.assertEqual(self.piece_table.getText(), "Hello, World! How are you?")

    def test_insert_in_middle(self):
        self.piece_table.insert(7, "Beautiful ")
        self.assertEqual(self.piece_table.getText(), "Hello, Beautiful World!")

    def test_delete_at_beginning(self):
        self.piece_table.delete(0, 5)
        self.assertEqual(self.piece_table.getText(), ", World!")

    def test_delete_at_end(self):
        self.piece_table.delete(len(self.piece_table.getText()) - 6, len(self.piece_table.getText()))
        self.assertEqual(self.piece_table.getText(), "Hello, ")

    def test_delete_in_middle(self):
        self.piece_table.delete(7, 12)
        self.assertEqual(self.piece_table.getText(), "Hello, !")

    def test_insert_and_delete_combined(self):
        self.piece_table.insert(7, "Beautiful ")
        self.piece_table.delete(0, 7)
        self.assertEqual(self.piece_table.getText(), "Beautiful World!")

    def test_retrieve_substring(self):
        self.assertEqual(self.piece_table.retrieve(7, 12), "World")

    def test_retrieve_whole_text(self):
        self.assertEqual(self.piece_table.retrieve(0, len(self.piece_table.getText())), "Hello, World!")

    def test_retrieve_out_of_range(self):
        self.assertIsNone(self.piece_table.retrieve(-5, 7))
        self.assertIsNone(self.piece_table.retrieve(15, 20))

    def test_empty_text(self):
        empty_piece_table = PieceTable("")
        self.assertEqual(empty_piece_table.getText(), "")

    def test_multiple_insertions_and_deletions(self):
        self.piece_table.insert(7, "Beautiful ")
        self.piece_table.delete(8, 17)
        self.assertEqual(self.piece_table.getText(), "Hello, BWorld!")
        self.piece_table.insert(7, "Wonderful ")
        self.assertEqual(self.piece_table.getText(), "Hello, Wonderful BWorld!")
        self.piece_table.delete(0, 6)
        self.assertEqual(self.piece_table.getText(), " Wonderful BWorld!")

    def test_delete_entire_text(self):
        self.piece_table.delete(0, len(self.piece_table.getText()))
        self.assertEqual(self.piece_table.getText(), "")

if __name__ == '__main__':
    unittest.main()
