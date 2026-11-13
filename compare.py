# compares results with and without stemming
# (used this to see if stemming actually helped)
import os
import preprocess
from search_index import SearchIndex
import main

queries = ["running", "run", "runner", "basketball", "rain", "battery", "coding classes", "electric cars", "storm power"]

for setting in [False, True]:
    preprocess.USE_STEMMING = setting
    index = SearchIndex()
    for d in main.load_documents(os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")):
        index.add_document(d)
    print("\n===== stemming = " + str(setting) + " =====")
    for q in queries:
        results = index.search(q, 5)
        ids = []
        for r in results:
            ids.append(r[0].doc_id)
        print(q.ljust(16) + str(len(results)) + " results  " + str(ids))
