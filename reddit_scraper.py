# gets posts from reddit and saves them as txt files in the data folder
# so the search engine can search them like the other articles
# reddit blocks the .json pages now so this uses the rss feed instead
# run with: python3 reddit_scraper.py
import os
import time
import html
import urllib.request
import urllib.error
import xml.etree.ElementTree as ET

DATA_FOLDER = "data"
# rss feeds use this namespace so every tag name needs it in front
ATOM = "{http://www.w3.org/2005/Atom}"


# the post text comes as html so this takes out the <tags>
def remove_tags(text):
    result = ""
    inside_tag = False
    for ch in text:
        if ch == "<":
            inside_tag = True
        elif ch == ">":
            inside_tag = False
            result = result + " "
        elif not inside_tag:
            result = result + ch
    # turns things like &amp; back into &
    result = html.unescape(result)
    # get rid of extra spaces
    return " ".join(result.split())


def get_posts(subreddit):
    url = "https://www.reddit.com/r/" + subreddit + "/.rss"
    # reddit blocks requests that dont look like a browser
    request = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) mini-search-engine/1.0"})

    # try a few times because reddit sometimes says 429 (too many requests)
    root = None
    for attempt in range(3):
        try:
            response = urllib.request.urlopen(request)
            root = ET.fromstring(response.read())
            response.close()
            break
        except urllib.error.HTTPError as e:
            if e.code == 429 and attempt < 2:
                print("r/" + subreddit + " said too many requests, waiting 30 seconds...")
                time.sleep(30)
            else:
                print("could not get r/" + subreddit + ": " + str(e))
                return []
        except Exception as e:
            print("could not get r/" + subreddit + ": " + str(e))
            return []
    if root == None:
        return []

    posts = []
    for entry in root.findall(ATOM + "entry"):
        title = entry.find(ATOM + "title").text
        if title == None:
            continue
        title = title.strip()
        content = entry.find(ATOM + "content")
        text = ""
        if content != None and content.text != None:
            text = remove_tags(content.text)
        # link posts only say "submitted by /u/... [link] [comments]" so cut that off
        if "submitted by" in text:
            text = text[:text.find("submitted by")].strip()
        # link posts have no real text so just use the title
        if text == "":
            text = title
        posts.append((title, text))
    return posts


def save_posts(subreddit, posts, folder):
    count = 0
    for i in range(len(posts)):
        title = posts[i][0]
        text = posts[i][1]
        # title has to be one line since load_documents uses the first line as the title
        title = title.replace("\n", " ")
        filename = "reddit_" + subreddit + "_" + str(i + 1) + ".txt"
        f = open(os.path.join(folder, filename), "w", encoding="utf-8")
        f.write(title + "\n")
        f.write(text + "\n")
        f.close()
        count += 1
    return count


def main():
    folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), DATA_FOLDER)
    subreddits = ["news", "technology", "sports"]

    total = 0
    for i in range(len(subreddits)):
        sub = subreddits[i]
        posts = get_posts(sub)
        saved = save_posts(sub, posts, folder)
        print("saved " + str(saved) + " posts from r/" + sub)
        total += saved
        # reddit only lets you ask a few times a minute so wait between subreddits
        if i < len(subreddits) - 1:
            time.sleep(15)
    print("done, saved " + str(total) + " posts to the data folder")


if __name__ == "__main__":
    main()
