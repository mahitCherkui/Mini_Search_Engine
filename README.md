# Mini_Search_Engine
A search engine that will only look a select few of documents or online through reddit or news articles for your top matching results.

## How to run
You need Python 3 (I used 3.14 but any Python 3 should work). No libraries need to be installed.

```
python3 main.py
```
Type a word or a few words and press enter. Type `quit` to stop.

To run the tests:
```
python3 test_search.py
```

To compare with stemming on and off:
```
python3 compare.py
```

## 1. Project idea
The program loads a bunch of text documents (short news articles) and lets you search them by keyword. You type a query and it gives back the top matching documents ranked by how relevant they are. It's like a really small version of Google but only for the files in the `data` folder.

## 2. Dataset
I wrote 15 short news style articles myself and put them in the `data/` folder (`doc1.txt` to `doc15.txt`). The first line of each file is the headline and the rest is the article. They are about different topics (sports, weather, tech, the city, running, etc.) and some of them share words on purpose so the ranking can be tested.

You don't have to download anything since the files are in the repo. You can also add your own `.txt` files to the folder and they will get loaded (first line = title). If you want a bigger dataset you could use the 20 Newsgroups dataset (http://qwone.com/~jason/20Newsgroups/) or a news headlines dataset from Kaggle, but I didn't use those.

## 3. Design
Files:
- `document.py` - `Document` class. Stores `doc_id`, `title`, `text`. Has `preview()` that returns the first 80 characters.
- `preprocess.py` - `preprocess(text)` makes the text lowercase, removes punctuation, splits into words and removes stop words (and stems them, see improvements). Also has `stem(word)`.
- `search_index.py` - `SearchIndex` class.
  - `add_document(doc)` - preprocesses the title + text and adds every word to the inverted index.
  - `search(query, k)` - preprocesses the query, finds the documents that have all the words, scores them, and returns the top k.
- `main.py` - `load_documents(folder)` reads the txt files into Document objects, `main()` builds the index and runs the search loop.
- `test_search.py` - unit tests.
- `compare.py` - runs some queries with stemming off and on.

How they work together: `main.py` loads the files -> makes `Document` objects -> `add_document()` for each one (which calls `preprocess()`) -> then in the loop every query goes to `search()` (which also calls `preprocess()` on the query so it matches the same way) -> results get printed.

## 4. Libraries
- `string` - for `string.punctuation`
- `heapq` - for `nlargest` to get the top k results
- `os` - for reading the files in the data folder
- `unittest` - for the tests

All of these come with Python so nothing to install.

## 5. Data structures
- **Dictionary (inverted index)** - this is the main one. It maps each word to another dictionary of `{doc_id: count}`. So for "basketball" it would be something like `{7: 2, 8: 2}`. This means search doesn't have to look through every document, it just looks up the word.
- **Set** - for each query word I take the set of doc ids that contain it and do set intersection (`&`) to get the docs that have ALL the words.
- **Heap** - `heapq.nlargest(k, scores)` to get the top k results without sorting the whole list.
- **List** - stop words, the list of documents, the list of results.

Algorithms: searching/lookup with hashing (dict), set intersection, and a heap (priority queue) for picking the top k. Ranking is basically counting.

## 6. Test cases
In `test_search.py`:
1. a word that is in only one document returns that document
2. a two word query only returns docs that have both words
3. search is case insensitive ("DOG" and "dog" give the same results)
4. an unknown word returns an empty list (no crash)
5. empty query, spaces only, or only stop words returns an empty list (no crash)
6. the doc that has the word more times is ranked first
7. `k` limits the number of results
8. preprocess removes punctuation, uppercase and stop words
9. (added later) stemming: "run" finds both "runner" and "running"

All 9 pass:
```
.........
----------------------------------------------------------------------
Ran 9 tests in 0.000s

OK
```

## 7. Expectations / weaknesses
I expected it to work well for simple searches on a small set of docs. Expected weaknesses:
- it only matches exact words so "run" and "running" are different words (I tried to fix this, see below)
- ranking is just word count so longer documents could win just because they're longer
- all words have to be in the doc, so if you type one extra word that's not there you get nothing
- no spelling correction, "basketbal" finds nothing
- apostrophes just get removed so "team's" becomes "teams"

## Results
Here is what I got running `main.py` with some searches (with stemming turned on):

```
==== Mini Search Engine ====
Loaded 15 documents
Type a search, or type quit to exit

Search: basketball
Top results:
1. Local High School Basketball Team Wins State Championship  (score: 2)
2. Basketball Star Signs New Contract  (score: 2)

Search: rain flooding
Top results:
1. Heavy Rain Causes Flooding In Several Towns  (score: 5)

Search: BATTERY
Top results:
1. Tech Company Releases New Phone With Longer Battery  (score: 2)
2. Electric Car Sales Keep Growing  (score: 1)

Search: zebra
No results found.

Search: the
No results found.
```
(I cut out the preview lines so it's shorter)

Interpreting the results:
- "basketball" found the 2 basketball articles and nothing else, which is right. They both have a score of 2 because they both say basketball once in the title and once in the text so it's a tie.
- "rain flooding" only gave the flooding article even though the storm article also says "rain". That's because the storm article doesn't have "flooding" and the search needs all the words. Score is 5 because rain and flooding show up a bunch of times.
- "BATTERY" in caps still worked so case insensitive works. The phone article is first because it says battery twice (title + text), the electric car one only says it once.
- "zebra" isn't in any doc and "the" is a stop word so both return nothing and don't crash.

Note: the doc ids come from the order the files get loaded, which is alphabetical, so doc10.txt loads before doc2.txt. That's why the ids in compare.py don't match the file names.

## Improvements
The biggest problem I saw was that "run", "running" and "runner" were treated as totally different words. So searching "run" gave 0 results even though 3 articles are about running.

To fix it I wrote a simple stemmer (`stem()` in `preprocess.py`). It cuts off endings like -ing, -er, -ers, -ed, -es, -s and then fixes double letters (running -> runn -> run). It's applied to both the documents and the query so they match the same way. You can turn it off with `USE_STEMMING = False` in `preprocess.py`.

Output from `compare.py` (numbers in brackets are doc ids):
```
===== stemming = False =====
running         3 results  [9, 14, 5]
run             0 results  []
runner          1 results  [14]
basketball      2 results  [8, 7]
rain            2 results  [11, 3]
battery         2 results  [10, 15]
coding classes  1 results  [2]
electric cars   1 results  [15]
storm power     1 results  [3]

===== stemming = True =====
running         3 results  [14, 9, 5]
run             3 results  [14, 9, 5]
runner          3 results  [14, 9, 5]
basketball      2 results  [8, 7]
rain            2 results  [11, 3]
battery         2 results  [10, 15]
coding classes  1 results  [2]
electric cars   1 results  [15]
storm power     1 results  [3]
```

With stemming, "run", "running" and "runner" all give the same 3 articles (the marathon one, the running/sleep study, and the park with a running track). Without it "run" gave nothing. The marathon article (14) also moved to first for "running" because it has "runner" and "running" which now count as the same word, which makes sense since it's the most about running. The other searches didn't change so it didn't break anything.

Problems with my stemmer:
- "battery" and "batteries" still don't match (becomes "battery" and "batteri")
- some words get cut weird, like "class" -> "clas" or "lanes" -> "lan". It still works since the query gets cut the same way but it's not perfect
- a real stemmer like the Porter stemmer (in the nltk library) would be better

Other things I could do to make it better if I had more time:
- use TF-IDF instead of just word count so common words matter less and long documents don't win just for being long
- give title words more points than words in the text
- if no doc has all the words, show docs that have some of them instead of nothing
- spelling correction for typos
- try it on a bigger dataset like 20 Newsgroups

## References
- Python docs for heapq: https://docs.python.org/3/library/heapq.html
- Python docs for sets: https://docs.python.org/3/tutorial/datastructures.html#sets
- Python docs for unittest: https://docs.python.org/3/library/unittest.html
- Inverted index: https://en.wikipedia.org/wiki/Inverted_index
- Stemming and the Porter stemmer: https://en.wikipedia.org/wiki/Stemming
- Stop words: https://en.wikipedia.org/wiki/Stop_word
- 20 Newsgroups dataset: http://qwone.com/~jason/20Newsgroups/
- Class notes on dictionaries, sets and heaps
