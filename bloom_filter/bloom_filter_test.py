import unittest
from bloom_filter import BloomFilter

class TestBloomFilter(unittest.TestCase):
    def test_element_membership(self):
        bf = BloomFilter(10)  # Bloom filter with 10 bits and 3 hash functions

        # Test inserting elements
        bf.insert("apple")
        bf.insert("banana")
        bf.insert("orange")

        # Test checking for existing elements
        self.assertTrue(bf.contains("apple"))
        self.assertTrue(bf.contains("banana"))
        self.assertTrue(bf.contains("orange"))

        # Test checking for non-existing elements
        self.assertFalse(bf.contains("grape"))
        self.assertFalse(bf.contains("watermelon"))

    def test_false_positive_rate(self):
        # Test the false positive rate of the Bloom Filter
        num_elements = 100
        bf = BloomFilter(1000)  # Bloom filter with 1000 bits and 3 hash functions

        # Insert some elements
        for i in range(num_elements):
            bf.insert(f"element_{i}")

        # Check for false positives
        false_positive_count = 0
        for i in range(num_elements):
            if bf.contains(f"non_existing_{i}"):
                false_positive_count += 1

        false_positive_rate = false_positive_count / num_elements
        # Since the number of hash functions and bit array size affect the false positive rate,
        # the rate might be higher than 0 but should be relatively low in a well-configured Bloom Filter.
        self.assertLessEqual(false_positive_rate, 0.1)  # Expecting false positive rate <= 10%

if __name__ == "__main__":
    unittest.main()
