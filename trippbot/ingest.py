from database import upload_phrases
import lxml.html
import requests
import hashlib

def ingest_phrases():
    page = requests.get("https://en.wikipedia.org/wiki/List_of_Latin_phrases_(full)")
    tree = lxml.html.fromstring(page.content)

    rows = tree.xpath("//table[contains(@class, 'wikitable')]/tr[position() > 1]")
    print("{} rows downloaded.".format(len(rows)))

    phrases = []
    for row in rows:
        latin = row[0].xpath(".//text()")
        if len(latin) != 1:
            continue
        latin = latin[0].strip()

        translation = row[1].xpath(".//text()")
        if len(translation) != 1:
            continue
        translation = translation[0].strip()

        notes = "".join(row[2].xpath(".//text()")).strip() if len(row) > 2 else None
        phrase_id = hashlib.md5(latin.encode()).hexdigest()
        phrases.append((phrase_id, latin, translation, notes))

    print("{} phrases to insert.".format(len(phrases)))
    upload_phrases(phrases)


if __name__ == "__main__":
    ingest_phrases()
