import json
import csv
import os

def main(productID):
    i = 0
    file = open("/Users/daniel/PycharmProjects/KDSeminar/data/bewertung.csv", "w")
    file2 = open("/Users/daniel/PycharmProjects/KDSeminar/data/reviews.csv", "r")
    writer = csv.writer(file)
    reader = csv.reader(file2)
    mydict = {rows[2]: rows[1] for rows in reader}
    file2.seek(0)
    stardict = {rows[2]: rows[3] for rows in reader}
    writer.writerow(['reviewnumber','aspect','pol','cluster','fulltext','rating'])
    with open(os.path.dirname(os.getcwd()) + '/data/model_results.json') as f:
        data = json.load(f)
    for i, product in enumerate(data):
        for prod_id, this_product_reviews in product.items():
            if prod_id == productID:
                for review in this_product_reviews:
                    aspect_pairs = review["aspect_pairs"]
                    if len(aspect_pairs) == 0:
                        writer.writerow([review['review_id'], "-", "-", "-", mydict[str(review['review_id'])]])

                    for map in aspect_pairs:
                        writer.writerow([review['review_id'], map['noun'] + ' ' + map['adj'], map['polarity'], map['cluster'], mydict[str(review['review_id'])], stardict[str(review['review_id'])]])