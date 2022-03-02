import json
import os

def main(productID):
    clusters = []
    sentiments = {}
    counters = {}
    reviews = {}
    with open('./data/model_results.json') as f:
        data = json.load(f)
    for i, product in enumerate(data):
        for prod_id, this_product_reviews in product.items():

                for review in this_product_reviews:
                    aspect_pairs = review["aspect_pairs"]
                    for map in aspect_pairs:
                        if map['cluster'] not in clusters:
                            clusters.append(map['cluster'])
                            sentiments[map['cluster']] = map['polarity']
                            counters[map['cluster']] = 1
                        sentiments[map['cluster']] += map['polarity']
                        counters[map['cluster']] += 1

    for key in sentiments:
        sentiments[key] = sentiments[key]/counters[key]
    return sentiments






if(__name__ == '__main__'):
    print(main('399147659'))

