import os
from document import Document
from search_index import SearchIndex

DATA_FOLDER = "data"


def load_documents(folder):
    docs = []
    count = 1
    files = sorted(os.listdir(folder))
    for filename in files:
        if filename.endswith(".txt"):
            f = open(os.path.join(folder, filename), "r", encoding="utf-8")
            lines = f.readlines()
            f.close()
            if len(lines) == 0:
                continue
            # first line is the title, the rest is the text
            title = lines[0].strip()
            text = ""
            for line in lines[1:]:
                text = text + line.strip() + " "
            docs.append(Document(count, title, text.strip()))
            count += 1
    return docs


def main():
    # so it works even if you run it from a different folder
    folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), DATA_FOLDER)

    index = SearchIndex()
    docs = load_documents(folder)
    for d in docs:
        index.add_document(d)

    print("==== Mini Search Engine ====")
    print("Loaded " + str(index.num_docs()) + " documents")
    print("Type a search, or type quit to exit")

    while True:
        query = input("\nSearch: ")
        if query.strip().lower() == "quit" or query.strip().lower() == "exit":
            print("bye!")
            break

        results = index.search(query, 5)

        if len(results) == 0:
            print("No results found.")
        else:
            print("Top results:")
            rank = 1
            for r in results:
                doc = r[0]
                score = r[1]
                print(str(rank) + ". " + doc.title + "  (score: " + str(score) + ")")
                print("   " + doc.preview())
                rank += 1


# need this so compare.py can import load_documents without starting the loop
if __name__ == "__main__":
    main()
