import heapq
from preprocess import preprocess
from document import Document


class SearchIndex:
    def __init__(self):
        # inverted index
        # word -> {doc_id: how many times the word is in that doc}
        self.index = {}
        # doc_id -> Document object
        self.documents = {}

    def add_document(self, doc):
        self.documents[doc.doc_id] = doc

        # title words count too so we add the title to the text
        words = preprocess(doc.title + " " + doc.text)

        for word in words:
            if word not in self.index:
                self.index[word] = {}
            if doc.doc_id not in self.index[word]:
                self.index[word][doc.doc_id] = 0
            self.index[word][doc.doc_id] = self.index[word][doc.doc_id] + 1

    def num_docs(self):
        return len(self.documents)

    def search(self, query, k=5):
        query_words = preprocess(query)

        # empty query (or only stop words)
        if len(query_words) == 0:
            return []

        # find docs that have ALL the words using sets
        matching = None
        for word in query_words:
            if word not in self.index:
                # word isnt anywhere so nothing can match all words
                return []
            docs_with_word = set(self.index[word].keys())
            if matching == None:
                matching = docs_with_word
            else:
                matching = matching & docs_with_word  # intersection

        # score = total count of the query words in the doc
        scores = []
        for doc_id in matching:
            score = 0
            for word in query_words:
                score = score + self.index[word][doc_id]
            scores.append((score, doc_id))

        # heap to get the top k
        top = heapq.nlargest(k, scores)

        results = []
        for item in top:
            results.append((self.documents[item[1]], item[0]))
        return results
