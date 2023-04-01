import json
import requests
from bs4 import BeautifulSoup

def get_element():
    pass

# product_code = input("Podaj kod produktu: ")
product_code = "100361771"

url = f"https://www.ceneo.pl/{product_code}#tab=reviews"

response = requests.get(url)
if response.status_code == requests.codes.ok:
    page_dom = BeautifulSoup(response.text, "html.parser")
    opinions = page_dom.select("div.js_product-review")
    opinions_all = []
    for opinion in opinions:
        single_opinion = {
            "opinion_id": opinion("data-entry-id"),
            "author": opinion.select_one("span. user-post_author-name").getText().strip(),
            "recommendation": opinion.select_one("span.user-post_author-recomendation").getText().strip(),
            "score": opinion.select_one("span.user-post_score-count").getText().strip(),
            "confirmed": opinion.select_one("div.review-pz").getText().strip(),
            "opinion_date": opinion.select_one("span.user-post_published > time:nth-child(1)["datetime"]").getText().strip(),
            "purchase_date": opinion.select_one("span.user-post_published > time:nth-child(2)["datetime"]").getText().strip(),
            "up_votes": opinion.select_one("span[id^="votes-yes"]").getText().strip(),
            "down_votes": opinion.select_one("span[id^="votes-no"]").getText().strip(),
            "content": opinion.select_one("div.user-post_text").getText().strip(),
            "cons": [p.get_text().strip() for p in opinion.select("div.review-feature_col:has(>div.review-feature__title--negatives) > div.review-feature__item")],
            "pros": [p.get_text().strip() for p in opinion.select("div.review-feature_col:has(>div.review-feature__title--negatives) > div.review-feature__item")]
        }

    print(json.dumps(single_opinion,indent=4, ensure_ascii=False))