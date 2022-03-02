import os
import json
import pandas as pd
import sys


BASE_PATH = os.getcwd()
PARENT = os.path.dirname(BASE_PATH)

sys.path.insert(0,BASE_PATH)
from dataprep import clean_data

prod_pronouns = ['it','this','they','these', 'one']

def fetch_reviews (usecols = None):
    reviewpath = './data/reviews.csv'
    raw_data = pd.read_csv(reviewpath, header=0, error_bad_lines=False, usecols=usecols)
    print(raw_data.head())
    return raw_data


def apply_extraction(row,nlp,sid):
    review_body = row['review-text']
    review_id = row['review-id']
    product_id = row['product-id']




    doc=nlp(review_body)
    ## M - Modifier || A - Aspect
    ## Regel1 = M ist ein Kind von A mit der Beziehung amod
    rule1_pairs = []
    rule2_pairs = []
    rule3_pairs = []
    rule4_pairs = []
    rule5_pairs = []
    rule6_pairs = []
    rule7_pairs = []

    for token in doc:
        A = "999999"
        M = "999999"
        if token.dep_ == "amod" and not token.is_stop:
            M = token.text
            A = token.head.text

            # adverb  hinzufügen (e.g. 'most comfortable headphones')
            M_children = token.children
            for child_m in M_children:
                if(child_m.dep_ == "advmod"):
                    M_hash = child_m.text
                    M = M_hash + " " + M
                    break

            # negation im adjektiv
            A_children = token.head.children
            for child_a in A_children:
                if(child_a.dep_ == "det" and child_a.text == 'no'):
                    neg_prefix = 'not'
                    M = neg_prefix + " " + M
                    break

        if(A != "999999" and M != "999999"):
            if A in prod_pronouns :
                A = "general"
            dict1 = {"noun" : A, "adj" : M, "rule" : 1, "polarity" : sid.polarity_scores(token.sent.lower_)['compound']}
            rule1_pairs.append(dict1)

        #zweite Regel
        #  M - Modifier || A - Aspect
        # Direktes Objekt - A ist Kind von einem Wort mit Beziehung nsubj, während
        # M Kind des selben Wortes mit Beziehung dobj ist
        # Annahme - Ein verb hat nur ein NSUBJ und DOBJ
        children = token.children
        A = "999999"
        M = "999999"
        add_neg_pfx = False
        for child in children :
            if(child.dep_ == "nsubj" and not child.is_stop):
                A = child.text

            if((child.dep_ == "dobj" and child.pos_ == "ADJ") and not child.is_stop):
                M = child.text

            if(child.dep_ == "neg"):
                neg_prefix = "not"
                add_neg_pfx = True

        if (add_neg_pfx and M != "999999"):
            M = neg_prefix + " " + M

        if(A != "999999" and M != "999999"):
            if A in prod_pronouns :
                A = "general"
            dict2 = {"noun" : A, "adj" : M, "rule" : 2, "polarity" : sid.polarity_scores(token.sent.lower_)['compound']}
            rule2_pairs.append(dict2)





        ## Dritte Regel
        ## M - Modifier || A - Aspect
        ## Adjectival Complement - A ist Kind eines Wortes mit Beziehung nsubj, während
        ## M Kind des selben Wortes mit Beziehung acomp ist
        ## Annahme - Ein Verb hat nur ein NSUBJ und DOBJ
        ## "The sound of the speakers would be better. The sound of the speakers could be better" - handled using AUX dependency

        children = token.children
        A = "999999"
        M = "999999"
        add_neg_pfx = False
        for child in children :
            if(child.dep_ == "nsubj" and not child.is_stop):
                A = child.text

            if(child.dep_ == "acomp" and not child.is_stop):
                M = child.text

            if(child.dep_ == "aux" and child.tag_ == "MD"):
                neg_prefix = "not"
                add_neg_pfx = True

            if(child.dep_ == "neg"):
                neg_prefix = "not"
                add_neg_pfx = True

        if (add_neg_pfx and M != "999999"):
            M = neg_prefix + " " + M

        if(A != "999999" and M != "999999"):
            if A in prod_pronouns :
                A = "general"
            dict3 = {"noun" : A, "adj" : M, "rule" : 3, "polarity" : sid.polarity_scores(token.sent.lower_)['compound']}
            rule3_pairs.append(dict3)


        ## Vierte Regel
        ## M - Modifier || A - Aspect

        #Adverb eines passiven Verbs - A ist Kind eines Wortes mit Beziehung nsubjpass, während
        # M Kind des selben Wortes mit Beziehung advmod ist

        ## Annahme - Ein Verb hat nur ein NSUBJ und DOBJ


        children = token.children
        A = "999999"
        M = "999999"
        add_neg_pfx = False
        for child in children :
            if((child.dep_ == "nsubjpass" or child.dep_ == "nsubj") and not child.is_stop):
                A = child.text

            if(child.dep_ == "advmod" and not child.is_stop):
                M = child.text
                M_children = child.children
                for child_m in M_children:
                    if(child_m.dep_ == "advmod"):
                        M_hash = child_m.text
                        M = M_hash + " " + child.text
                        break

            if(child.dep_ == "neg"):
                #neg_prefix = child.text
                neg_prefix = "not"
                add_neg_pfx = True

        if (add_neg_pfx and M != "999999"):
            M = neg_prefix + " " + M

        if(A != "999999" and M != "999999"):
            if A in prod_pronouns :
                A = "general"
            dict4 = {"noun" : A, "adj" : M, "rule" : 4, "polarity" : sid.polarity_scores(token.sent.lower_)['compound']}
            rule4_pairs.append(dict4)



        ## Fünfte Regel
        ## M - Modifier || A - Aspect

        #Komplement eines Kopularverbs - A ist Kind von M mit Beziehung nsubj, während
        # M ein Kind mit der Beziehung cop hat

        ## Annahme - Ein Verb hat nur ein NSUBJ und DOBJ

        children = token.children
        A = "999999"
        buf_var = "999999"
        for child in children :
            if(child.dep_ == "nsubj" and not child.is_stop):
                A = child.text
                # check_spelling(child.text)

            if(child.dep_ == "cop" and not child.is_stop):
                buf_var = child.text
                #check_spelling(child.text)

        if(A != "999999" and buf_var != "999999"):
            if A in prod_pronouns :
                A = "general"
            dict5 = {"noun" : A, "adj" : token.text, "rule" : 5, "polarity" : sid.polarity_scores(token.sent.doc)['compound']}
            rule5_pairs.append(dict5)


        ## Sexte Regel
        ## M - Modifier || A - Aspect
        ## Beispiel - "It ok", "ok" ist INTJ (Einwürfe wie "bravo", "great" etc.)

        children = token.children
        A = "999999"
        M = "999999"
        if(token.pos_ == "INTJ" and not token.is_stop):
            for child in children :
                if(child.dep_ == "nsubj" and not child.is_stop):
                    A = child.text
                    M = token.text

        if(A != "999999" and M != "999999"):
            if A in prod_pronouns :
                A = "general"
            dict6 = {"noun" : A, "adj" : M, "rule" : 6, "polarity" : sid.polarity_scores(M)['compound']}
            rule6_pairs.append(dict6)


    ## Siebte Regel
    ## M - Modifier || A - Aspect
    ## ATTR - Verbindung zwischen einem Verb wie 'be/seem/appear' und seinem Komplement
    ## Beispiel: 'this is garbage' -> (this, garbage)

        children = token.children
        A = "999999"
        M = "999999"
        add_neg_pfx = False
        for child in children :
            if(child.dep_ == "nsubj" and not child.is_stop):
                A = child.text

            if((child.dep_ == "attr") and not child.is_stop):
                M = child.text

            if(child.dep_ == "neg"):
                neg_prefix = child.text
                add_neg_pfx = True

        if (add_neg_pfx and M != "999999"):
            M = neg_prefix + " " + M

        if(A != "999999" and M != "999999"):
            if A in prod_pronouns :
                A = "general"
            dict7 = {"noun" : A, "adj" : M, "rule" : 7, "polarity" : sid.polarity_scores(M)['compound']}
            rule7_pairs.append(dict7)



    aspects = []

    aspects = rule1_pairs + rule2_pairs + rule3_pairs +rule4_pairs +rule5_pairs + rule6_pairs + rule7_pairs



    dic = {"product_id" : product_id ,"review_id" : review_id , "aspect_pairs" : aspects}
    return dic


def extract_aspects(reviews,nlp,sid):

    aspect_list = reviews.apply(lambda row: apply_extraction(row,nlp,sid), axis=1)
    return aspect_list


def aspect_extraction(nlp,sid):

    usecols =  ['product-id','review-text','review-id']
    raw_data = fetch_reviews(usecols)
    reviews = clean_data.clean_data(raw_data)
    aspect_list = extract_aspects(reviews,nlp,sid)
    aspect_list = list(aspect_list)
    with open('./data/reviews_aspect_raw.json', 'w') as outfile:
        json.dump(aspect_list, outfile)


    return 1


