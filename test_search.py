# tests for the search engine
# run with: python3 test_search.py

import unittest
from document import Document
from search_index import SearchIndex
from preprocess import preprocess


def make_index():
    index = SearchIndex()
    index.add_document(Document(1, "Dogs", "My dog likes to run in the park"))
    index.add_document(Document(2, "Cats", "The cat sleeps all day on the couch"))
    index.add_document(Document(3, "Pets", "A dog and a cat can be friends. The dog is loud"))
    return index


class TestSearch(unittest.TestCase):

    def test_one_word_one_doc(self):
        index = make_index()
        results = index.search("couch")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0][0].doc_id, 2)

    def test_two_words_need_both(self):
        index = make_index()
        results = index.search("dog cat")
        # only doc 3 has both dog and cat
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0][0].doc_id, 3)

    def test_case_insensitive(self):
        index = make_index()
        r1 = index.search("DOG")
        r2 = index.search("dog")
        self.assertEqual(len(r1), len(r2))
        self.assertTrue(len(r1) > 0)

    def test_unknown_word(self):
        index = make_index()
        results = index.search("elephant")
        self.assertEqual(results, [])

    def test_empty_query(self):
        index = make_index()
        self.assertEqual(index.search(""), [])
        self.assertEqual(index.search("   "), [])
        # only stop words
        self.assertEqual(index.search("the and"), [])

    def test_ranking(self):
        index = make_index()
        results = index.search("dog")
        # doc 3 says dog twice so it should be first
        self.assertEqual(results[0][0].doc_id, 3)

    def test_top_k(self):
        index = make_index()
        results = index.search("dog", k=1)
        self.assertEqual(len(results), 1)

    def test_preprocess(self):
        words = preprocess("Hello, World! The END.")
        self.assertEqual(words, ["hello", "world", "end"])

    # added after the stemming improvement
    def test_stemming(self):
        index = SearchIndex()
        index.add_document(Document(1, "Race", "The runner won the race"))
        index.add_document(Document(2, "Gym", "I like running at the gym"))
        results = index.search("run")
        self.assertEqual(len(results), 2)


if __name__ == "__main__":
    unittest.main()
