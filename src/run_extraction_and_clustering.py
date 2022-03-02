import os
import spacy
import sys
from nltk.sentiment.vader import SentimentIntensityAnalyzer

from src import aspect_extraction, mapper, aspect_clustering, crawler, JSON_to_List_Mapper

BASE_PATH = os.getcwd()
sys.path.insert(0,BASE_PATH)
NUM_CLUSTERS = 5




stopwords = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"]

exclude_stopwords = ['it','this','they','these'] # werden erstezt durch 'general', deswegen fast immer eine Kategorie mit diesem Namen

def init_spacy():
    nlp = spacy.load('en_core_web_sm')
    for w in stopwords:
        nlp.vocab[w].is_stop = True
    for w in exclude_stopwords:
        nlp.vocab[w].is_stop = False
    return nlp

def init_nltk():
    try :
        sid = SentimentIntensityAnalyzer()
    except LookupError:
        print("Please install SentimentAnalyzer using : nltk.download('vader_lexicon')")
    return(sid)

def main(productID):
    crawler.main(productID)
    print("jo")
    nlp = init_spacy()
    sid = init_nltk()
    aspect_extraction.aspect_extraction(nlp,sid)
    file_raw = os.path.dirname(os.getcwd()) + "/data/reviews_aspect_raw.json"
    print("hallo")
    file_map = os.path.dirname(os.getcwd()) + "/data/reviews_aspect_mapping.json"
    mapper.map(file_raw, file_map)
    print("hallo1")
    #Apekte werden geclustert
    aspect_clustering.main()
    #Mapper aufrufen des alle Cluster und die jeweilige bewertung ausgibt als Dictionary
    print(JSON_to_List_Mapper.main(productID))

    return JSON_to_List_Mapper.main(productID)



if __name__ == '__main__' :
    main(0)
