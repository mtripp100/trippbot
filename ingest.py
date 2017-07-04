from lxml import html
import requests

def ingest_compact():
    page = requests.get("https://en.wikipedia.org/wiki/List_of_Latin_phrases_(full)")
    tree = html.fromstring(page.content)
    
    rows = tree.xpath("//table[contains(@class, 'wikitable')]/tr[position() > 1]")
    print("{} rows downloaded.".format(len(rows)))

    phrases = []
    for row in rows:
        latin = "".join(row[0].xpath(".//text()"))
        translation = "".join(row[1].xpath(".//text()"))
        notes = "".join(row[2].xpath(".//text()")) if len(row) > 2 else None
        phrases.append((latin, translation, notes))

    print("{} phrases ingested.".format(len(phrases)))
    return phrases
