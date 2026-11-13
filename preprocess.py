import string

# list of common words that dont mean much so we skip them
# (got these from looking at common english words, not every stop word)
STOP_WORDS = ["a", "an", "the", "and", "or", "but", "is", "are", "was", "were",
              "in", "on", "at", "to", "for", "of", "with", "by", "from", "it",
              "this", "that", "these", "those", "be", "been", "has", "have", "had",
              "as", "so", "if", "than", "then", "they", "she", "he", "we", "you",
              "i", "my", "our", "their", "its", "not", "do", "did", "does", "will",
              "said", "says", "who", "what", "which", "more", "some", "also",
              "up", "out", "about", "into", "after", "over", "there", "too"]

# set this to False to turn off stemming (to compare results)
USE_STEMMING = True


# my own simple stemmer so "running", "runner" and "runs" all become "run"
# its not as good as a real one (like porter stemmer) but it helps
def stem(word):
    endings = ["ing", "ers", "er", "ed", "es", "s"]
    for e in endings:
        if word.endswith(e) and len(word) - len(e) >= 3:
            # dont cut the s off words like "class" or "glass"
            if e == "s" and word.endswith("ss"):
                continue
            word = word[:-len(e)]
            break
    # running -> runn -> run
    if len(word) > 3 and word[-1] == word[-2] and word[-1] not in "aeiou":
        word = word[:-1]
    return word


def preprocess(text):
    # make everything lowercase
    text = text.lower()

    # remove punctuation
    # TODO: apostrophes like "team's" turn into "teams" which is kind of weird
    for p in string.punctuation:
        text = text.replace(p, "")

    words = text.split()

    result = []
    for w in words:
        if w not in STOP_WORDS:
            if USE_STEMMING:
                w = stem(w)
            result.append(w)
    # print(result)
    return result
