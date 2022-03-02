import requests
from bs4 import BeautifulSoup
import csv
import os

def main(productID):
    count = 1 # the count in queue used to track the elements in queue
    reviews=[] # List to store reviews of the product
    tokenizedReviews = []
    ratings=[] # List to store ratings of the product
    reviewIDs=[]
    no_pages = 100 # no of pages to scrape in the website (provide it via arguments)
    reviewsurl = ''
    i = 0

    url = 'https://www.amazon.com/dp/' + productID


    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36', "Accept-Encoding": "gzip, deflate", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT": "1","Connection": "close", "Upgrade-Insecure-Requests": "1", 'Accept-Language': 'en-us'}

    r = requests.get(url, headers=headers)
    content = r.content
    soup = BeautifulSoup(content, "lxml")
    file = open( os.path.dirname(os.getcwd()) + "/data/reviews.csv", "w")



    for link in soup.findAll('a', attrs={'data-hook': "see-all-reviews-link-foot"}):
        reviewsurl = 'https://www.amazon.com' + link.get('href') + '&pageNumber='
        print(reviewsurl)

    while count <= no_pages :


        reviewsurlWithPageNumber = reviewsurl + str(count)

        resp = requests.get(reviewsurlWithPageNumber, headers=headers)
        content = resp.content
        soup = BeautifulSoup(content, "lxml")

        for d in soup.findAll('span', attrs={'data-hook': 'review-body'}):
            review = d.find('span')
            reviews.append(review.text)

        for a in soup.findAll('div', attrs={'data-hook': 'review'}):
            id = a.get('id')
            reviewIDs.append(id)
            print(id)

        for c in soup.findAll('i', attrs={'data-hook': 'review-star-rating'}):
            rating = c.find('span')
            if rating is not None:
                ratings.append(rating.text)

            else:
                ratings.append('no rating found')
                print('no ratings found')
        count += 1
        print(count)


    writer = csv.writer(file)
    writer.writerow(["product-id", "review-text", "review-id","rating"])
    while i < len(reviews):
        writer.writerow([productID,reviews[i],reviewIDs[i],ratings[i]])
        i += 1
        print(i)



    print('Crawling finished')








