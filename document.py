# Document class
# holds one document (like one news article)

class Document:
    def __init__(self, doc_id, title, text):
        self.doc_id = doc_id
        self.title = title
        self.text = text

    def __str__(self):
        return str(self.doc_id) + ": " + self.title

    # print a short version of the text so it doesnt fill the whole screen
    def preview(self):
        if len(self.text) > 80:
            return self.text[0:80] + "..."
        else:
            return self.text
